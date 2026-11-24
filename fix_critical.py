# fix_critical.py - إصلاح الأخطاء الحرجة فقط

with open('routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 14 خطأ حرج فقط تمنع التشغيل
fixes = [
    ('fr om sqlalchemy import func', 'from sqlalchemy import func'),
    ('from app import a pp, db, mail', 'from app import app, db, mail'),
    ('Visit or,', 'Visitor,'),
    ('d ef send_verification_email', 'def send_verification_email'),
    ('def get_db _cart_items', 'def get_db_cart_items'),
    ('def merge_sessio n_cart_into_db', 'def merge_session_cart_into_db'),
    ('impo rt cloudinary.uploader', 'import cloudinary.uploader'),
    ('api_s ecret=os.environ.get', 'api_secret=os.environ.get'),
    ('exce pt Exception as e:', 'except Exception as e:'),
    ('token_uri="https://oauth2.googleapi s.com/token"', 'token_uri="https://oauth2.googleapis.com/token"'),
    ('credentials=cred s)', 'credentials=creds)'),
    ('{"ra w": raw_message}', '{"raw": raw_message}'),
    ('def allowed_file(filenam e):', 'def allowed_file(filename):'),
    ('session["cart "]', 'session["cart"]'),
]

for wrong, correct in fixes:
    content = content.replace(wrong, correct)

with open('routes.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم إصلاح 14 خطأ حرج!")