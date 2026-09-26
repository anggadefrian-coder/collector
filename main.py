import urllib.request
import json
import csv
import os
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================
# KONFIGURASI
# ==========================================

URL = "https://indodax.com/api/btc_idr/ticker"
CSV_FILE = "data/btc_idr_ticker.csv"

# ==========================================
# HEADER
# ==========================================

print("====================================", flush=True)
print("INDODAX BTC/IDR COLLECTOR", flush=True)
print("====================================", flush=True)

# ==========================================
# AMBIL DATA INDODAX
# ==========================================

req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(req, timeout=15) as response:

        print("HTTP STATUS:", response.status, flush=True)

        data = json.loads(
            response.read().decode("utf-8")
        )

    ticker = data["ticker"]

    # ======================================
    # WAKTU WIB
    # ======================================

    waktu = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%Y-%m-%d %H:%M:%S")

    # ======================================
    # DATA
    # ======================================

    last = ticker["last"]
    buy = ticker["buy"]
    sell = ticker["sell"]
    high = ticker["high"]
    low = ticker["low"]
    volume = ticker["vol_btc"]

    print("KONEKSI INDODAX BERHASIL", flush=True)
    print("Waktu :", waktu, flush=True)
    print("BTC/IDR", flush=True)
    print("Last  :", last, flush=True)
    print("Buy   :", buy, flush=True)
    print("Sell  :", sell, flush=True)
    print("High  :", high, flush=True)
    print("Low   :", low, flush=True)
    print("Vol   :", volume, flush=True)

    # ======================================
    # BUAT FOLDER DATA
    # ======================================

    os.makedirs("data", exist_ok=True)

    # ======================================
    # CEK FILE CSV
    # ======================================

    file_baru = not os.path.exists(CSV_FILE)

    # ======================================
    # SIMPAN DATA
    # ======================================

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        if file_baru:
            writer.writerow([
                "timestamp",
                "last",
                "buy",
                "sell",
                "high",
                "low",
                "volume_btc"
            ])

        writer.writerow([
            waktu,
            last,
            buy,
            sell,
            high,
            low,
            volume
        ])

    print("DATA TERSIMPAN:", CSV_FILE, flush=True)

    # ======================================
    # SIMPAN KE GITHUB
    # ======================================

    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"],
        check=True
    )

    subprocess.run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com"
        ],
        check=True
    )

    subprocess.run(
        ["git", "add", CSV_FILE],
        check=True
    )

    # Cek apakah ada perubahan
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )

    if result.returncode != 0:

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "collector: simpan data BTC/IDR"
            ],
            check=True
        )

        subprocess.run(
            ["git", "push"],
            check=True
        )

        print("DATA BERHASIL DI-PUSH KE GITHUB", flush=True)

    else:
        print("TIDAK ADA DATA BARU UNTUK DI-COMMIT", flush=True)

except Exception as e:

    print("COLLECTOR GAGAL", flush=True)
    print("ERROR:", repr(e), flush=True)
    raise

print("====================================", flush=True)
print("COLLECTOR SELESAI", flush=True)
print("====================================", flush=True)
