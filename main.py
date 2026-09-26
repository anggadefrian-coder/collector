import time
from datetime import datetime

print("==============================", flush=True)
print("INDODAX COLLECTOR TEST", flush=True)
print("PYTHON BERJALAN DI GITHUB CLOUD", flush=True)
print("==============================", flush=True)

for i in range(3):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"COLLECTOR AKTIF | Percobaan {i + 1} | {waktu}", flush=True)
    time.sleep(10)

print("==============================", flush=True)
print("TEST SELESAI", flush=True)
print("==============================", flush=True)
