"""
Django settings for modern Blog CMS project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')   # We'll set this in Render

DEBUG = False

ALLOWED_HOSTS = ['*']   # We'll change this later to your actual domain

INSTALLED_APPS = [
    # Unfold Admin Theme - Must come before django.contrib.admin
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party packages
    'django_ckeditor_5',
    'taggit',
    'django_cleanup.apps.CleanupConfig',

    # Our app
    'blog',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.config.wsgi.application'

# ====================== DATABASE ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # Using SQLite for easy start
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ====================== STATIC & MEDIA ======================
# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ====================== DEFAULT AUTO FIELD ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================== UNFOLD (Modern Admin Panel) ======================
UNFOLD = {
    "SITE_TITLE": "Blog CMS Admin",
    "SITE_HEADER": "Modern Blog CMS",
    "SITE_BRANDING": "Blog CMS",
    "title": "Comments",
    "icon": "comment",
    "link": "admin:blog_comment_changelist",

    "COLORS": {
        "primary": {
            "50": "#f0f9ff",
            "100": "#e0f2fe",
            "200": "#bae6fd",
            "300": "#7dd3fc",
            "400": "#38bdf8",
            "500": "#0ea5e9",
            "600": "#0284c8",
            "700": "#0369a1",
            "800": "#075985",
            "900": "#0c4a6e",
            "950": "#082f49",
        },
    },

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Content Management",
                "separator": True,
                "items": [
                    {
                        "title": "All Posts",
                        "icon": "article",
                        "link": "admin:blog_post_changelist",
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": "admin:blog_category_changelist",
                    },
                    {
                        "title": "Tags",
                        "icon": "label",
                        "link": "admin:taggit_tag_changelist",
                    },
                ],
            },
        ],
    },
}

# ====================== CKEDITOR 5 CONFIG ======================
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 
            'numberedList', 'blockQuote', '|', 'imageUpload', 
            'insertTable', 'mediaEmbed', '|', 'undo', 'redo'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', '|', 'imageStyle:alignLeft',
                'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side'
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells']
        },
        'height': '500px',
    }
}

CKEDITOR_5_UPLOAD_PATH = "ckeditor_uploads/"

# ====================== OTHER SETTINGS ======================
SITE_ID = 1

# Debug Toolbar (only in development)
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
