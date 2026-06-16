import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'



ALLOWED_HOSTS = [
    h.strip() for h in os.getenv(
        'ALLOWED_HOSTS', 'localhost,127.0.0.1'
    ).split(',') if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    'https://faucet-vacancy-grit.ngrok-free.dev',
    'http://faucet-vacancy-grit.ngrok-free.dev',
]

INSTALLED_APPS = [
    'jazzmin',
    'modeltranslation',          # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'main.middleware.RateLimitMiddleware',  # basic per-IP flood / brute-force throttling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Enables language switching
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'college_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # Exposes LANGUAGES to templates
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'college_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('ky', 'Кыргызча'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# ── Static & media ───────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# ── Security hardening ────────────────────────────────────────────────────────
# ngrok terminates TLS and forwards plain HTTP — trust its proto header so
# Django's request.is_secure() reports correctly (CSRF / secure-cookie logic).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = 'DENY'                       # blocks clickjacking via <iframe>
SECURE_CONTENT_TYPE_NOSNIFF = True             # stops MIME-sniffing attacks
SECURE_REFERRER_POLICY = 'same-origin'
CSRF_COOKIE_HTTPONLY = True                    # CSRF cookie unreadable by JS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Caps request body size so oversized payloads can't be used to exhaust memory
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB

# Per-IP request throttling (see main/middleware.py) — blunts brute-force
# login attempts and single-source flooding. NOTE: this does not stop
# distributed/volumetric DDoS — that must be mitigated at the network edge
# (Cloudflare, ngrok, a real reverse proxy with rate limiting, etc.).
RATELIMIT_GENERAL = (120, 60)   # 120 requests / 60s per IP, site-wide
RATELIMIT_STRICT = (10, 60)     # 10 requests / 60s per IP, for sensitive paths
RATELIMIT_STRICT_PATHS = ('/admin/login/', '/i18n/setlang/')

# ── TinyMCE ──────────────────────────────────────────────────────────────────
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'menubar': 'file edit view insert format tools table',
    'plugins': (
        'advlist autolink lists link image charmap preview anchor '
        'searchreplace visualblocks code fullscreen insertdatetime '
        'media table code help wordcount'
    ),
    'toolbar': (
        'undo redo | formatselect | bold italic underline | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | link image | '
        'removeformat | code fullscreen'
    ),
    'content_css': False,
    'skin': 'oxide',
    'promotion': False,
    'language': 'ru',
}
TINYMCE_SPELLCHECKER = False

# ── Jazzmin ──────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "КА Колледж · Админ",
    "site_header": "КА Региональный Колледж",
    "site_brand": "Администрация",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "welcome_sign": "Добро пожаловать в панель управления",
    "copyright": "Кочкор-Атинский региональный колледж",
    "search_model": ["main.News", "main.Specialty", "main.Document"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "🌐 Открыть сайт", "url": "/", "new_window": True},
        {"name": "📰 Новости", "url": "/admin/main/news/"},
        {"name": "🖼 Галерея", "url": "/admin/main/gallery/"},
    ],
    "usermenu_links": [
        {"name": "🌐 Сайт", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "main.SiteSettings",
        "main.CollegeInfo",
        "main.MinistryPage",
        "main.Specialty",
        "main.News",
        "main.GalleryCategory",
        "main.Gallery",
        "main.Admission",
        "main.Document",
        "main.Contact",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "main": "fas fa-hospital-alt",
        "main.SiteSettings": "fas fa-cog",
        "main.News": "fas fa-newspaper",
        "main.Specialty": "fas fa-graduation-cap",
        "main.Gallery": "fas fa-images",
        "main.GalleryCategory": "fas fa-folder-open",
        "main.Contact": "fas fa-phone-alt",
        "main.CollegeInfo": "fas fa-university",
        "main.Admission": "fas fa-file-alt",
        "main.Document": "fas fa-file-pdf",
        "main.MinistryPage": "fas fa-landmark",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}
