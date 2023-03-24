from keyboards.default.main_menu import main_menu
from loader import db, dp
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.main_state import Main


@dp.message_handler(text="📊Reyting ko'rish", state=Main.main_menu)
async def showRatingToUsers(message: Message, state: FSMContext):
    await message.answer("Iltimos, test ID-ni kiriting!")
    await state.set_state("getTESTIDUser")

home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
home_btn.add("🏡 Bosh menyu")


@dp.message_handler(state="getTESTIDUser")
async def showF(message: Message, state: FSMContext):
    test_id = message.text
    test_bor = await db.get_test_by_id(test_id)
    if test_bor:
        subject = await db.get_test_name(test_id)
        rating = await db.show_rating_by_user(test_id)
        show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
        i = 1
        for user in rating:
            show_rating += "{0}) {1} - {2} ball, {3}\n".format(i, user['full_name'], user['ball'], user['created_time'])
            i += 1

        await message.answer(show_rating)
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()

    else:
        await message.answer("Afsuski bu test bazadan topilmadi, qayta kiriting!", reply_markup=ReplyKeyboardRemove())
        return

