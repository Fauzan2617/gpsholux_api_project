# app/api.py
import os, sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.state import get_gps_state, update_gps_state
from app.simulator import start_simulator  # tambahkan ini

# tentukan path seperti sebelumnya…
base_dir      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(base_dir, "templates")
static_dir    = os.path.join(base_dir, "static")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
 )

# Jalankan simulator saat server mulai
@app.on_event("startup")
def on_startup():
    start_simulator()

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gps")
def read_gps():
    return get_gps_state()

@app.post("/update")
async def update(data: dict):
    update_gps_state(data)
    return {"status": "ok"}
