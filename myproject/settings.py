# from pathlib import Path
# import os
# from dotenv import load_dotenv
# import dj_database_url

# BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(BASE_DIR / ".env")
# print("DEBUG DB FILE EXISTS:", os.path.exists(BASE_DIR / ".env"))
# print("DATABASE_URL:", os.getenv("DATABASE_URL"))
# SECRET_KEY = 'django-insecure-change-this-in-production'

# DEBUG = True

# ALLOWED_HOSTS = ["*"]  # production me restrict karna

# # =========================
# # APPLICATIONS
# # =========================

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     "django.contrib.sites",

#     "rest_framework",  # <- keep this

#     "rest_framework.authtoken",  # 🔥 ADD THIS (IMPORTANT)

#     "allauth",
#     "allauth.account",
#     "allauth.socialaccount",

#     "allauth.socialaccount.providers.google",
#     "allauth.socialaccount.providers.github",

#     "dj_rest_auth",
#     "dj_rest_auth.registration",
#     'rest_framework_simplejwt',

#     'corsheaders',
#     'myapp',
    
# ]
# SITE_ID = 2

# # =========================
# # MIDDLEWARE
# # =========================

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # MUST be on top

#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',

#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'allauth.account.middleware.AccountMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'myproject.urls'

# # =========================
# # TEMPLATES
# # =========================

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproject.wsgi.application'

# # =========================
# # DATABASE
# # =========================

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }



# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///db.sqlite3'
#     )
# }

# # =========================
# # PASSWORD VALIDATION
# # =========================

# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # =========================
# # INTERNATIONALIZATION
# # =========================

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Asia/Kolkata'
# USE_I18N = True
# USE_TZ = True

# # =========================
# # STATIC FILES
# # =========================

# STATIC_URL = 'static/'

# # =========================
# # CORS (IMPORTANT FOR REACT)
# # =========================

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]
# CORS_ALLOW_CREDENTIALS = True
# # =========================
# # EMAIL CONFIG (SECURE)
# # =========================

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# CSRF_TRUSTED_ORIGINS = [
#     "https://ai-code-mentor-backend-0rmn.onrender.com",
# ]

# # =========================
# # REST FRAMEWORK + JWT
# # =========================

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     )
# }
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]
# SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#         "SCOPE": ["profile", "email"],
#         "AUTH_PARAMS": {"access_type": "online"},
#     },
#     "github": {
#         "SCOPE": ["user:email"],
#     },
# }
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False

# SESSION_COOKIE_SAMESITE = "Lax"
# CSRF_COOKIE_SAMESITE = "Lax"
# LOGIN_REDIRECT_URL = 'http://localhost:3000/Dashboard'
# SOCIALACCOUNT_LOGIN_ON_GET = True

# ACCOUNT_LOGIN_REDIRECT_URL = "http://localhost:3000/Dashboard"
# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_QUERY_EMAIL = True
# SOCIALACCOUNT_ADAPTER = "allauth.socialaccount.adapter.DefaultSocialAccountAdapter"
# ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
# ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# DJ_REST_AUTH = {
#     "PASSWORD_RESET_CONFIRM_URL": "http://localhost:3000/reset-password/{uid}/{token}",
#     "PASSWORD_RESET_USE_SITES_DOMAIN": False,
# }
# from datetime import timedelta
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
# }





from pathlib import Path
import os
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['ai-code-mentor-backend-0rmn.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt',
    'corsheaders',
    'myapp',
]

SITE_ID = 2

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# =========================
# DATABASE
# =========================

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL')
#     )
# }


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "github": {
        "SCOPE": ["user:email"],
    },
}
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Render pe — PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL
        )
    }
else:
    # Local pe — SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# CORS
# =========================

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://ai-code-mentor-frontend.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# =========================
# EMAIL
# =========================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# =========================
# CSRF
# =========================

CSRF_TRUSTED_ORIGINS = [
    "https://ai-code-mentor-backend-0rmn.onrender.com",
    "https://ai-code-mentor-frontend.onrender.com",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# =========================
# REST FRAMEWORK + JWT
# =========================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

# =========================
# ALLAUTH
# =========================

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#         "SCOPE": ["profile", "email"],
#         "AUTH_PARAMS": {"access_type": "online"},
#     },
#     "github": {
#         "SCOPE": ["user:email"],
#     },
# }

LOGIN_REDIRECT_URL = 'https://ai-code-mentor-frontend.onrender.com/dashboard'
ACCOUNT_LOGIN_REDIRECT_URL = 'https://ai-code-mentor-frontend.onrender.com/dashboard'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = "allauth.socialaccount.adapter.DefaultSocialAccountAdapter"
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
SOCIALACCOUNT_LOGIN_REDIRECT_URL = "https://ai-code-mentor-frontend.onrender.com/dashboard"

DJ_REST_AUTH = {
    "PASSWORD_RESET_CONFIRM_URL": "https://ai-code-mentor-frontend.onrender.com/reset-password/{uid}/{token}",
    "PASSWORD_RESET_USE_SITES_DOMAIN": False,
}