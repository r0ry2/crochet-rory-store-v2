import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ==================================================
# ⚙️ الإعدادات
# ==================================================
# اسم ملف الـ OAuth اللي نزلته من Google Cloud
CLIENT_SECRET_FILE = "client_secret_796767713706-d2dfk6felpuha0d4ie5n6oc81qqs9qic.apps.googleusercontent.com.json"

# الملف اللي راح يتولد فيه الـ Refresh Token بعد النجاح
TOKEN_FILE = "token.json"

# الصلاحيات المطلوبة (إرسال إيميل فقط)
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# ⚠️ غيّر هذا البريد إلى بريدك الشخصي اللي تبي ترسل عليه الإيميل التجريبي
TEST_RECIPIENT_EMAIL = "noni200217noni@gmail.com"  # <-- غيّر هذا إذا حابب


# ==================================================
# 📧 دالة إنشاء رسالة الإيميل
# ==================================================
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html', 'utf-8')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    # تشفير الرسالة بصيغة base64url كما تتطلب Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


# ==================================================
# 🚀 دالة الإرسال الرئيسية
# ==================================================
def send_test_email():
    creds = None

    # 1. التحقق من وجود token.json محفوظ مسبقاً
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 2. إذا ما كان فيه token، أو انتهت صلاحيته، نطلب التفويض من المتصفح
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("\n🌐 جاري فتح المتصفح لتسجيل الدخول ومنح الصلاحيات...")
            print("⚠️ تأكد من أنك مسجل دخول بحساب Gmail الصحيح في المتصفح.\n")
            
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            # المنفذ 8080 غالباً يكون متاح، لو كان محجوز غيّره لـ 8090 مثلاً
            creds = flow.run_local_server(port=8081)
            
        # حفظ الـ Credentials (بما فيها Refresh Token) في ملف آمن
        with open(TOKEN_FILE, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())
        print("✅ تم حفظ بيانات التفويض (Refresh Token) بنجاح في token.json\n")

    try:
        # 3. بناء خدمة Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        # 4. تجهيز الرسالة
        # نستخدم نفس بريد المرسل كاسم للعرض للتجربة
        sender_email = creds.token_uri.split('/')[0] # مجرد خدعة، الأفضل نحدده يدوياً
        # الأفضل: نقرأه من الـ creds أو نحدده يدوياً. هنا سنستخدم بريدك المعروف
        sender_email = "noni200217noni@gmail.com" # <-- غيّر هذا لبريدك المرسل
        
        message = create_message(
            sender=sender_email,
            to=TEST_RECIPIENT_EMAIL,
            subject="✅ اختبار Gmail API - Crochet Rory Store",
            message_text="""
                <h2>أهلاً بك في Crochet Rory Store! 🧶</h2>
                <p>هذه رسالة اختبارية للتأكد من نجاح إعداد Gmail API.</p>
                <p>إذا وصلت لك هذه الرسالة، فهذا يعني أن:</p>
                <ul>
                    <li>✅ إعدادات Google Cloud صحيحة.</li>
                    <li>✅ الـ Refresh Token تم حفظه بنجاح.</li>
                    <li>✅ الإرسال عبر HTTPS يعمل (ومناسب لـ Render).</li>
                </ul>
                <p>بالتوفيق في مشروعك! 💕</p>
            """
        )
        
        # 5. إرسال الرسالة
        print("📤 جاري إرسال الإيميل التجريبي...")
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        
        print(f"\n🎉 نجاح باهر! تم إرسال الإيميل بنجاح.")
        print(f"📧 معرف الرسالة (Message ID): {sent_message['id']}")
        print(f"📁 تم حفظ الـ Refresh Token في ملف: {TOKEN_FILE}")
        print("\n⚠️ خطوة مهمة جداً: افتح ملف token.json وانسخ قيمة 'refresh_token' سنحتاجها في الخطوة القادمة.")

    except Exception as error:
        print(f"\n❌ حدث خطأ أثناء الإرسال: {error}")


if __name__ == '__main__':
    # التحقق من وجود ملف الـ client_secret
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"❌ خطأ: لم يتم العثور على ملف {CLIENT_SECRET_FILE}")
        print("تأكد من أن الملف موجود في نفس مجلد هذا السكربت.")
    else:
        send_test_email()