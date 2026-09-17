BARBER.UZ
=========

O'zbekiston bo'yicha barberlar marketplace'i (Django MVP).
Bu versiya sodda qilingan: Docker/PostgreSQL yo'q, faqat Python + Django + SQLite.
Kichik/o'rta loyihalar uchun bu yetarli va ishlatish ancha oson.

ASOSIY QISMLAR
1. User va Barber rollari + Django Admin.
2. 14 hudud bo'yicha barber qidirish.
3. Barber profil: avatar/cover, bio, manzil, telefon, ish vaqti, tajriba, Instagram/Telegram.
4. Xizmatlar, narx va davomiylik.
5. Foto va VIDEO portfolio.
6. Booking va statuslar: pending/confirmed/cancelled/done.
7. Review/rating.
8. Favorites.
9. Notification modeli.
10. Free/Pro subscription modeli.
11. SQLite database (fayl asosida, alohida server kerak emas).
12. S3-compatible media storage uchun USE_S3 (ixtiyoriy, keyinroq kerak bo'lsa).
13. WhiteNoise static files.
14. Demo payment model va provider ulash uchun tayyor joy.

MUHIM
Bu ZIP — infratuzilma skeleton hisoblanadi. Haqiqiy pul to'lovi, SMS,
Telegram bot, S3 storage uchun tegishli provider account/API kalitlari kerak.
API kalitlarni kodga yozmang; faqat .env orqali bering.

ISHGA TUSHIRISH (Windows, PowerShell)
------------------------------------
1. Terminalda loyiha papkasiga kiring:
   cd barber_uz_pro

2. Virtual muhit yarating va faollashtiring:
   python -m venv venv
   venv\Scripts\activate

3. Kerakli paketlarni o'rnating:
   pip install -r requirements.txt

4. .env faylini yarating:
   Copy-Item .env.example .env
   (Standart holatda DEBUG=True va SQLite ishlaydi — hech narsa o'zgartirish shart emas.)

5. Bazani tayyorlang:
   python manage.py makemigrations
   python manage.py migrate

6. Admin hisobini yarating:
   python manage.py createsuperuser

7. Serverni ishga tushiring:
   python manage.py runserver

8. Brauzerda oching:
   Sayt:  http://127.0.0.1:8000/
   Admin: http://127.0.0.1:8000/admin/

   MUHIM: http:// bilan kiring (https:// emas). Agar brauzeringiz avtomatik
   https ga o'tkazsa, chrome://net-internals/#hsts sahifasida 127.0.0.1
   uchun "Delete domain security policies" qiling.

KEYINGI SAFAR ISHGA TUSHIRISH
Har safar qaytadan pip install qilish shart emas — faqat:
   venv\Scripts\activate
   python manage.py runserver

MA'LUMOTLAR BAZASINI ZAXIRALASH (BACKUP)
SQLite — bu shunchaki bitta fayl: db.sqlite3
Zaxira olish uchun uni boshqa joyga nusxalab qo'ying:
   Copy-Item db.sqlite3 db_backup.sqlite3

PRODUCTIONGA CHIQARISH HAQIDA
Bu versiya asosan LOCAL/DEVELOPMENT uchun sozlangan (DEBUG=True, SQLite).
Agar kelajakda haqiqiy saytga (domenga) chiqarish kerak bo'lsa, quyidagilar
alohida ko'rib chiqiladi:
- DEBUG=False qilish
- kuchli SECRET_KEY
- real ALLOWED_HOSTS va CSRF_TRUSTED_ORIGINS
- HTTPS (hosting provayder yoki reverse proxy orqali)
- ko'proq foydalanuvchi/trafik uchun PostgreSQL (SQLite yetarli bo'lmasa)
- media storage (S3 va h.k.)
- payment provider webhook signature verification
- Telegram/SMS provider credentials
- rate limiting va login protection
- admin 2FA/restricted access
- monitoring va error tracking
Hozircha bularning hech biri shart emas — shunchaki local'da ishga tushirib
sinab ko'rish uchun yuqoridagi qadamlar yetarli.

TEXNOLOGIYALAR
Python 3.13
Django 6.1
SQLite
HTML5/CSS3/JavaScript
Pillow
WhiteNoise
