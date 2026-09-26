import urllib.request
import json
from datetime import datetime

print("====================================", flush=True)
print("INDODAX API CONNECTION TEST", flush=True)
print("====================================", flush=True)

url = "https://indodax.com/api/btc_idr/ticker"

try:
    with urllib.request.urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    ticker = data["ticker"]

    print("KONEKSI INDODAX BERHASIL", flush=True)
    print("Waktu :", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
    print("BTC/IDR", flush=True)
    print("Last  :", ticker["last"], flush=True)
    print("Buy   :", ticker["buy"], flush=True)
    print("Sell  :", ticker["sell"], flush=True)
    print("High  :", ticker["high"], flush=True)
    print("Low   :", ticker["low"], flush=True)
    print("Vol   :", ticker["vol_btc"], flush=True)

except Exception as e:
    print("KONEKSI INDODAX GAGAL", flush=True)
    print("ERROR:", str(e), flush=True)
    raise

print("====================================", flush=True)
print("TEST INDODAX SELESAI", flush=True)
print("====================================", flush=True)
