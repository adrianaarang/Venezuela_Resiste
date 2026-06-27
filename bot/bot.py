"""
Venezuela Earthquake Aftershock Alert Bot
Consulta USGS cada 2 minutos y avisa en Telegram de réplicas nuevas.

SETUP local:
  pip install httpx
  Crea un archivo .env con las variables (ver .env.example)
  python bot.py

DEPLOY Railway:
  Sube la carpeta bot/ y añade las variables de entorno en Railway.
"""

import os
import asyncio
import httpx
from datetime import datetime, timezone
from pathlib import Path

# Carga .env si existe (local). En Railway las vars vienen del entorno directamente.
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ── CONFIG ────────────────────────────────────────────
TOKEN    = os.environ["TELEGRAM_TOKEN"]
CHAT_ID  = os.environ["TELEGRAM_CHAT"]
MIN_MAG  = float(os.getenv("MIN_MAG", "4.5"))
INTERVAL = 120  # segundos entre consultas

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_PARAMS = {
    "format":       "geojson",
    "starttime":    "2026-06-24",
    "minmagnitude": str(MIN_MAG),
    "latitude":     "10.5",
    "longitude":    "-68.0",
    "maxradiuskm":  "350",
    "orderby":      "time",
    "limit":        "20",
}

seen_ids: set[str] = set()

# ── EMOJI POR MAGNITUD ────────────────────────────────
def mag_emoji(mag: float) -> str:
    if mag >= 6.5: return "🔴"
    if mag >= 5.5: return "🟠"
    if mag >= 4.5: return "🟡"
    return "⚪"

# ── FORMATEAR MENSAJE ─────────────────────────────────
def build_message(feat: dict) -> str:
    props = feat["properties"]
    mag   = props["mag"]
    place = props.get("place", "Venezuela")
    ts    = props["time"] / 1000
    depth = feat["geometry"]["coordinates"][2]
    dt    = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%H:%M UTC")
    url   = props.get("url", "")

    emoji = mag_emoji(mag)
    lines = [
        f"{emoji} *RÉPLICA M{mag:.1f}*",
        f"📍 {place}",
        f"🕐 {dt}  |  🏔 Prof. {depth:.0f} km",
    ]
    if url:
        lines.append(f"[Ver en USGS]({url})")
    return "\n".join(lines)

# ── ENVIAR A TELEGRAM ─────────────────────────────────
async def send(client: httpx.AsyncClient, text: str):
    await client.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id":    CHAT_ID,
            "text":       text,
            "parse_mode": "Markdown",
        },
        timeout=10,
    )

# ── CONSULTAR USGS ────────────────────────────────────
async def poll(client: httpx.AsyncClient):
    global seen_ids
    try:
        r = await client.get(USGS_URL, params=USGS_PARAMS, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[USGS error] {e}")
        return

    new_events = [
        f for f in data["features"]
        if f["id"] not in seen_ids
    ]

    if not seen_ids:
        seen_ids = {f["id"] for f in data["features"]}
        print(f"[boot] {len(seen_ids)} eventos cargados, vigilando réplicas ≥ M{MIN_MAG}")
        return

    for feat in reversed(new_events):
        msg = build_message(feat)
        await send(client, msg)
        seen_ids.add(feat["id"])
        mag = feat["properties"]["mag"]
        print(f"[alerta] M{mag:.1f} → {feat['properties'].get('place','?')}")

# ── BUCLE PRINCIPAL ───────────────────────────────────
async def main():
    print(f"[start] Venezuela Avisos Bot · min M{MIN_MAG} · intervalo {INTERVAL}s")
    async with httpx.AsyncClient() as client:
        while True:
            await poll(client)
            await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
