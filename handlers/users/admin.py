import re
import random

from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from handlers.users.texts import qoshish_yoriqnomasi, bazaga_qoshildi, add_PMTest, add_ATest
from keyboards.default.main_menu import main_menu
from loader import dp, db
from data.config import ADMINS
from states.main_state import Main

admin_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_btn.add("Block test qo'shish")
admin_btn.add("Test bo'yicha reytingni ko'rish")
admin_btn.add("Foydalanuvchilar sonini ko'rish")
admin_btn.add("🔙 Orqaga")


user_types_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_types_btn.add("PM o'quvchilariga")
user_types_btn.add("Abiturientlarga")
user_types_btn.add("🔙 Orqaga")

this_btn = ["Block test qo'shish", "Test bo'yicha reytingni ko'rish", "🔙 Orqaga", "Foydalanuvchilar sonini ko'rish"]
this_btn_2 = ["PM o'quvchilariga", "Abiturientlarga", "🔙 Orqaga"]

@dp.message_handler(text="/admin", chat_id=ADMINS, state="*")
async def show_details(message: Message, state: FSMContext):
    await message.answer("😊 Admin panelga xush kelibsiz!", reply_markup=admin_btn)
    await state.set_state("first_step")

@dp.message_handler(text=this_btn, chat_id=ADMINS, state="first_step")
async def make_d(message: Message, state: FSMContext):
    if message.text == this_btn[0]:
        await message.answer("Kimlar uchun test qo'shmoqchisiz?", reply_markup=user_types_btn)
        await state.set_state("add_special")
    elif message.text == this_btn[1]:
        await message.answer("Test ID raqamini kiriting!")
        await state.set_state("defineID")
    elif message.text == this_btn[2]:
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()
    elif message.text == this_btn[3]:
        users = await db.count_users()
        await message.answer(f"""
Ayni payt botdan {users} kishi ro'yxatdan o'tgan

""")
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()



@dp.message_handler(text=this_btn_2, chat_id=ADMINS, state="add_special")
async def add_test_sp(message: Message, state: FSMContext):
    if message.text == this_btn_2[0]:
        await message.answer(add_PMTest())
        await state.set_state("getPMQuestions")

    elif message.text == this_btn_2[1]:
        await message.answer(add_ATest())
        await state.set_state("getABQuestions")

    elif message.text == this_btn_2[2]:
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()



@dp.message_handler(state="getPMQuestions")
async def addPMQ(message: Message, state: FSMContext):
    test_id = random.randint(0, 999999)
    full_answer = message.text
    if "*" in full_answer:
        where_is_star = full_answer.find("*")
        where_is_star = int(where_is_star)
        where_is_star += 1
        answers = full_answer[where_is_star:]
        where_is_star -= 1
        subject = full_answer[:where_is_star]
        user_answers = re.sub('[^a-zA-Z]+', '', answers)
        user_answers = user_answers.lower()
        length = len(user_answers)
        if answers.isdigit():
            await message.answer(add_PMTest(), reply_markup=ReplyKeyboardRemove())
            return
        #
        if len(user_answers) == 80:
            await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialPM")
            await message.answer(bazaga_qoshildi(test_id, user_answers))
            await message.answer("Kimlar uchun test qo'shmoqchisiz?", reply_markup=user_types_btn)
            await state.set_state("add_special")

        else:
            await message.answer(add_PMTest())
            return



@dp.message_handler(state="getABQuestions")
async def addPMQ(message: Message, state: FSMContext):
    test_id = random.randint(0, 999999)
    full_answer = message.text
    if "*" in full_answer:
        where_is_star = full_answer.find("*")
        where_is_star = int(where_is_star)
        where_is_star += 1
        answers = full_answer[where_is_star:]
        where_is_star -= 1
        subject = full_answer[:where_is_star]
        user_answers = re.sub('[^a-zA-Z]+', '', answers)
        user_answers = user_answers.lower()
        length = len(user_answers)
        if answers.isdigit():
            await message.answer(add_ATest(), reply_markup=ReplyKeyboardRemove())
            return
        #
        if len(user_answers) == 90:
            await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialA")
            await message.answer(bazaga_qoshildi(test_id, user_answers))
            await message.answer("Kimlar uchun test qo'shmoqchisiz?", reply_markup=user_types_btn)
            await state.set_state("add_special")

        else:
            await message.answer(add_ATest())
            return



@dp.message_handler(state="defineID")
async def define_them(message: Message, state: FSMContext):
    test_id = message.text
    if test_id.isdigit():
        is_test = await db.get_test_by_id(test_id)
        if is_test:
            subject = await db.get_test_name(test_id)
            rating = await db.show_rating_by_user(test_id)
            show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
            i = 1
            for user in rating:
                show_rating += "{0}) {1} - {2} ball\n".format(i, user['full_name'], user['ball'])
                i += 1

            await message.answer(show_rating)
            await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
            await Main.main_menu.set()
        else:
            await message.answer("Siz kiritgan ID bo'yicha test topilmadi!\nQayta kiriting!", reply_markup=ReplyKeyboardRemove())
            return
    else:
        await message.answer("TEST ID xato kiritilgan!\n Iltimos, qayta kiriting!", reply_markup=ReplyKeyboardRemove())
        return