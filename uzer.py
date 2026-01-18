import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
TOKEN = "8438208241:AAGfSqyeOzzLfuKulRHD7uHfRLc8eOiXwtI"
ADMIN_ID = 123456789  # Твой ID (узнай в @userinfobot)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# База данных в памяти
user_data = {} # {id: {"balance": 0, "banned": False}}
prices = {"spam": 10, "dox": 50, "snos": 100}

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_u(uid):
    if uid not in user_data:
        user_data[uid] = {"balance": 1000, "banned": False}
    return user_data[uid]

# --- КОМАНДЫ ПРАНКА И АНИМАЦИИ ---

@dp.message(Command("dox"))
async def cmd_dox(message: types.Message):
    msg = await message.answer("📡 Подключение к базе данных...")
    await asyncio.sleep(1)
    await msg.edit_text("🔍 Поиск по лицу и геолокации...")
    await asyncio.sleep(1.5)
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.1"
    res = (f"❌ **ДОКС ДАННЫЕ** ❌\n"
           f"📍 IP: `{ip}`\n"
           f"🏠 Адрес: г. Москва, ул. Большая, д. {random.randint(1,100)}\n"
           f"📱 Номер: +7 (9{random.randint(10,99)}) {random.randint(100,999)}-01-02\n"
           f"🌐 Провайдер: Starlink / MGTS\n"
           f"🔐 Пароли: `qwerty123`, `admin777`")
    await msg.edit_text(res, parse_mode="Markdown")

@dp.message(Command("snos"))
async def cmd_snos(message: types.Message):
    msg = await message.answer("⚠️ Инициация удаления аккаунта...")
    await asyncio.sleep(1)
    for i in range(20, 101, 20):
        await msg.edit_text(f"📡 Отправка пакетов деструкции: {i}%")
        await asyncio.sleep(0.5)
    await msg.edit_text("🚫 **АККАУНТ УДАЛЕН.**\nСессия будет завершена в течение 5 минут.")

@dp.message(Command("type"))
async def cmd_type(message: types.Message):
    text = message.text.replace("/type ", "")
    if not text: return
    msg = await message.answer("▒")
    current = ""
    for char in text:
        current += char
        await msg.edit_text(current + "▒")
        await asyncio.sleep(0.1)
    await msg.edit_text(current)

# --- СПАМ КОМАНДЫ ---

@dp.message(Command("sp"))
async def cmd_sp(message: types.Message):
    try:
        args = message.text.split()
        text = args[1].replace("_", " ")
        count = int(args[2])
        for _ in range(min(count, 50)):
            await message.answer(text)
            await asyncio.sleep(0.5)
               except: await message.answer("Используй: `/sp текст_с_подчеркиванием 10`", parse_mode="Markdown")

@dp.message(Command("dspam"))
async def cmd_dspam(message: types.Message):
    try:
        args = message.text.split()
        count = int(args[1])
        text = " ".join(args[2:])
        for _ in range(min(count, 50)):
            m = await message.answer(text)
            await asyncio.sleep(0.1)
            await m.delete()
    except: pass

# --- КРИПТО И ЧЕКИ ---

@dp.message(Command("send"))
async def cmd_send(message: types.Message):
    args = message.text.split()
    if len(args) < 3: return
    cur, amo = args[1], args[2]
    await message.answer(f"💎 **Крипто-чек создан!**\n\nСумма: `{amo} {cur}`\nСтатус: `Активен`\n\n[Забрать чек](https://t.me/CryptoBot?start=fake)", parse_mode="Markdown")

# --- УТИЛИТЫ ---

@dp.message(Command("calc"))
async def cmd_calc(message: types.Message):
    try:
        res = eval(message.text.replace("/calc ", ""))
        await message.answer(f"🔢 Результат: `{res}`", parse_mode="Markdown")
    except: await message.answer("Ошибка в примере")

@dp.message(Command("reverse"))
async def cmd_rev(message: types.Message):
    t = message.text.replace("/reverse ", "")
    await message.answer(t[::-1])

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    u = get_u(message.from_user.id)
    await message.answer(f"👤 **Твой профиль:**\n\n💰 Баланс: `{u['balance']}` ⭐\n🆔 ID: `{message.from_user.id}`", parse_mode="Markdown")

# --- АДМИН МЕНЮ ---

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Изменить баланс", callback_data="adm_stars")],
        [InlineKeyboardButton(text="🚫 Бан пользователя", callback_data="adm_ban")],
        [InlineKeyboardButton(text="📈 Цены", callback_data="adm_prices")]
    ])
    await message.answer("⚙️ **Админ-панель:**", reply_markup=kb)

# --- ИГРЫ ---
@dp.message(Command("duel"))
async def cmd_duel(message: types.Message):
    await message.answer("🔫 Стреляю...")
    await asyncio.sleep(1)
    await message.answer(random.choice(["💀 Ты проиграл!", "🎉 Осечка! Ты жив."]))

# Запуск
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
