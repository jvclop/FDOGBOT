import os
import asyncio
import requests
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotSettings
from aiohttp import web

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotSettings(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# Comando /start
@router.message(commands=["start"])
async def start_handler(message: Message):
    await message.answer("🐶 ¡Bienvenido al bot oficial de $FDOG!\nEscribe /price para ver el precio actual.")

# Comando /price
@router.message(commands=["price"])
async def price_handler(message: Message):
    try:
        token_address = "78Csm5Dc2hQxqzVAe7TQ81bcNiAKc5ALxiJPZSTgpump"
        url = f"https://client-api.pump.fun/token/{token_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()

        if not data.get("priceUsd"):
            await message.answer("❗ El token aún no tiene datos de precio. Intenta más tarde.")
            return

        price = float(data["priceUsd"])
        cap = float(data["marketCapUsd"])
        holders = data.get("holderCount", "N/A")

        reply = (
            f"💰 Precio de $FDOG: ${price:.6f}\n"
            f"📈 Market Cap: ${cap:,.0f}\n"
            f"👥 Holders: {holders}\n"
            f"🔗 https://pump.fun/coin/{token_address}"
        )
        await message.answer(reply)

    except Exception as e:
        await message.answer(f"❗ Error obteniendo el precio:\n<code>{e}</code>")

# Servidor web para Render
async def handle(request):
    return web.Response(text="Bot $FDOG activo")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8000)))
    await site.start()

# Lanzamiento del bot y servidor web
async def main():
    await start_web()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
