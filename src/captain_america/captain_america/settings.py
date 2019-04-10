# -*- coding: utf-8 -*-
"""
Django settings for captain_america project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ox^v4pgl_5gctmi#1b$h(&@4ppiz^kxmbz1-#z3bnx!g3*boc^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'captain_america',
    'spider',
    'warehouse'
    # 'push'
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

ROOT_URLCONF = 'captain_america.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'captain_america.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '39.105.194.66',
        'PORT': '3306',
        'NAME': 'hero_test',
        'USER': 'root',
        'PASSWORD': '123456',
        # 'OPTIONS': {
        #     "init_command": "SET foreign_key_checks = 0;"
        # }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
TIME_FORMAT = "H:i:s"
DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Format
MODEL_OBJECT_DISPLAY = u'{0}_{1}'

# Suit
SUIT_CONFIG = {
    'ADMIN_NAME': u'美国队长',
    'MENU': (
        {
            'app': 'auth',
            'icon': 'icon-lock',
            'models': ('user', 'group')
         },
        {
            'label': u'爬虫',
            'app': 'spider',
            'models': ('Site', 'Control', 'Channel', 'Task')
        },
        {
            'label': u'仓库',
            'app': 'warehouse',
            'models': ('User', 'Video', 'Tag', 'VideoTag')
        }
    ),
}

CRONJOBS = [  # 定时任务列表
    ('47 11 * * *', 'django.core.management.run_spiders', [], {}, '>> /var/run.log'),
]

# Commands
COLONIST_INTERVAL = 10
COLONIST_CRONTAB_COMMENT = 'captain_america.spider.models.control.id ==> {0}'

# Spider Project
SPIDER_PROJECT_NAME = 'spider_man'
SPIDER_PROJECT_SCRIPT = 'run.sh'
