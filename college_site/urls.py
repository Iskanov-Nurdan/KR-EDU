import re
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve as serve_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # set_language endpoint
    path('', include('main.urls')),
]

# django.conf.urls.static.static() is a no-op when DEBUG=False, so it can't
# be used here: this project runs via `runserver` behind ngrok rather than a
# real reverse proxy/whitenoise setup, and uploaded files must stay reachable
# even with DEBUG=False. Call the underlying view directly instead. Static
# files are handled separately by `runserver --insecure`.
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve_static,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
