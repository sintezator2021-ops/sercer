from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

# TOKEN твого Telegram-бота
TOKEN = "8240464361:AAHB1ZBediNF3xN5gg23MwVzIohTyTteAl4"

# Список ID отримувачів
CHAT_IDS = [947916210]

# Створення сесії та бота
session = AiohttpSession()
bot = Bot(TOKEN, session=session)

app = FastAPI()

# Дозволяємо запити з будь-якого сайту (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Маршрут прийому замовлень
@app.post("/order")
async def order(
    name: str = Form(...),
    phone: str = Form(...),
    product: str = Form("кільця"),
):
    text = (
        "Нове замовлення:\n"
        f"Товар: {product}\n"
        f"Ім'я: {name}\n"
        f"Телефон: {phone}"
    )

    # Розсилка всім отримувачам
    for cid in CHAT_IDS:
        await bot.send_message(cid, text)

    return {"status": "ok"}

# Закриття сесії при завершенні роботи сервера
@app.on_event("shutdown")
async def shutdown():
    await bot.session.close()

# Локальний запуск (Render це ігнорує)
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)

