import os
import torch
from dotenv import load_dotenv
from diffusers import StableDiffusionXLPipeline
from fastapi import FastAPI
from pydantic import BaseModel
from pyngrok import ngrok
import nest_asyncio
import uvicorn
import base64
from io import BytesIO
import threading
import gradio as gr

# Load environment variables from .env file
load_dotenv()

# 1. Configuration
hf_token = os.getenv('HF_TOKEN')
ngrok_token = os.getenv('NGROK_TOKEN')

if not hf_token:
    print("Warning: HF_TOKEN not found in environment variables.")
if not ngrok_token:
    print("Warning: NGROK_TOKEN not found in environment variables.")
else:
    # Autentikasi ngrok
    ngrok.set_auth_token(ngrok_token)

# 2. Memuat Model Stable Diffusion XL ke GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Memuat model ke {device}...")

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_safetensors=True,
    token=hf_token
)
pipe = pipe.to(device)
print("Model berhasil dimuat!")

# 3. Membuat REST API dengan FastAPI
app = FastAPI()

# Skema request data
class ImageRequest(BaseModel):
    prompt: str
    guidance_scale: float = 7.5

@app.post("/generate")
def generate_image(req: ImageRequest):
    # Proses inferensi AI
    image = pipe(req.prompt, guidance_scale=req.guidance_scale).images[0]

    # Mengonversi gambar menjadi string Base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": img_str}

# 4. Menjalankan Server dan Mengekspos URL Publik via ngrok
def run_fastapi():
    if ngrok_token:
        try:
            ngrok_tunnel = ngrok.connect(8000)
            print(f"\n=======================================================")
            print(f"API PUBLIK ANDA BERJALAN DI: {ngrok_tunnel.public_url}/generate")
            print(f"=======================================================\n")
        except Exception as e:
            print(f"Gagal menghubungkan ngrok: {e}")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

# 5. UI Gradio
def generate_image_ui(prompt, guidance_scale):
    image = pipe(prompt, guidance_scale=guidance_scale).images[0]
    return image

interface = gr.Interface(
    fn=generate_image_ui,
    inputs=[
        gr.Textbox(label="Masukkan Prompt Teks", placeholder="Contoh: A futuristic city at sunset..."),
        gr.Slider(minimum=1.0, maximum=20.0, value=7.5, step=0.5, label="Guidance Scale")
    ],
    outputs=gr.Image(label="Hasil Gambar"),
    title="Stable Diffusion XL - Image Generator",
    description="Generator gambar AI gratis menggunakan Stable Diffusion XL."
)

if __name__ == "__main__":
    # Jalankan FastAPI di thread terpisah
    threading.Thread(target=run_fastapi, daemon=True).start()
    
    # Jalankan Gradio
    print("Memulai UI Gradio...")
    interface.launch(share=True)
