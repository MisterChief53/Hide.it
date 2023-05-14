# settings.py

# Add the following at the top of the file to import the necessary modules
import os

# Add the following settings to configure the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the following settings to configure your app and installed apps
INSTALLED_APPS = [
    # ...
    'polls',
    # ...
]

# Add the following settings to configure your database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Add the following settings to configure your middleware
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]

# Add the following settings to configure your static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add the following settings to configure your media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
