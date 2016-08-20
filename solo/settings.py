import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)


STRIPE_KEYS = {
	'API_KEY': 'sk_live_0MKUXgCdCSMYf1dDhBZI4BOJ',
	'PUBLIC_KEY': 'pk_live_Cs5ppryF0Sg6wteG4y7Kri88',
	'CLIENT_ID': 'ca_8IFnisGC3UegfN3ZnNqRxGSRB2DIzMb1',
}

# For dev
# STRIPE_KEYS = {
# 	'API_KEY': 'sk_test_QqlkG4EYvRku2zvzrZRksmwJ',
# 	'PUBLIC_KEY': 'pk_test_egZpQehcB86xWgcr0n1eZluM',
# 	'CLIENT_ID': 'ca_8IFn5chY6QPiJ4ayx9roSbAqrIA5tZgx',
# }

# twilio credentials
TWILIO_ACCOUNT_SID = "ACb311a23eddf63e73d3812c07921b540c" 
TWILIO_AUTH_TOKEN = "6bf4a906976eb9f31d683dd336be4784" 


STATIC_ROOT = os.path.join(PROJECT_APP, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = ["static",]
#STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
#STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

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

f = os.path.join(PROJECT_APP_PATH, "local_settings.py")
if os.path.exists(f):
    import sys
    import imp
    module_name = "%s.local_settings" % PROJECT_APP
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())

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

EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJQWFUMH5MCIHX52Q' #'ses-smtp-user.20160616-182855'
EMAIL_HOST_PASSWORD = 'AlETX02PSbQI8a46g7RL/cN7lbzF9sBHbOTag+TUOxxv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@getfreshbaked.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'