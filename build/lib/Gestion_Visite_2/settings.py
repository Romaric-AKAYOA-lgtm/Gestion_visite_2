from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fs_*)x*mc#pu_fr(+i(^0vt&i_fhc$#^ue5^g@(q9!5ap9jfl3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'directeur',
    'secretaire',
    'visiteur',
    'visite',
    'programme_visite',
    'Activation',
    'administration',
    'connection',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Activation.activation_middleware.ActivationMiddleware',
            
]

ROOT_URLCONF = 'Gestion_Visite_2.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 # Ajouter le context processor de votre application 'activation'
                 'Activation.context_processors.check_activation',  # Vérifiez ce chemin
                # Ajouter le context processor de votre application 'administration'
                'administration.context_processors.administration',  # Vérifiez ce chemin
                # 'connecton.context_processors.user_info',  # Vérifiez ce chemin si nécessaire
            ],
        },
    },
]

WSGI_APPLICATION = 'Gestion_Visite_2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""     
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Gestion_visite_2_INRAP_db',  # Remplace par le nom de ta base
        'USER': 'root',  # Par défaut dans XAMPP
        'PASSWORD': '',  # Laisse vide si aucun mot de passe
        'HOST': 'localhost',  
        'PORT': '3306',  
          'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
# Si tu utilises des fichiers statiques en développement
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Assure-toi que ce chemin pointe vers ton dossier 'static' principal
]

# En production, spécifie un dossier pour collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'transactions.log'),
            'formatter': 'detailed',
        },
    },
    'formatters': {
        'detailed': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'transactions': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
