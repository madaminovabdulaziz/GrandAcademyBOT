import logging
from keyboards.default.telefon import phone_btn
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message, ReplyKeyboardMarkup
from keyboards.default.main_menu import main_menu
from keyboards.inline.subs import the_btn
from data.config import CHANNELS
from loader import dp, db, bot
from states.main_state import Main
from utils.misc import subscription

role_mrkp = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
role_mrkp.add("Prezident maktab o'quvchisi")
role_mrkp.add("Abiturient")
role_mrkp.add("Bulardan hech biri emas")

roles_list = ["Prezident maktab o'quvchisi", "Abiturient", "Bulardan hech biri emas"]

@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Message, state: FSMContext):
    is_User = await db.select_user(message.from_user.id)
    if is_User is None:
        channels_format = str()
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channels_format += f"<b>👉 <a href='{invite_link}'>{chat.title}</a></b>\n"
            await message.answer(f"😊 Assalomu alaykum!\n\nBotdan foydalanish uchun quyidagi kanalga obuna bo'ling!👇\n",
                                 reply_markup=the_btn, disable_web_page_preview=True)
            await state.set_state("is_sbs")

    else:
        for channel in CHANNELS:
            result = str()
            status = await subscription.check(user_id=message.from_user.id, channel=channel)
            channel = await bot.get_chat(channel)

            if status:
                await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                await Main.main_menu.set()
            else:
                is_User = await db.select_user(message.from_user.id)
                if is_User is None:
                    try:
                        user = await db.add_user(telegram_id=message.from_user.id,
                                                 full_name=message.from_user.full_name,
                                                 username=message.from_user.username,
                                                 )

                    except asyncpg.exceptions.UniqueViolationError:
                        pass
                    result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")

                    await state.set_state("is_sbs")
                else:
                    result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")

                    await Main.sbs.set()

            try:
                await message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
            except:
                pass


@dp.callback_query_handler(text="check", state="is_sbs")
async def checker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)

        if status:
            await call.message.answer(f"""

😊<b>Hurmatli foydalanuvchi!</b>
Kanalimiz obunachilari safida bo'lganingizdan minnatdormiz!
            """)
            await call.message.answer("""
<b>☑️ Ro'yxatdan o'ting!</b>
----------------------------

Iltimos, ism, familiyangizni kiriting:\n\nMisol: <b>Aziz Azizov</b>""", reply_markup=ReplyKeyboardRemove())
            await state.set_state("not_user")

        else:

            result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")
            await state.set_state("is_sbs")
    try:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
    except:
        pass


@dp.message_handler(state="not_user")
async def get_name(message: types.Message, state: FSMContext):
    ism = str(message.text)
    await db.update_user_name(message.from_user.id, ism)
    await message.answer("Telefon raqamingizni yuboring!", reply_markup=phone_btn)
    await state.set_state("phone")


@dp.message_handler(state="phone", content_types=types.ContentType.CONTACT)
async def get_user_phone(message: Message, state: FSMContext):
    number = message.contact.phone_number
    number = str(number)
    await db.update_user_phone(message.from_user.id, number)
    await message.answer("Tanlang ⬇️", reply_markup=role_mrkp)
    await state.set_state("role")



@dp.message_handler(text=roles_list, state="role")
async def check_role(message: Message, state: FSMContext):
    role = message.text
    if role == roles_list[0]:
        await db.update_role("p_school", message.from_user.id)
    elif role == roles_list[1]:
        await db.update_role("abitur", message.from_user.id)
    elif role == roles_list[2]:
        await db.update_role("random", message.from_user.id)
    else:
        await message.answer("Xatolik!\nQayta kiriting!", reply_markup=role_mrkp)
        return
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username,
                                 )

    except asyncpg.exceptions.UniqueViolationError:
        pass
    await message.answer("Siz ro'yxatdan o'tdingiz!")
    await message.answer("🏡 Bosh menyu:", reply_markup=main_menu)
    await Main.main_menu.set()

@dp.callback_query_handler(text="check", state=Main.sbs)
async def checker(call: CallbackQuery, state: FSMContext):
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)

        if status:
            await call.message.answer("🏡 Bosh menyu:", reply_markup=main_menu)
            await Main.main_menu.set()
        else:
            result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")
            await Main.sbs.set()

    try:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
    except:
        pass


