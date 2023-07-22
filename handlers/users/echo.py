from aiogram import types
import textwrap
from loader import dp, db
from data.config import ADMINS


# Echo bot
@dp.message_handler(commands=['users'], state="*", chat_id=ADMINS)
async def bot_echo(message: types.Message):


    users = await db.get_all_users()

    i = 1
    data = "<b>BARCHA FOYDALUVCHILAR\n\n\n</b>"
    max_message_length = 4096  # Adjust this value based on the maximum message length allowed by your messaging platform

    for user in users:
        data += "{0}) {1} - {2} - @{3} - {4} - <b>☎️ Tel: </b>{5}\n".format(i, user['id'], user['full_name'], user['username'],
                                                            user['telegram_id'], user['phone'])
        i += 1

    # Split the data into smaller chunks using textwrap
    data_chunks = textwrap.wrap(data, width=max_message_length, replace_whitespace=False)

    # Send each chunk as a separate message
    for chunk in data_chunks:
        await message.answer(chunk)

