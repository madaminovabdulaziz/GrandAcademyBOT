from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="โ Test qo'shish"),
            KeyboardButton(text="๐ Test tekshirish")
        ],

        [
            KeyboardButton(text="๐ Mening ma'lumotlarim")
        ],
        [
            KeyboardButton(text="๐Reyting ko'rish")
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)
