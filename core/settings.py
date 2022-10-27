"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import sys

import decouple
import dj_database_url

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def get_env_variable(name, cast=str, default=""):
    try:
        if cast == bool:
            return os.environ[name].lower() in [
                "true",
                "1",
                "t",
                "y",
                "yes",
                "yeah",
                "yup",
                "certainly",
                "uh-huh",
            ]
        return cast(os.environ[name])
    # pylint: disable=W0702, bare-except
    except:
        return decouple.config(name, cast=cast, default=default)


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

SECRET_KEY = get_env_variable("SECRET_KEY")
DEBUG = get_env_variable("DEBUG", cast=bool)
ENVIRONMENT = get_env_variable("ENVIRONMENT", default="development")
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

LOGLEVEL = get_env_variable("LOGLEVEL", default="error").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOGLEVEL,
        },
    },
    "formatters": {
        "default": {
            # exact format is not important, this is the minimum information
            "format": "[%(asctime)s] %(name)-12s] %(levelname)-8s : %(message)s",
        },
    },
}

mailjet_api_key = get_env_variable("MAILJET_API_KEY")
mailjet_api_secret = get_env_variable("MAILJET_API_SECRET")

DEFAULT_FROM_EMAIL = "contact@apilos.beta.gouv.fr"

if mailjet_api_key != "":
    EMAIL_BACKEND = "django_mailjet.backends.MailjetBackend"
    MAILJET_API_KEY = mailjet_api_key
    MAILJET_API_SECRET = mailjet_api_secret
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

env_allowed_hosts = []
try:
    env_allowed_hosts = get_env_variable("ALLOWED_HOSTS").split(",")
except KeyError:
    pass

CONVERTAPI_SECRET = get_env_variable("CONVERTAPI_SECRET")

ALLOWED_HOSTS = ["localhost"] + env_allowed_hosts


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_dramatiq",
    "bailleurs.apps.BailleursConfig",
    "conventions.apps.ConventionsConfig",
    "instructeurs.apps.InstructeursConfig",
    "programmes.apps.ProgrammesConfig",
    "apilos_settings.apps.ApilosSettingsConfig",
    "stats.apps.StatsConfig",
    "siap.apps.SiapConfig",
    "users.apps.UsersConfig",
    "upload.apps.UploadConfig",
    "comments.apps.CommentsConfig",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "django_cas_ng",
    "django.contrib.admindocs",
    "explorer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

if not TESTING:
    MIDDLEWARE = MIDDLEWARE + [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": False,
            "context_processors": [
                "core.context_processor.get_environment",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

try:
    # dj_database_url is used in scalingo environment to interpret the
    # connection configuration to the DB from a single URL with all path
    # and credentials
    decouple.config("DATABASE_URL")
    default_settings = dj_database_url.config()
except decouple.UndefinedValueError:
    default_settings = {
        "ENGINE": "django.db.backends.postgresql",
        "USER": get_env_variable("DB_USER"),
        "NAME": get_env_variable("DB_NAME"),
        "HOST": get_env_variable("DB_HOST"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "PORT": get_env_variable("DB_PORT", default="5432"),
        "TEST": {
            "NAME": get_env_variable("DB_NAME") + "-test",
        },
        "ATOMIC_REQUESTS": True,
    }

# EXPORER settings
# from https://django-sql-explorer.readthedocs.io/en/latest/install.html
# The readonly access is configured with fake access when DB_READONLY env
# variable is not set.
DB_READONLY = decouple.config(
    "DB_READONLY", default="postgres://fakeusername:fakepassword@postgres:5432/database"
)
readonly_settings = dj_database_url.parse(DB_READONLY)

DATABASES = {"default": default_settings, "readonly": readonly_settings}
EXPLORER_CONNECTIONS = {"Default": "readonly"}
EXPLORER_DEFAULT_CONNECTION = "readonly"


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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Static files
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "staticfiles"))
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Why STAGING = FALSE ?
STAGING = False

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "core.backends.EmailBackend",
]

# Redirect to home URL after login
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Object storage with Scaleway
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = get_env_variable("AWS_DEFAULT_ACL")
AWS_S3_REGION_NAME = get_env_variable("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL = get_env_variable("AWS_S3_ENDPOINT_URL")

if AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 6 * 60 * 60

# Security settings
if ENVIRONMENT != "development":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Lax"

# https://django-csp.readthedocs.io/en/latest/configuration.html
CSP_DEFAULT_SRC = "'none'"
CSP_SCRIPT_SRC = (
    "https://stats.data.gouv.fr/piwik.js",
    "'self'",
    "'sha256-zaYxlJmjbzgo2YczX5XHFlvamZUNy264d7XlOOUwMME='",
    "'sha256-928U3JmFf9xytJJBtEU5V1FVGcqsTfwaVnI2vmHmamA='",
    "'sha256-lkrKw/baCFdnI+tB9T+0yFMewpXSk9yct2ZbWEGPDhY='",
    # Convention > récapitilatif > manage type I and type II options
    "'sha256-J71e5kr85q2XGRl+qwOA/tpMsXmKDjeTnvlzBhBsz/0='",
    "'sha256-h7boyH6dI/JQnsm6Iw1sAtEbdb/+638kREPj4sfWmMs='",  # ???
    # Convention > Récapitulatif > Comment type1and2
    "'sha256-7uHmVaAHWxl0RElSoWED7kK+9kRSQ+E6SQ3aBK1prkU='",
    # Swagger UI
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-standalone-preset.js",
)
CSP_IMG_SRC = (
    "'self'",
    "data:",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png",
)
CSP_OBJECT_SRC = "'none'"

X_FRAME_OPTIONS = "SAMEORIGIN"
CSP_FRAME_SRC = "'self'"
CSP_FONT_SRC = "'self'", "data:"
CSP_CONNECT_SRC = ("'self'", "https://stats.data.gouv.fr/piwik.php")
CSP_STYLE_SRC = (
    "'self'",
    "https://code.highcharts.com/css/highcharts.css",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui.css",
    "'unsafe-inline'",
)
CSP_MANIFEST_SRC = "'self'"
CSP_INCLUDE_NONCE_IN = [
    "script-src",
]
CSP_EXCLUDE_URL_PREFIXES = ("/explorer",)

# Disable whitenoise for test
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
    if TESTING
    else "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "siap.siap_authentication.SIAPJWTAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": get_env_variable("JWT_ALGORITHM", default="HS256"),
    "SIGNING_KEY": get_env_variable("JWT_SIGN_KEY", default=None),
    "USER_ID_CLAIM": "user-login",
    "USER_ID_FIELD": "cerbere_login",
}

SIAP_CLIENT_JWT_SIGN_KEY = get_env_variable("SIAP_CLIENT_JWT_SIGN_KEY", default=None)
SIAP_CLIENT_ALGORITHM = get_env_variable("SIAP_CLIENT_ALGORITHM", default="HS256")
SIAP_CLIENT_HOST = get_env_variable("SIAP_CLIENT_HOST", default=None)
SIAP_CLIENT_PATH = get_env_variable("SIAP_CLIENT_PATH", default=None)

SPECTACULAR_SETTINGS = {
    "TITLE": "API APiLos",
    "DESCRIPTION": "Documentation de l'API APiLos consommée par SIAP",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [{"name": "config-resource", "description": "Config Resource"}],
    "DISABLE_ERRORS_AND_WARNINGS": False,
    # OTHER SETTINGS
}

APILOS_PAGINATION_PER_PAGE = 20

# to do : deprecate drf_yasg
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "api.auto_schema.ReadWriteAutoSchema",
}

CERBERE_AUTH = get_env_variable("CERBERE_AUTH")
USE_MOCKED_SIAP_CLIENT = get_env_variable("USE_MOCKED_SIAP_CLIENT", cast=bool)
NO_SIAP_MENU = get_env_variable("NO_SIAP_MENU", cast=bool)

if CERBERE_AUTH:
    MIDDLEWARE = MIDDLEWARE + [
        "django_cas_ng.middleware.CASMiddleware",
        "siap.custom_middleware.CerbereSessionMiddleware",
    ]

    AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + [
        "core.backends.CerbereCASBackend",
    ]  # custom backend CAS

    # CAS config
    CAS_SERVER_URL = CERBERE_AUTH
    CAS_VERSION = "CAS_2_SAML_1_0"
    CAS_USERNAME_ATTRIBUTE = "username"
    CAS_APPLY_ATTRIBUTES_TO_USER = True
    CAS_RENAME_ATTRIBUTES = {
        "UTILISATEUR.ID": "username",
        "UTILISATEUR.LOGIN": "cerbere_login",
        "UTILISATEUR.NOM": "last_name",
        "UTILISATEUR.PRENOM": "first_name",
        "UTILISATEUR.MEL": "email",
    }

    LOGIN_URL = "/accounts/cerbere-login"

SENTRY_URL = get_env_variable("SENTRY_URL")

if SENTRY_URL:
    # opened issue on Sentry package : https://github.com/getsentry/sentry-python/issues/1081
    # it should be solved in a further release
    # pylint: disable=E0110
    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.05,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": decouple.config("REDIS_URL", default="redis://redis:6379"),
    },
    "MIDDLEWARE": [
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}

# limit reach when an operation has 167 logements
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
