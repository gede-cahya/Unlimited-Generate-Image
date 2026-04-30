# Unlimited Generate Image

Proyek ini adalah generator gambar berbasis AI menggunakan model Stable Diffusion XL (SDXL) dari Stability AI. Proyek ini menyediakan antarmuka web menggunakan Gradio dan REST API menggunakan FastAPI yang diekspos melalui ngrok.

## Fitur
- **Stable Diffusion XL**: Menggunakan model SDXL terbaru untuk kualitas gambar tinggi.
- **FastAPI**: Endpoint `/generate` untuk integrasi programmatic.
- **Gradio UI**: Antarmuka web yang user-friendly.
- **ngrok Integration**: Akses API Anda dari mana saja secara publik.

## Persiapan

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/gede-cahya/Unlimited-Generate-Image.git
   cd Unlimited-Generate-Image
   ```

2. **Instalasi Dependensi**:
   Pastikan Anda memiliki Python 3.8+ dan CUDA terinstal jika ingin menjalankan di GPU.
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi Environment**:
   Salin file `.env.example` menjadi `.env` dan isi token yang diperlukan.
   ```bash
   cp .env.example .env
   ```
   - `HF_TOKEN`: Token dari [Hugging Face](https://huggingface.co/settings/tokens).
   - `NGROK_TOKEN`: Token dari [ngrok Dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).

## Cara Menjalankan

Jalankan perintah berikut:
```bash
python main.py
```

Setelah berjalan:
- **Gradio UI** akan tersedia di URL lokal dan URL publik (jika `share=True` aktif).
- **FastAPI** akan berjalan di port 8000 dan diekspos melalui ngrok.

## Endpoint API

### POST `/generate`
Request Body:
```json
{
  "prompt": "A beautiful landscape of Bali",
  "guidance_scale": 7.5
}
```
Response:
```json
{
  "image_base64": "..."
}
```
