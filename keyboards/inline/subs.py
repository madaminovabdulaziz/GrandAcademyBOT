from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


the_btn = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="GRAND Akademiyasi", url="https://t.me/grand_akademiyasi")
        ],
            [
                InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")
            ]

        ]
    )


