from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types.message import Message
import re
from keyboards.default.main_menu import main_menu
from loader import dp, db
from aiogram.dispatcher import FSMContext
from states.main_state import Main
from datetime import date, datetime
from pytz import timezone
from .texts import javob_tekshirish, after_test_high, after_test_low, after_test_lowPM, after_test_highPM, \
    after_test_lowA, after_test_highA


@dp.message_handler(text="🔑 Test tekshirish", state=Main.main_menu)
async def check_fstep(message: Message, state: FSMContext):

    home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    home_btn.add("🏡 Bosh menyu")
    await message.answer(javob_tekshirish(), reply_markup=home_btn)
    await state.set_state("next_step1")


@dp.message_handler(state="next_step1")
async def check_sstep(message: Message, state: FSMContext):
    errors = 0
    full_answer = message.text
    if full_answer == "🏡 Bosh menyu":
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
        await Main.main_menu.set()
    else:
        if "*" in full_answer:
            where_is_star = full_answer.find("*")
            where_is_star = int(where_is_star)
            where_is_star += 1

            user_answers = full_answer[where_is_star:]
            user_answers = user_answers.lower()
            if user_answers.isdigit():
                await message.answer(javob_tekshirish(), reply_markup=ReplyKeyboardRemove())
                return
            else:
                pass

            where_is_star -= 1
            test_id = full_answer[:where_is_star]

            is_test_yes = await db.get_test_by_id(test_id)   
            if is_test_yes:
                test_id = int(test_id)
                test_type = await db.get_test_type(test_id)
                if test_type == "usual":
                    is_Done_before = await db.check_is_done(test_id, message.from_user.id)

                    if is_Done_before is None:
                        correct_answer = await db.get_test_answers(test_id)  # correct answers
                        user_answers = re.sub('[^a-zA-Z]+', '', user_answers)  # user answers
                        # count len of correct_answer and users answer and first check it
                        len1 = await db.get_test_length(test_id)
                        len2 = len(user_answers)
                        date_t = date.today()
                        date_t = str(date_t)

                        if len1 == len2:

                            await db.add_done_test(test_id, message.from_user.id, date_t)
                            for x, y in zip(correct_answer, user_answers):
                                if x == y:
                                    pass
                                else:
                                    errors += 1

                            name = await db.getUser_name(message.from_user.id)
                            subject = await db.get_test_name(test_id)
                            user_id = str(message.from_user.id)
                            test_code = test_id
                            questionLength = len(correct_answer)
                            userAnswers = len(correct_answer) - errors
                            percent = userAnswers / questionLength * 100
                            percent = round(percent)
                            time_format = '%Y-%m-%d %H:%M:%S'
                            test_id = str(test_id)
                            formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                            await db.add_rating(test_id, user_id, name, percent, formatted_now, "usual")
                            rating = await db.show_rating_by_user(test_id)
                            show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
                            i = 1
                            for user in rating:
                                show_rating += "{0}) {1} - {2} foiz\n".format(i, user['full_name'], user['ball'])
                                i += 1

                            show_rating += "\n\n<b>Reyting har 5-10 daqiqada yangilanadi!</b>"
                            show_rating += "\nBosh menyu -> Reyting ko'rish tugmalari orqali reytingni qayta tekshirishni unutmang!"
                            show_rating += "🤖 Bot Abdulaziz Madaminov (@abdulaziz_madaminov) tomonidan tayyorlandi."
                            if percent < 80:
                                await message.answer(
                                    after_test_low(message.from_user.username, name, subject, test_code, questionLength,
                                                   userAnswers, percent, formatted_now),
                                    disable_web_page_preview=True)
                              
                                await message.answer(show_rating, reply_markup=main_menu)
                                await Main.main_menu.set()
                            elif 80 <= percent <= 100:
                                await message.answer(
                                    after_test_high(message.from_user.username, name, subject, test_code,
                                                    questionLength,
                                                    userAnswers, percent, formatted_now),
                                    disable_web_page_preview=True)
                                await message.answer(show_rating, reply_markup=main_menu)
                                await Main.main_menu.set()

                        else:
                            await message.answer(f"❗️ <b>{test_id}</b>-sonli testning {len1}-ta savoli mavjud!\n\n"
                                                 f"<i>Siz esa {len2}-ta javob yubordingiz. Iltimos, qayta yuboring!!!</i>")
                            return
                        # need to build rating for users

                    else:
                        await message.answer("Siz bu testni avval yechgansiz! Qayta javob berish mumkun emas!")
                        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                        await Main.main_menu.set()
                #################################################
                elif test_type == "specialPM":
                    errors_part1 = 0
                    errors_part2 = 0
                    is_Done_before = await db.check_is_done(test_id, message.from_user.id)

                    if is_Done_before is None:
                        correct_answer = await db.get_test_answers(test_id)  # correct answers
                        user_answers = re.sub('[^a-zA-Z]+', '', user_answers)  # user answers
                        # count len of correct_answer and users answer and first check it
                        len1 = await db.get_test_length(test_id)
                        len2 = len(user_answers)
                        date_t = date.today()
                        date_t = str(date_t)

                        if len1 == len2:
                            part1 = user_answers[0:40]
                            part2 = user_answers[40:]

                            part1_corect = correct_answer[0:40]
                            part2_corect = correct_answer[40:]
                            await db.add_done_test(test_id, message.from_user.id, date_t)
                            for x, y in zip(part1, part1_corect):
                                if x == y:
                                    pass
                                else:
                                    errors_part1 += 1
                            for j, k in zip(part2, part2_corect):
                                if j == k:
                                    pass
                                else:
                                    errors_part2 += 1

                            part1UserCorrectAnswers = 40 - errors_part1
                            part1UserCorrectAnswers = int(part1UserCorrectAnswers)
                            part1BALL = part1UserCorrectAnswers * 2
                            part2UserCorrectAnswers = 40 - errors_part2
                            part2UserCorrectAnswers = int(part2UserCorrectAnswers)
                            part2BALL = part2UserCorrectAnswers * 0.5

                            overall_ball = part1BALL + part2BALL
                            overall_erros = errors_part2 + errors_part1
                            overall_ball = round(overall_ball, 1)

                            name = await db.getUser_name(message.from_user.id)
                            subject = await db.get_test_name(test_id)
                            test_code = test_id
                            questionLength = len(correct_answer)
                            userAnswers = len(correct_answer) - overall_erros

                            time_format = '%Y-%m-%d %H:%M:%S'
                            formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                            if overall_ball < 80:
                                await message.answer(
                                    after_test_lowPM(message.from_user.username, name, subject, test_code,
                                                     questionLength,
                                                     userAnswers, overall_ball, formatted_now, errors_part1,
                                                     errors_part2),
                                    disable_web_page_preview=True)
                                # rating
                            elif 80 <= overall_ball <= 100:
                                await message.answer(
                                    after_test_highPM(message.from_user.username, name, subject, test_code,
                                                      questionLength,
                                                      userAnswers, overall_ball, formatted_now, errors_part1,
                                                      errors_part2),
                                    disable_web_page_preview=True)
                            user_id = message.from_user.id
                            name = await db.getUser_name(user_id)
                            user_id = str(user_id)
                            test_id = str(test_id)
                            await db.add_rating(test_id, user_id, name, overall_ball, formatted_now, "specialPM")
                            rating = await db.show_rating_by_user(test_id)
                            show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
                            i = 1
                            for user in rating:
                                show_rating += "{0}) {1} - {2} ball \n".format(i, user['full_name'], user['ball'])
                                i += 1
                                
                            show_rating += "🤖 Bot Abdulaziz Madaminov (@abdulaziz_madaminov) tomonidan tayyorlandi."

                            await message.answer(show_rating)
                            await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                            await Main.main_menu.set()



                        else:
                            await message.answer(f"❗️ <b>{test_id}</b>-sonli testning {len1}-ta savoli mavjud!\n\n"
                                                 f"<i>Siz esa {len2}-ta javob yubordingiz. Iltimos, qayta yuboring!!!</i>")
                            return
                        # need to build rating for users

                    else:
                        await message.answer("Siz bu testni avval yechgansiz! Qayta javob berish mumkun emas!")
                        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                        await Main.main_menu.set()
                elif test_type == "specialA":
                    errors_part1 = 0
                    errors_part2 = 0
                    errors_part3 = 0
                    is_Done_before = await db.check_is_done(test_id, message.from_user.id)

                    if is_Done_before is None:
                        correct_answer = await db.get_test_answers(test_id)  # correct answers
                        user_answers = re.sub('[^a-zA-Z]+', '', user_answers)  # user answers
                        # count len of correct_answer and users answer and first check it
                        len1 = await db.get_test_length(test_id)
                        len2 = len(user_answers)
                        date_t = date.today()
                        date_t = str(date_t)

                        if len1 == len2:
                            part1 = user_answers[0:30]
                            part2 = user_answers[30:60]
                            part3 = user_answers[60:90]

                            part1_corect = correct_answer[0:30]
                            part2_corect = correct_answer[30:60]
                            part3_corect = correct_answer[60:90]
                            await db.add_done_test(test_id, message.from_user.id, date_t)
                            for x, y in zip(part1, part1_corect):
                                if x == y:
                                    pass
                                else:
                                    errors_part1 += 1
                            for j, k in zip(part2, part2_corect):
                                if j == k:
                                    pass
                                else:
                                    errors_part2 += 1
                            for m, n in zip(part3, part3_corect):
                                if m == n:
                                    pass
                                else:
                                    errors_part3 += 1

                            part1UserCorrectAnswers = 30 - errors_part1
                            part1UserCorrectAnswers = int(part1UserCorrectAnswers)
                            part1BALL = part1UserCorrectAnswers * 1.1
                            part2UserCorrectAnswers = 30 - errors_part2
                            part2UserCorrectAnswers = int(part2UserCorrectAnswers)
                            part2BALL = part2UserCorrectAnswers * 3.1
                            part3UserCorrectAnswers = 30 - errors_part3
                            part3UserCorrectAnswers = int(part3UserCorrectAnswers)
                            part3BALL = part3UserCorrectAnswers * 2.1

                            overall_ball = part1BALL + part2BALL + part3BALL
                            overall_ball = round(overall_ball, 1)
                            overall_erros = errors_part2 + errors_part1 + errors_part3

                            name = await db.getUser_name(message.from_user.id)
                            subject = await db.get_test_name(test_id)
                            test_code = test_id
                            questionLength = len(correct_answer)
                            userAnswers = len(correct_answer) - overall_erros

                            time_format = '%Y-%m-%d %H:%M:%S'
                            formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                            if overall_ball < 160:
                                await message.answer(
                                    after_test_lowA(message.from_user.username, name, subject, test_code,
                                                    questionLength,
                                                    userAnswers, overall_ball, formatted_now, errors_part1,
                                                    errors_part2, errors_part3),
                                    disable_web_page_preview=True)
                                # rating
                            elif 160 <= overall_ball <= 189:
                                await message.answer(
                                    after_test_highA(message.from_user.username, name, subject, test_code,
                                                     questionLength,
                                                     userAnswers, overall_ball, formatted_now, errors_part1,
                                                     errors_part2, errors_part3),
                                    disable_web_page_preview=True)
                            # rating
                            user_id = message.from_user.id
                            name = await db.getUser_name(user_id)
                            user_id = str(user_id)
                            test_id = str(test_id)
                            await db.add_rating(test_id, user_id, name, overall_ball, formatted_now, "specialA")
                            rating = await db.show_rating_by_user(test_id)
                            show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
                            i = 1
                            for user in rating:
                                show_rating += "{0}) {1} - {2} ball\n".format(i, user['full_name'], user['ball'])
                                i += 1
                            
                            
                            show_rating += "🤖 Bot Abdulaziz Madaminov (@abdulaziz_madaminov) tomonidan tayyorlandi."
                            await message.answer(show_rating)
                            await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                            await Main.main_menu.set()


                        #print(rating)

                        else:
                            await message.answer(f"❗️ <b>{test_id}</b>-sonli testning {len1}-ta savoli mavjud!\n\n"
                                                 f"<i>Siz esa {len2}-ta javob yubordingiz. Iltimos, qayta yuboring!!!</i>")
                            return
                        # need to build rating for users

                    else:
                        await message.answer("Siz bu testni avval yechgansiz! Qayta javob berish mumkun emas!")
                        await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                        await Main.main_menu.set()
            else:
                await message.answer("""
                🤷‍♂️ <b>Afsus! Test bazadan topilmadi!</b>
                Test kodini noto`g`ri yuborgan bo`lishingiz mumkin, iltimos tekshirib qaytadan yuboring.
                                    """)
                await message.answer("🏡 Bosh menyu", reply_markup=main_menu)
                await Main.main_menu.set()                       
