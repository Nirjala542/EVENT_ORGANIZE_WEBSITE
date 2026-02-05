import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / '.env'

# #region agent log
try:
    from pathlib import Path as _Path
    LOG_DIR = _Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
    LOG_FILE = LOG_DIR / 'debug.log'
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    env_file_exists = DOTENV_PATH.exists()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"B","location":"settings.py:12","message":"Checking .env file existence","data":{"env_file_exists":env_file_exists,"env_path":str(DOTENV_PATH)}, "timestamp":int(__import__('time').time()*1000)})+'\n')
except:
    pass
# #endregion

# Always load .env from project root (works even if runserver started elsewhere)
load_dotenv(dotenv_path=DOTENV_PATH)

# #region agent log
try:
    from pathlib import Path as _Path
    LOG_DIR = _Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
    LOG_FILE = LOG_DIR / 'debug.log'
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"B","location":"settings.py:25","message":"load_dotenv executed","data":{"dotenv_path":str(DOTENV_PATH)}, "timestamp":int(__import__('time').time()*1000)})+'\n')
except:
    pass
# #endregion

SECRET_KEY = 'replace-this-in-production'

DEBUG = True

ALLOWED_HOSTS = []

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# #region agent log
try:
    from pathlib import Path as _Path
    LOG_DIR = _Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
    LOG_FILE = LOG_DIR / 'debug.log'
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"settings.py:35","message":"GEMINI_API_KEY loaded from environment","data":{"api_key_length":len(GEMINI_API_KEY) if GEMINI_API_KEY else 0,"api_key_empty":not bool(GEMINI_API_KEY),"api_key_preview":GEMINI_API_KEY[:10]+"..." if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10 else GEMINI_API_KEY},"timestamp":int(__import__('time').time()*1000)})+'\n')
except: pass
# #endregion

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'book_my_event.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'book_my_event.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email - default to console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
