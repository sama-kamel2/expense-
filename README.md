# نظام إدارة المصروفات (Expense Management System)

مشروع Django كامل وجاهز للنشر (production-ready) لإدارة المصروفات الشخصية.

## المميزات
- تسجيل مستخدم / تسجيل دخول / تسجيل خروج
- لوحة تحكم (Dashboard) بإحصائيات فورية
- إضافة / تعديل / حذف المصروفات
- تصنيفات مصروفات خاصة بكل مستخدم
- تاريخ + مبلغ + وصف لكل مصروف
- إجمالي المصروفات وإجمالي مصروفات الشهر الحالي
- إحصائيات حسب التصنيف وآخر 6 أشهر
- بحث وفلترة (بالتصنيف، التاريخ، الوصف)
- لوحة إدارة Django (Django Admin)
- واجهة متجاوبة (Responsive) بدعم اللغة العربية RTL
- إعدادات جاهزة للنشر على سيرفر/دومين حقيقي

## التشغيل محليًا

```bash
python3 -m venv venv
source venv/bin/activate          # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # ثم عدّل القيم داخل .env
export DEBUG=True                 # للتطوير المحلي فقط

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

افتح المتصفح على: http://127.0.0.1:8000/

## متغيرات البيئة (.env)
انسخ `.env.example` إلى `.env` واملأ القيم:

| المتغير | الوصف |
|---|---|
| `SECRET_KEY` | مفتاح سري عشوائي وطويل (لازم تغيّره قبل النشر) |
| `DEBUG` | `False` في الإنتاج |
| `ALLOWED_HOSTS` | الدومين بتاعك مفصول بفاصلة |
| `CSRF_TRUSTED_ORIGINS` | روابط https الخاصة بالدومين |
| `DATABASE_URL` | رابط قاعدة بيانات Postgres (اختياري، لو فاضي هيستخدم SQLite) |

## النشر (Deployment)

المشروع جاهز لأي منصة تدعم Python/WSGI (مثل: Railway, Render, Heroku-style, DigitalOcean App Platform, أو VPS عادي مع Nginx + Gunicorn).

### خطوات عامة على VPS (Ubuntu + Nginx + Gunicorn):

1. ارفع المشروع للسيرفر وجهّز بيئة بايثون:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. جهّز ملف `.env` بالقيم الحقيقية (`DEBUG=False`, `ALLOWED_HOSTS`, `SECRET_KEY`, `DATABASE_URL`...).
3. اجمع الملفات الثابتة:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. شغّل المشروع بـ Gunicorn:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```
5. حط Nginx كـ reverse proxy قدام Gunicorn، وفعّل شهادة SSL (مثلاً عن طريق Certbot) عشان `SECURE_SSL_REDIRECT` يشتغل صح.
6. (اختياري) استخدم Postgres بدل SQLite لو عندك أكتر من instance بيشتغل على نفس القاعدة، عن طريق `DATABASE_URL`.

### النشر على منصة PaaS (Railway/Render/Heroku)
المشروع فيه `Procfile` و`runtime.txt` جاهزين، يكفي تربط الـ repo وتضيف environment variables (زي `.env.example`) ومعظم المنصات هتشغّل `release: migrate` و`web: gunicorn` تلقائيًا.

## هيكل المشروع
```
expense_manager/
├── config/            # إعدادات المشروع (settings, urls, wsgi)
├── expenses/          # التطبيق الرئيسي (models, views, forms, urls, admin)
├── templates/expenses/# قوالب HTML
├── static/css/        # ملفات CSS
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
└── manage.py
```

## ملاحظات أمنية قبل النشر
- غيّر `SECRET_KEY` لقيمة عشوائية طويلة.
- خلّي `DEBUG=False` في الإنتاج.
- حدّد `ALLOWED_HOSTS` و`CSRF_TRUSTED_ORIGINS` بالدومين الحقيقي فقط.
- استخدم HTTPS (SSL) دايمًا في الإنتاج.
