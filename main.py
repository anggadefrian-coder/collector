import time
from datetime import datetime

print("==============================")
print("INDODAX COLLECTOR TEST")
print("PYTHON BERJALAN DI GITHUB CLOUD")
print("==============================")

for i in range(3):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"COLLECTOR AKTIF | Percobaan {i + 1} | {waktu}")
    time.sleep(10)

print("==============================")
print("TEST SELESAI")
print("==============================")
