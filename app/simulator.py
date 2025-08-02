# app/simulator.py
import threading
import time
import requests
import serial
import pynmea2
from datetime import datetime, timezone

SERVER_URL   = "http://127.0.0.1:8000/update"
SERIAL_PORT  = "COM6"    # sesuaikan kalau port-mu berbeda
BAUDRATE     = 4800      # umumnya GPS NMEA default 4800 bps

def _simulate():
    print("[GPS Simulator] Membuka port serial", SERIAL_PORT)
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    except serial.SerialException as e:
        print("[GPS Simulator] Gagal buka serial:", e)
        return

    last_alt = 0.0
    while True:
        try:
            raw = ser.readline().decode("ascii", errors="ignore").strip()
            if not raw.startswith("$"):
                continue

            msg = pynmea2.parse(raw)

            # GGA → update altitude
            if isinstance(msg, pynmea2.types.talker.GGA):
                try:
                    last_alt = float(msg.altitude)
                except (ValueError, TypeError):
                    pass

            # RMC → paket utama: lat/lon/speed/course
            if isinstance(msg, pynmea2.types.talker.RMC) and msg.status == "A":
                data = {
                    "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc)
                                           .isoformat(),
                    "latitude":  msg.latitude,
                    "longitude": msg.longitude,
                    "altitude":  last_alt,
                    # spd_over_grnd dalam knot → km/h = *1.852
                    "speed":     round(float(msg.spd_over_grnd or 0) * 1.852, 2),
                    "heading":   float(msg.true_course or 0.0),
                }

                # kirim ke server
                res = requests.post(SERVER_URL, json=data, timeout=5)
                print(f"→ {res.status_code} | {data}")

            time.sleep(0.1)

        except pynmea2.ParseError:
            # parsing gagal, skip
            continue
        except Exception as e:
            print("[Simulator error]", e)
            time.sleep(1)

def start_simulator():
    t = threading.Thread(target=_simulate, daemon=True)
    t.start()
