"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-iii1!65$kdq^=#cm)$utv&@lj-%_52gr8ucalwhiqk=j_5-&_e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
    # Note for future: If we go to production and set Debug to False:
    # Will need to run `python manage.py collectstatic` to collect all static files...
    # https://docs.djangoproject.com/en/5.0/howto/static-files/#deployment


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # our own custom made apps
    'users',

    # third party apps

    # Temporary 3rd party UI for allauth - We should add our own custom UI later
    # https://github.com/danihodovic/django-allauth-ui
    "allauth_ui", # Needs to be added before allauth

    # will use django-allauth for authentication (both regular and social accounts such as google)
    # https://docs.allauth.org/en/latest/introduction/index.html
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # More third party apps
    "widget_tweaks", # dependency for allauth_ui
    "phonenumber_field", # for phone number field in user model

    # apps that come with Django by default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Allauth needs this as well as some that were already added by default
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # 'DIRS': [],
        # Doing this allows us to override allauth templates or other templates 
        # Django will look in our templates folder (project/templates) first before looking in other template folders
        'DIRS': [BASE_DIR / 'templates'], 
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request' 
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django allauth also needs these backends 
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Note this is technically not the best practice but maybe fine in our case
# See https://docs.djangoproject.com/en/5.0/topics/i18n/timezones/
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication/User Settings
AUTH_USER_MODEL = 'users.User' # Let Django know which model represents a User
ACCOUNT_EMAIL_REQUIRED = True # Require the user to enter a email address when signing up
LOGIN_REDIRECT_URL = 'users:profile' # redirect to users/profile page after login
ACCOUNT_AUTHENTICATION_METHOD = 'email' # Use email to login
ACCOUNT_USERNAME_REQUIRED = False # Don't require a Username
SOCIALACCOUNT_AUTO_SIGNUP = False # Don't automatically sign up social accounts
# Use our custom forms for allauth
ACCOUNT_FORMS = {'signup': 'users.forms.MyCustomSignupForm'}
SOCIALACCOUNT_FORMS = {'signup': 'users.forms.MyCustomSocialSignupForm'}

SOCIALACCOUNT_ADAPTER = 'users.adapter.CustomSocialAccountAdapter' # Use our custom adapter for social accounts

# Let allauth know not to use username for representing a user
# Still defaults to username unless user __str__ method is overwriten
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Could also specify another name for the user to be displayed in email or message framework messages
# ACCOUNT_USER_DISPLAY = lambda user: user.some_function() 

# Set up email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cohabitat.ru@gmail.com'
EMAIL_HOST_PASSWORD = 'oypgzzgdkiuaogry' # This is a google app password (not the gmail password)

