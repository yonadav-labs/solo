import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)


# STRIPE_KEYS = {
#     'API_KEY': 'sk_test_1AFSPD5Dg8RihyPPtylWiSsR',
#     'PUBLIC_KEY': 'pk_test_Q4RGBzPFhWbMP2daCqMg6Rj7',
#     'CLIENT_ID': 'ca_8Qcy5FPjST3HuFl7xXjisiodyjKE5d8V',
# }



STRIPE_KEYS = {
	'API_KEY': 'sk_test_QqlkG4EYvRku2zvzrZRksmwJ',
	'PUBLIC_KEY': 'pk_test_egZpQehcB86xWgcr0n1eZluM',
	'CLIENT_ID': 'ca_8IFn5chY6QPiJ4ayx9roSbAqrIA5tZgx',
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '))*bdzp8!4)acc45^ms4(srw%nh8^yt+_55775y&9zt%i3rx_i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

MEDIA_URL = STATIC_URL + "/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.gis',
	'django.contrib.sites',
	
	'seller',
	
	# stripe authentication through allauth
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.stripe',
	
]

# add login redirect
# sign up form for sellers
LOGIN_REDIRECT_URL = '/seller' 


MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'solo.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(PROJECT_ROOT, "templates")],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.static',
				'django.contrib.messages.context_processors.messages',
				
			],
		},
	},
]

WSGI_APPLICATION = 'solo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'solo2',
		'USER': 'postgres',
		'PASSWORD': 'pbn6h9E',
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


## stripe allauth and socialauth
SITE_ID = 1

#################################################################
# allauth settings for social connections

# source: https://realpython.com/blog/python/adding-social-authentication-to-django/
AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)


# dictionary containing provider specific settings.
SOCIALACCOUNT_PROVIDERS = {
	'stripe': {
		'SCOPE': ['read_write',],
	}
}

# attempt to bypass the signup form by using fields (e.g. username, email) 
# retrieved from the social account provider. If a conflict arises due to a 
# duplicated e-mail the signup form will still kick in
SOCIALACCOUNT_AUTO_SIGNUP = True

AUTH_USER_MODEL = 'seller.Seller'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jason50010001@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'jason50010001@gmail.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
