def javob_tekshirish():
    text = """
🟡 <b>Javoblar tekshirish yo'riqnomasi</b>

Javoblarni bilish uchun:

Test kodi*sizning javoblaringiz

ko'rinishida yuboring

-----------------------

Misol:
000000*aabbccdd
<b>yoki</b>
000000*1a2a3b4b 

🛑🛑🛑 Agar siz <b>blok-test</b> javoblarini yubormoqchi bo'lsangiz,
quyidagicha yuborishingiz mumkun:

1) Prezident Maktab o'quvchilari: (40ta+40ta)
-> Misol: 1a2b...39a40b+41a42b...79a80b
    <b>yoki</b> aabc..ab+cd...ad
    
2) Abiturientlar: (30ta+30ta+30ta)
-> Misol: 1a2b...29a30b+31a32d....59a60b+61a62c....89a90b
    <b>yoki</b> abc...abc+acd...adc+abc...abc    
    """
    return text


def after_test_low(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now):
    text = f"""

👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
🔣 Foiz: <b>{ball}</b> %

🕰 Sana va vaqt: {formatted_now}

----------------------------------

☝️ <b>Natijangizni yaxshilash uchun testlarimizda doimiy qatnashib boring!</b>

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat
                           
"""
    return text


def after_test_high(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now):
    text = f"""

👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
🔣 Foiz: <b>{ball}</b> %

🕰 Sana va vaqt: {formatted_now}

----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text

def after_test_highPM(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2):
    text = f"""
👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Tanqidiy va Muammolida xatolar soni: <b>{part1}</b>
➡️ Ingliz tilidagi xatolar soni: <b>{part2}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text


def after_test_lowPM(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2):
    text = f"""
👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Tanqidiy va Muammolida xatolar soni: <b>{part1}</b>
➡️ Ingliz tilidagi xatolar soni: <b>{part2}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

☝️ <b>Natijangizni yaxshilash uchun testlarimizda doimiy qatnashib boring!</b>
----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text


def qoshish_yoriqnomasi():
    text = """
❗️<b>Test yaratish yo'riqnomasi</b>

Test yaratish uchun

Fan nomi*to'g'ri javoblar

ko'rinishida yuboring

-----------------------

Misol:
Matematika*1a2a3b4b
<b>yoki</b>
Matematika*abcfed
    """
    return text


def bazaga_qoshildi(test_id, user_answers):
    text = f"""

<b>✅Test bazaga qo`shildi.</b>

Test kodi: <b>{test_id}</b>
Savollar soni: {len(user_answers)} ta

Testda qatnashuvchilar quyidagi ko`rinishda javob yuborishlari mumkin:

{test_id}*abcde... ({len(user_answers)} ta)
<b>yoki</b>
{test_id}*1a2b3c4d... ({len(user_answers)} ta)
    """

    return text



def show_infor(name, phone):
    text = f"""
📋 <b>Sizning ma'lumotlaringiz:</b>

Ismingiz: <b>{name}</b>
Telefon raqamingiz: <b>{phone}</b>



⚠️ Diqqat!
<i>Agar ma'lumotlaringizni o'zgartirmoqchi bo'lsangiz, 
quyidagi o'zgartirmoqchi bo'lgan tugmalardan birini bosing</i>👇

"""
    return text




def show_infor_updated(name, phone):
    text = f"""
✅ O'zgartirildi!!!

📋 <b>Sizning ma'lumotlaringiz:</b>

Ismingiz: <b>{name}</b>
Telefon raqamingiz: <b>{phone}</b>



⚠️ Diqqat!
<i>Agar ma'lumotlaringizni o'zgartirmoqchi bo'lsangiz, 
quyidagi o'zgartirmoqchi bo'lgan tugmalardan birini bosing</i>👇

"""
    return text





def add_PMTest():
    text = """
⚠️ Diqqat!

Test savollari 80-ta bo'lishi shart!
Aks xolda, bot test yaratmaydi!
E'tiborli bo'ling!

------------------------------------

Test yaratish yo'riqnomasi

Test nomi*aabbccaabbcc
<b>yoki</b>
Test nomi*1a2b...39a40+b41a...79a80a 
    
    """
    return text


def add_ATest():
    text = """
⚠️ Diqqat!

Test savollari 90-ta bo'lishi shart!
Aks xolda, bot test yaratmaydi!
E'tiborli bo'ling!


------------------------------------

Test yaratish yo'riqnomasi

Test nomi*aabbccaabbcc
<b>yoki</b>
Test nomi*1a2b...29a30b+31a...59a60a+61a62c...89d90b

    """
    return text





def after_test_lowA(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2, part3):
    text = f"""

👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Majburiy blokda xatolar soni: <b>{part1}</b>
➡️ Birinchi asosiy blokda xatolar soni: <b>{part2}</b>
➡️ Ikkinchi asosiy blokda xatolar soni: <b>{part3}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

☝️ <b>Natijangizni yaxshilash uchun testlarimizda doimiy qatnashib boring!</b>

----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text



def after_test_highA(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2, part3):
    text = f"""

👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Majburiy blokda xatolar soni: <b>{part1}</b>
➡️ Birinchi asosiy blokda xatolar soni: <b>{part2}</b>
➡️ Ikkinchi asosiy blokda xatolar soni: <b>{part3}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text