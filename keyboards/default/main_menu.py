from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Test qo'shish"),
            KeyboardButton(text="✅ Test tekshirish")
        ],

        [
            KeyboardButton(text="📁 Mening ma'lumotlarim")
        ],
        [
            KeyboardButton(text="📊Reyting ko'rish")
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)