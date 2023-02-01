import re

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types.message import Message

from keyboards.default.main_menu import main_menu
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.main_state import Main
import random
from .texts import qoshish_yoriqnomasi, bazaga_qoshildi
from data.config import ADMINS


@dp.message_handler(text="➕ Test qo'shish", state=Main.main_menu)
async def fstep(message: Message, state: FSMContext):
    home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    home_btn.add("🏡 Bosh menyu")
    await message.answer(qoshish_yoriqnomasi(), reply_markup=home_btn)
    await state.set_state("second")



@dp.message_handler(state="second")
async def sstep(message: Message, state: FSMContext):
    test_id = random.randint(0, 999999)
    full_test = message.text
    if full_test == "🏡 Bosh menyu":
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()
    else:
        if "*" in full_test:
            where_is_star = full_test.find("*")
            where_is_star = int(where_is_star)
            where_is_star += 1

            answers = full_test[where_is_star:]
            if answers.isdigit():
                await message.answer(qoshish_yoriqnomasi(), reply_markup=ReplyKeyboardRemove())
                return
            else:
                pass

            where_is_star -= 1
            subject = full_test[:where_is_star]
            user_answers = re.sub('[^a-zA-Z]+', '', answers)
            user_answers = user_answers.lower()
            length = len(user_answers)
            await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "usual")
            await message.answer(bazaga_qoshildi(test_id, user_answers))
            await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
            await Main.main_menu.set()

        else:
            await message.answer(qoshish_yoriqnomasi(), reply_markup=ReplyKeyboardRemove())
            await state.set_state("second")
