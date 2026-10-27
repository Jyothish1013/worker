import requests
import random
import time
import math

SERVER_URL = "https://wifi-enabled-smart-band.onrender.com/data"

def generate_motion():
    # Generate realistic ESP32-like acceleration values
    ax = round(random.uniform(0.5, 4.0), 2)
    ay = round(random.uniform(0.5, 4.0), 2)
    az = round(random.uniform(0.5, 4.0), 2)

    # Compute magnitude (overall G)
    overall = round(math.sqrt(ax*ax + ay*ay + az*az), 2)

    return ax, ay, az, overall

def generate_remote_motion():
    # Remote node (WRIST)
    ax = round(random.uniform(0.5, 4.0), 2)
    ay = round(random.uniform(0.5, 4.0), 2)
    az = round(random.uniform(0.5, 4.0), 2)

    overall = round(math.sqrt(ax*ax + ay*ay + az*az), 2)

    return ax, ay, az, overall

def generate_alarm(local_g, remote_g):
    # Alarm logic similar to ESP32
    return 1 if (local_g >= 2.5 or remote_g >= 2.5) else 0

while True:
    # Generate local motion
    lx, ly, lz, lg = generate_motion()

    # Generate remote motion
    rx, ry, rz, rg = generate_remote_motion()

    # Alarm logic
    alarm = generate_alarm(lg, rg)

    # Build JSON exactly like your ESP32 cloudTask()
    payload = {
        "ax": lx,
        "ay": ly,
        "az": lz,
        "total_g": lg,
        "remote": {
            "ax": rx,
            "ay": ry,
            "az": rz,
            "overall": rg
        },
        "alarm": alarm,
        "timestamp": int(time.time() * 1000)
    }

    print("\nSending simulated data:")
    print(payload)

    try:
        response = requests.post(SERVER_URL, json=payload)
        print("Server Response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)

    time.sleep(1)
