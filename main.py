# main.py

import os
import threading
import webview
import uvicorn

from app.simulator import start_simulator
from app.api import app

def _run_server():
    uvicorn.run(
        app,
        host="0.0.0.0",                           # ▶️ Ganti dari 127.0.0.1 ke 0.0.0.0
        port=int(os.getenv("PORT", 8000)),       # ▶️ Ambil PORT dari env, default 8000
        log_config=None,
        log_level="info"
    )

if __name__ == "__main__":
    # Mulai simulator data GPS (dummy atau real, tergantung simulator.py)
    start_simulator()

    # Jalankan FastAPI di background thread
    server = threading.Thread(target=_run_server, daemon=True)
    server.start()

    # ─────────────────────────────────────────────────────────────
    # Jika di cloud (Railway), WebView tidak akan jalan—Rails
    # akan memanggil Procfile "web: uvicorn app.api:app ..." saja.
    # Baris berikut hanya untuk testing lokal.
    # ─────────────────────────────────────────────────────────────
    try:
        webview.create_window(
            title="GPS Transmitter",
            url=f"http://0.0.0.0:{os.getenv('PORT', 8000)}",
            width=800,
            height=600,
            resizable=True
        )
        webview.start()
    except Exception:
        # Jika WebView gagal (di environment tanpa GUI), abaikan
        pass
