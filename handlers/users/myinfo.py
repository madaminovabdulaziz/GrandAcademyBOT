from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.default.main_menu import main_menu
from keyboards.default.telefon import phone_btn
from loader import db, dp
from states.main_state import Main
from aiogram.dispatcher import FSMContext
from .texts import show_infor, show_infor_updated

change_mrkp = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_mrkp.add("🔀 Ismni o'zgartirish")
change_mrkp.add("🔀 Telefon raqamni o'zgartirish")
change_mrkp.add("🏡 Bosh menyu")


@dp.message_handler(text="/mydata", state="*")
async def show_c_data(message: Message, state: FSMContext):
    name = await db.getUser_name(message.from_user.id)
    phone = await db.getUser_phone(message.from_user.id)
    await message.answer(show_infor(name, phone), reply_markup=change_mrkp)
    await state.set_state("change_info")


this_btn = ["🔀 Ismni o'zgartirish", "🔀 Telefon raqamni o'zgartirish", "🏡 Bosh menyu"]
@dp.message_handler(text="📁 Mening ma'lumotlarim", state=Main.main_menu)
async def show_info(message: Message, state: FSMContext):
    name = await db.getUser_name(message.from_user.id)
    phone = await db.getUser_phone(message.from_user.id)
    await message.answer(show_infor(name, phone), reply_markup=change_mrkp)
    await state.set_state("change_info")


@dp.message_handler(text=this_btn, state="change_info")
async def change_them(message: Message, state: FSMContext):
    option = message.text
    if option == this_btn[2]:
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()
    elif option == this_btn[0]:
        await message.answer("Iltimos, ismingizni kiriting:\n\nMisol: <b>Aziz Azizov</b>")
        await state.set_state("cname")
    elif option == this_btn[1]:
        await message.answer("Telefon raqamingizni yuboring!\n\n +998 XX XXXXXXX formatida yuboring!\nMisol: 902777877")
        await state.set_state("cphone")



@dp.message_handler(state="cname")
async def change_name(message: Message, state: FSMContext):
    name = message.text
    await db.update_user_name(message.from_user.id, name)
    name = await db.getUser_name(message.from_user.id)
    phone = await db.getUser_phone(message.from_user.id)
    await message.answer(show_infor_updated(name, phone), reply_markup=change_mrkp)
    await state.set_state("change_info")





@dp.message_handler(state="cphone")
async def change_name(message: Message, state: FSMContext):
    phone = message.text
    if len(phone) == 9:
        await db.update_user_phone(message.from_user.id, phone)
        name = await db.getUser_name(message.from_user.id)
        phone = await db.getUser_phone(message.from_user.id)
        await message.answer(show_infor_updated(name, phone), reply_markup=change_mrkp)
        await state.set_state("change_info")
    else:
        await message.answer("Qayta kiriting!\n\nMisol: 902777877")
        return



