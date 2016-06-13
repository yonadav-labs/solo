from solo.settings.common import *

INSTALLED_APPS += ('storages',)
AWS_STORAGE_BUCKET_NAME = "s3-test-bucket-us-west-06-13-2016"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL


DATABASES = {    
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Solo',
        'USER' : 'postgres',
        'PASSWORD' : 'nekner16',
        'HOST' : 'mydbinstance.c4cdttulc2bc.us-west-1.rds.amazonaws.com',
        'PORT' : '5432',
    }
}

