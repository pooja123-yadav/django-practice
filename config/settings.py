from config.common import *
import os
import environ

ENV = "PRODUCTION"
DEBUG = True

env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') 

TIME_ZONE = 'Asia/Kolkata'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',
        'NAME'      : env('DB_NAME'),
        'USER'      : env('DB_USER'),
        'PASSWORD'  : env('DB_PASSWORD'),
        "HOST"      : env('DB_HOST'),
        'PORT'      : env('DB_PORT'),
        'TIME_ZONE' : TIME_ZONE
    }
}

