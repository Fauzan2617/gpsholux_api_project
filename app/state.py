# app/state.py
from threading import Lock

# State GPS awal
_gps_state = {
    "timestamp": "",
    "latitude":  0.0,
    "longitude": 0.0,
    "altitude":  0.0,
    "speed":     0.0,
    "heading":   0.0,
}
_lock = Lock()

def get_gps_state() -> dict:
    with _lock:
        return _gps_state.copy()

def update_gps_state(data: dict):
    with _lock:
        _gps_state.update({
            "timestamp": data.get("timestamp", ""),
            "latitude":  data.get("latitude", 0.0),
            "longitude": data.get("longitude", 0.0),
            "altitude":  data.get("altitude", 0.0),
            "speed":     data.get("speed", 0.0),
            "heading":   data.get("heading", 0.0),
        })
