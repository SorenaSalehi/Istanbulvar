from django import forms
from django.core.validators import RegexValidator
from .models import Address
import re

phone_regex = RegexValidator(
    regex=r"^\(9\d{2}\)\s\d{3}\s-\s\d{4}$",
    message="فرمت شماره تلفن باید به صورت (9**) *** - **** باشد.",
)

email_regex = RegexValidator(
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    message="لطفاً یک آدرس ایمیل معتبر وارد کنید.",
)

password_regex = RegexValidator(
    regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    message=(
        "رمز عبور باید حداقل ۸ کاراکتر، شامل یک حرف بزرگ، یک حرف کوچک، یک عدد "
        "و یک کاراکتر ویژه باشد."
    ),
)

PHONE_WIDGET_ATTRS = {
    "id": "phone_number",
    "placeholder": "(9__) ___ - ____",
    "data-mask": "(9##) ### - ####",
    "class": "phone-mask",
}


class SignUpForm(forms.Form):
    email = forms.EmailField(
        label="آدرس ایمیل",
        required=True,
        validators=[email_regex],
        widget=forms.TextInput(
            attrs={"placeholder": "ایمیل خود را وارد کنید"}
        ),
    )
    phone_number = forms.CharField(
        label="شماره تلفن",
        max_length=16,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs=PHONE_WIDGET_ATTRS),
    )
    password = forms.CharField(
        label="رمز عبور",
        required=True,
        validators=[password_regex],
        widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور خود را وارد کنید"}),
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور خود را دوباره وارد کنید"}),
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        cleaned = re.sub(r"\D", "", phone)
        if len(cleaned) != 10 or not cleaned.startswith("9"):
            raise forms.ValidationError(
                "شماره تلفن باید ۱۰ رقمی و با 9 شروع شود."
            )
        return cleaned

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "رمزهای عبور مطابقت ندارند.")
        return cleaned_data


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره تلفن",
        max_length=16,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs=PHONE_WIDGET_ATTRS),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور خود را وارد کنید"}),
        required=True,
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        cleaned = re.sub(r"\D", "", phone)
        if len(cleaned) != 10 or not cleaned.startswith("9"):
            raise forms.ValidationError(
                "شماره تلفن باید ۱۰ رقمی و با 9 شروع شود."
            )
        return cleaned


class LoginByCodeForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره تلفن",
        max_length=16,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs=PHONE_WIDGET_ATTRS),
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        cleaned = re.sub(r"\D", "", phone)
        if len(cleaned) != 10 or not cleaned.startswith("9"):
            raise forms.ValidationError(
                "شماره تلفن باید ۱۰ رقمی و با 9 شروع شود."
            )
        return cleaned


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="کد تأیید",
        max_length=5,
        required=True,
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "first_name",
            "last_name",
            "street",
            "apartment",
            "city",
            "state",
            "is_corporate",
            "tax_office",
            "company_name",
            "tax_id",
        ]
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "street": "آدرس",
            "apartment": "آپارتمان / واحد",
            "city": "شهر",
            "state": "استان",
            "is_corporate": "آدرس شرکتی",
            "tax_office": "اداره مالیاتی",
            "company_name": "نام شرکت",
            "tax_id": "شناسه مالیاتی",
        }
        widgets = {
            "street": forms.TextInput(attrs={"placeholder": "آدرس خود را وارد کنید"}),
            "city": forms.TextInput(attrs={"placeholder": "شهر خود را وارد کنید"}),
            "apartment": forms.TextInput(attrs={"placeholder": "آپارتمان، شماره واحد و غیره"}),
            "tax_id": forms.TextInput(attrs={"placeholder": "در صورت شرکتی بودن آدرس پر شود"}),
            "tax_office": forms.TextInput(attrs={"placeholder": "اداره مالیاتی را وارد کنید"}),
            "company_name": forms.TextInput(attrs={"placeholder": "نام شرکت را وارد کنید"}),
            "is_corporate": forms.CheckboxInput(),
        }
        error_messages = {
            "street": {"required": "لطفاً آدرس را وارد کنید."},
            "city": {"required": "لطفاً شهر را وارد کنید."},
            "state": {"required": "لطفاً استان را انتخاب کنید."},
        }

    def clean(self):
        cleaned_data = super().clean()
        is_corporate = cleaned_data.get("is_corporate")
        tax_office = cleaned_data.get("tax_office")
        company_name = cleaned_data.get("company_name")
        tax_id = cleaned_data.get("tax_id")
        if is_corporate or tax_office or company_name or tax_id:
            if not tax_office:
                self.add_error("tax_office", "در صورت شرکتی بودن آدرس، وارد کردن اداره مالیاتی الزامی است.")
            if not company_name:
                self.add_error("company_name", "در صورت شرکتی بودن آدرس، وارد کردن نام شرکت الزامی است.")
            if not tax_id:
                self.add_error("tax_id", "در صورت شرکتی بودن آدرس، وارد کردن شناسه مالیاتی الزامی است.")
        return cleaned_data
