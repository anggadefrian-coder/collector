import urllib.request
import json
from datetime import datetime

print("====================================", flush=True)
print("INDODAX API TEST", flush=True)
print("====================================", flush=True)

url = "https://indodax.com/api/btc_idr/ticker"

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(req, timeout=15) as response:
        print("HTTP STATUS:", response.status, flush=True)

        data = json.loads(response.read().decode("utf-8"))
        ticker = data["ticker"]

        print("KONEKSI INDODAX BERHASIL", flush=True)
        print("Waktu :", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
        print("Last  :", ticker["last"], flush=True)
        print("Buy   :", ticker["buy"], flush=True)
        print("Sell  :", ticker["sell"], flush=True)
        print("High  :", ticker["high"], flush=True)
        print("Low   :", ticker["low"], flush=True)
        print("Vol   :", ticker["vol_btc"], flush=True)

except Exception as e:
    print("KONEKSI INDODAX GAGAL", flush=True)
    print("ERROR:", repr(e), flush=True)

print("====================================", flush=True)
print("TEST SELESAI", flush=True)
print("====================================", flush=True)
