from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField

from wtforms import (
    BooleanField,
    FloatField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Regexp,
    ValidationError,  
    Length
)

import re
# ==================================================
# 🧶 PRODUCT FORM
# ==================================================

class ProductForm(FlaskForm):

    # ==========================
    # 🧵 Product Name
    # ==========================

    name = StringField(
        "Product Name",
        validators=[
            DataRequired()
        ]
    )

    # ==========================
    # 🏷️ Product Category
    # ==========================

    category = SelectField(
        "Category",
        choices=[
            ("dolls", "Dolls"),
            ("keychains", "Keychains"),
            ("pattern", "Pattern"),
            ("coaster", "Coaster"),
            ("ready_stock", "Ready Stock")
        ],
        validators=[
            DataRequired()
        ]
    )



# ==================================================
# 🔐 CUSTOM PASSWORD VALIDATOR
# ==================================================
def validate_password_strength(form, field):
    """
    يتحقق من قوة كلمة المرور:
    - 8 أحرف على الأقل
    - حرف كبير واحد على الأقل
    - رقم واحد على الأقل
    - رمز خاص واحد على الأقل
    """
    password = field.data
    
    if len(password) < 8:
        raise ValidationError(
            "كلمة المرور يجب أن تكون 8 أحرف على الأقل."
        )
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            "كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل."
        )
    
    if not re.search(r'\d', password):
        raise ValidationError(
            "كلمة المرور يجب أن تحتوي على رقم واحد على الأقل."
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            "كلمة المرور يجب أن تحتوي على رمز خاص واحد على الأقل (!@#$%^&*)."
        )
    # ==========================
    # 💰 Product Price
    # ==========================

    price = FloatField(
        "Price",
        validators=[
            DataRequired()
        ]
    )

    # ==========================
    # 📜 Product Description
    # ==========================

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    # ==========================
    # 🖼️ Product Image
    # ==========================

    image = FileField(
        "Product Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Images only!"
            )
        ]
    )

    # ==========================
    # 📍 Publish Location
    # ==========================

    publish_location = SelectField(
        "Publish Product",
        choices=[
            (
                "both",
                "Show in Home + Products pages"
            ),
            (
                "products_only",
                "Show only in Products page"
            )
        ],
        default="products_only"
    )

    # ==========================
    # ✨ Customization
    # هل المنتج قابل للتخصيص؟
    # ==========================

    is_customizable = BooleanField(
        "Allow Customization",
        default=False
    )

    # ==========================
    # 💾 Submit
    # ==========================

    submit = SubmitField(
        "Save"
    )


# ==================================================
# 👤 REGISTER FORM
# ==================================================
class RegisterForm(FlaskForm):
    # ==========================
    # 👤 Username
    # ==========================
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25)
        ]
    )
    
    # ==========================
    # 📧 Email
    # ==========================
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    
    # ==========================
    # 📱 Phone Number
    # ==========================
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r'^\d{8,15}$',
                message="رقم الجوال يجب أن يحتوي على 8-15 رقم فقط."
            )
        ]
    )
    
    # ==========================
    #  Password
    # ==========================
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            validate_password_strength  # ← أضفنا الـ validator الجديد
        ]
    )
    
    # ==========================
    # 🔐 Confirm Password
    # ==========================
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="كلمتا المرور غير متطابقتين.")
        ]
    )
    
    # ==========================
    #  Submit
    # ==========================
    submit = SubmitField("Register")

# ==================================================
# 🔐 LOGIN FORM
# ==================================================

class LoginForm(FlaskForm):

    # ==========================
    # 📧 Email
    # ==========================

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    # ==========================
    # 🔑 Password
    # ==========================

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    # ==========================
    # 🔓 Submit
    # ==========================

    submit = SubmitField(
        "Login"
    )


# ==================================================
# 📧 VERIFY EMAIL FORM
# ==================================================

class VerifyCodeForm(FlaskForm):

    # ==========================
    # 🔢 Verification Code
    # ==========================

    code = StringField(
        "Verification Code",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=6
            )
        ]
    )

    # ==========================
    # ✅ Submit
    # ==========================

    submit = SubmitField(
        "Verify"
    )