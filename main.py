import os
import requests
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from aiohttp import web
import asyncio

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("🐶 ¡Bienvenido al bot oficial de $FDOG!\nEscribe /price para ver el precio actual.")

@dp.message_handler(commands=["price"])
async def price(msg: types.Message):
    try:
        token_address = "78Csm5Dc2hQxqzVAe7TQ81bcNiAKc5ALxiJPZSTgpump"
        url = f"https://client-api.pump.fun/token/{token_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        data = resp.json()

        if "priceUsd" not in data or data["priceUsd"] is None:
            await msg.reply("❗ El token aún no tiene datos de precio. Intenta más tarde.")
            return

        price_usd = float(data["priceUsd"])
        market_cap = float(data["marketCapUsd"])
        holders = data.get("holderCount", "N/A")

        response = (
            f"💰 Precio actual de $FDOG: ${price_usd:.6f}\n"
            f"📈 Market Cap: ${market_cap:,.0f}\n"
            f"👥 Holders: {holders}\n"
            f"🔗 Ver: https://pump.fun/coin/{token_address}"
        )
        await msg.reply(response)

    except Exception as e:
        await msg.reply(f"❗ Error obteniendo el precio:\n`{e}`")

# Servidor web para que Render no apague la app
async def handle(request):
    return web.Response(text="Bot $FDOG funcionando!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_app():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8000)))
    await site.start()

loop = asyncio.get_event_loop()
loop.create_task(start_web_app())

if __name__ == "__main__":
    executor.start_polling(dp)
