import urllib.request
import json
import csv
import os
import subprocess
import time
from datetime import datetime
from zoneinfo import ZoneInfo

CSV_FILE = "data/btc_idr_15m.csv"

print("====================================", flush=True)
print("INDODAX BTC/IDR OHLC 15M COLLECTOR", flush=True)
print("====================================", flush=True)

try:
    # Git config
    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"],
        check=True
    )
    subprocess.run(
        [
            "git", "config", "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com"
        ],
        check=True
    )

    # Sinkronisasi repository
    print("SINKRONISASI DENGAN GITHUB...", flush=True)
    subprocess.run(
        ["git", "pull", "--rebase", "origin", "main"],
        check=True
    )

    # Ambil OHLC sekitar 2 jam terakhir
    now = int(time.time())
    start = now - (2 * 60 * 60)

    url = (
        "https://indodax.com/tradingview/history_v2"
        f"?from={start}&symbol=BTCIDR&tf=15&to={now}"
    )

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        print("HTTP STATUS:", response.status, flush=True)
        candles = json.loads(response.read().decode("utf-8"))

    if not isinstance(candles, list):
        raise Exception(f"Format data tidak sesuai: {candles}")

    os.makedirs("data", exist_ok=True)

    # Baca timestamp candle yang sudah tersimpan
    existing = set()

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row["unix_time"])

    rows_baru = []

    for candle in candles:
        unix_time = str(candle["Time"])

        # Jangan simpan candle duplikat
        if unix_time in existing:
            continue

        waktu = datetime.fromtimestamp(
            candle["Time"],
            ZoneInfo("Asia/Jakarta")
        ).strftime("%Y-%m-%d %H:%M:%S")

        rows_baru.append([
            unix_time,
            waktu,
            candle["Open"],
            candle["High"],
            candle["Low"],
            candle["Close"],
            candle["Volume"]
        ])

    # Urutkan candle berdasarkan waktu
    rows_baru.sort(key=lambda x: int(x[0]))

    file_baru = not os.path.exists(CSV_FILE)

    if rows_baru:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if file_baru:
                writer.writerow([
                    "unix_time",
                    "timestamp_wib",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume"
                ])

            writer.writerows(rows_baru)

        print(
            f"{len(rows_baru)} CANDLE BARU TERSIMPAN",
            flush=True
        )

        print("CANDLE TERAKHIR:", rows_baru[-1], flush=True)

        # Push ke GitHub
        subprocess.run(["git", "add", CSV_FILE], check=True)

        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"]
        )

        if result.returncode != 0:
            subprocess.run(
                [
                    "git", "commit", "-m",
                    "collector: simpan OHLC BTC/IDR 15m"
                ],
                check=True
            )

            subprocess.run(
                ["git", "push", "origin", "main"],
                check=True
            )

            print(
                "OHLC BERHASIL DI-PUSH KE GITHUB",
                flush=True
            )

    else:
        print("TIDAK ADA CANDLE BARU", flush=True)

except Exception as e:
    print("OHLC COLLECTOR GAGAL", flush=True)
    print("ERROR:", repr(e), flush=True)
    raise

print("====================================", flush=True)
print("OHLC COLLECTOR SELESAI", flush=True)
print("====================================", flush=True)
