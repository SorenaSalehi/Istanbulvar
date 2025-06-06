"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%y-xvlur3t-w4o*cg-y8&rif6&#gy9+)mv3o)m-l+29bljs#$a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://iran.wigenzo.com.tr",
    "https://www.iran.wigenzo.com.tr",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My apps
    "users",
    "shop",
    "payment",
    "website",
    "django_summernote",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # My context_processors
                "shop.context_processors.getHeader",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "assets",
]


# Custom country/province choices (unchanged)

COUNTRY_CHOICES = (("Iran", "ایران"),)

IRAN_PROVINCES_CHOICES = (
    {"id": "1",  "name": "البرز"},
    {"id": "2",  "name": "اردبیل"},
    {"id": "3",  "name": "بوشهر"},
    {"id": "4",  "name": "چهارمحال و بختیاری"},
    {"id": "5",  "name": "آذربایجان شرقی"},
    {"id": "6",  "name": "فارس"},
    {"id": "7",  "name": "گیلان"},
    {"id": "8",  "name": "گلستان"},
    {"id": "9",  "name": "همدان"},
    {"id": "10", "name": "هرمزگان"},
    {"id": "11", "name": "ایلام"},
    {"id": "12", "name": "اصفهان"},
    {"id": "13", "name": "کرمان"},
    {"id": "14", "name": "کرمانشاه"},
    {"id": "15", "name": "خوزستان"},
    {"id": "16", "name": "کهگیلویه و بویراحمد"},
    {"id": "17", "name": "کردستان"},
    {"id": "18", "name": "لرستان"},
    {"id": "19", "name": "مرکزی"},
    {"id": "20", "name": "مازندران"},
    {"id": "21", "name": "خراسان شمالی"},
    {"id": "22", "name": "قزوین"},
    {"id": "23", "name": "قم"},
    {"id": "24", "name": "خراسان رضوی"},
    {"id": "25", "name": "سمنان"},
    {"id": "26", "name": "سیستان و بلوچستان"},
    {"id": "27", "name": "خراسان جنوبی"},
    {"id": "28", "name": "تهران"},
    {"id": "29", "name": "آذربایجان غربی"},
    {"id": "30", "name": "یزد"},
    {"id": "31", "name": "زنجان"},
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


##### MY Custom Settings

AUTH_USER_MODEL = "users.CustomUser"
