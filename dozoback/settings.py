from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-rbl+!03h2&$1x0t6s+=o0yh+w=aghg7i6@yd3szlh&th)l$*_6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['dozo01.pythonanywhere.com', 'dozo-jade.vercel.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Dozo',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Añadir CORS middleware al principio
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = False  # Cambiar a False para mayor seguridad
CORS_ALLOWED_ORIGINS = [
    'https://dozo-jade.vercel.app',  # Dominio de tu frontend en Vercel
    'https://dozo01.pythonanywhere.com',  # Dominio en PythonAnywhere
]

CORS_ALLOW_CREDENTIALS = True  # Permitir cookies/sesiones si es necesario

CSRF_TRUSTED_ORIGINS = [
    'https://dozo-jade.vercel.app',  # Confianza para solicitudes CSRF
    'https://dozo01.pythonanywhere.com',
]

# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'panzzz956@gmail.com'
EMAIL_HOST_PASSWORD = 'dudu xlda xvyf byrd'  # Cambia por tu contraseña o usa variables de entorno en producción
DEFAULT_FROM_EMAIL = 'Dozo <panzzz956@gmail.com>'

ROOT_URLCONF = 'dozoback.urls'

AUTH_USER_MODEL = 'Dozo.CustomUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dozoback.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True


# Archivos estáticos y multimedia
STATIC_URL = '/static/'
STATIC_ROOT = '/home/dozo01/static'  # Ruta para PythonAnywhere
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/dozo01/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/dozo01/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
