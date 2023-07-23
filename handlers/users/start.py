import logging

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
    logging.info("Received /start command")
    is_User = await db.select_user(message.from_user.id)
    if is_User is None:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username,
                                     )

        except asyncpg.exceptions.UniqueViolationError:
            pass

        payload = message.get_args()
        if payload.startswith("class_"):
            class_name = payload.split('_')[1]
            test_id = payload.split('_')[2]
            test_len = await db.get_test_length(test_id)

            await state.update_data(
                {"classname": class_name, "test_id": test_id, "testlen": test_len}
            )

        channels_format = str()
        for channel in CHANNELS:
            try:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                channels_format += f"<b>👉 <a href='{invite_link}'>{chat.title}</a></b>\n"
            except Exception as e:
                logging.error(f"Error getting chat {channel}: {e}")

        await message.answer(
            f"😊 Assalomu alaykum!\n\nBotdan foydalanish uchun quyidagi kanalga obuna bo'ling!👇\n",
            reply_markup=the_btn,
            disable_web_page_preview=True
        )
        await state.set_state("is_sbs")
    else:
        for channel in CHANNELS:
            result = str()
            try:
                status = await subscription.check(user_id=message.from_user.id, channel=channel)
                channel = await bot.get_chat(channel)

                if status:
                    payload = message.get_args()
                    if payload.startswith("class_"):
                        class_name = payload.split('_')[1]
                        test_id = payload.split('_')[2]
                        test_len = await db.get_test_length(test_id)
                        text = f"""
    ✅ Test boshlandi.

    📔 Sinf: {class_name}
    🔑 Test kodi: {test_id}
    📝 Savollar soni: {test_len}

    Javobingizni quyidagi ko'rinishda yuborishingiz mumkin:
    {test_id}*abcdabcd...
    yoki
    {test_id}*1a2b3c4d5a...

                        """
                        await message.answer(text, reply_markup=ReplyKeyboardRemove())
                        await state.set_state("next_step1")
                    else:
                        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                        await Main.main_menu.set()

                else:
                    result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")
                    await state.set_state("is_sbs")
            except Exception as e:
                logging.error(f"Error checking channel {channel}: {e}")

            try:
                await message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
            except:
                pass


@dp.callback_query_handler(text="check", state="is_sbs")
async def checker_callback(call: CallbackQuery, state: FSMContext):
    await call.answer()
    logging.info("Received callback query: check")
    result = str()
    for channel in CHANNELS:
        try:
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
        except Exception as e:
            logging.error(f"Error checking channel {channel}: {e}")

    try:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
    except:
        pass


@dp.message_handler(state="not_user")
async def get_name(message: types.Message, state: FSMContext):
    ism = str(message.text)
    await db.update_user_name(message.from_user.id, ism)
    await message.answer("Telefon raqamingizni +998 ** ******* formatida yuboring!\n\nMisol 901234567")
    await state.set_state("phone")


@dp.message_handler(state="phone")
async def get_user_phone(message: Message, state: FSMContext):
    number = message.text
    if number.isdigit() and len(number) == 9:
        number = str(number)
        await db.update_user_phone(message.from_user.id, number)
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username,
                                     )
        except asyncpg.exceptions.UniqueViolationError:
            pass
        await message.answer("Siz ro'yxatdan o'tdingiz!")
        data = await state.get_data()
        class_name = data.get('classname')
        test_id = data.get("test_id")
        length = data.get('testlen')
        if class_name is None:
            await message.answer("🏡 Bosh menyu:", reply_markup=main_menu)
            await Main.main_menu.set()
        else:
            text = f"""
✅ Test boshlandi.

📔 Sinf: {class_name}
🔑 Test kodi: {test_id}
📝 Savollar soni: {length}

Javobingizni quyidagi ko'rinishda yuborishingiz mumkin:
{test_id}*abcdabcd...
yoki
{test_id}*1a2b3c4d5a...
 """
            await message.answer(text, reply_markup=ReplyKeyboardRemove())
            await state.set_state("next_step1")

    else:
        await message.answer("Telefon raqamingizni +998 ** ******* formatida yuboring!\n\nMisol 901234567")


@dp.callback_query_handler(text="check", state=Main.sbs)
async def checker_callback(call: CallbackQuery, state: FSMContext):
    logging.info("Received callback query: check")
    result = str()
    for channel in CHANNELS:
        try:
            status = await subscription.check(user_id=call.from_user.id, channel=channel)
            channel = await bot.get_chat(channel)

            if status:
                await call.message.answer("🏡 Bosh menyu:", reply_markup=main_menu)
                await Main.main_menu.set()
            else:
                result += (f"❗️❗️❗️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz\n\nObuna bo'ling!")
                await Main.sbs.set()
        except Exception as e:
            logging.error(f"Error checking channel {channel}: {e}")

    try:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=the_btn)
    except:
        pass
