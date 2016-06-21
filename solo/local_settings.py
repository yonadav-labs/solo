# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

# DEBUG = False
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "6@!6yreauz&k4)(4(((jq@17w@_mcr9bzu49%7%=vuze_!3f8!"
NEVERCACHE_KEY = "-&outap0_#5%035lkznw1rd5okape@jnup2!b*ezpu$g%v(#dv"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "solo",
        "USER": "postgres",
        "PASSWORD": "pbn6h9E",
    }
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["www.getfreshbaked.com", "getfreshbaked.com", "localhost"] 
# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

FABRIC = {
    "DEPLOY_TOOL": "git",  
    "SSH_USER": "ubuntu",  
    "SSH_KEY_PATH": "testkey.pem",
    "VIRTUALENV_HOME":  "/home/ubuntu/do", 
    "PROJECT_NAME": "solo", 
    "GUNICORN_PORT": 8000, 
    "REPO_URL": "https://jason5001001@bitbucket.org/cflproject2016/solo.git", 
    "HOSTS": ["54.67.42.100",],  # The IP address of your VPS
    "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
    "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
    "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
    "DB_PASS": "pbn6h9E",  # Live database password
    "ADMIN_PASS": "u83jiEVT;i?",  # Live admin user password
    "SECRET_KEY": SECRET_KEY,
    "NEVERCACHE_KEY": NEVERCACHE_KEY,
}
