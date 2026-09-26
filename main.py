import time
from datetime import datetime

print("================================")
print("INDODAX COLLECTOR AKTIF")
print("PYTHON BERJALAN DI GITHUB CLOUD")
print("================================")

while True:
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"COLLECTOR AKTIF | {waktu}")
    time.sleep(60)
