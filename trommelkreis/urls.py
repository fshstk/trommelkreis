"""trommelkreis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from trommelkreis import views

urlpatterns = [
    path("", views.index),  # TODO: use a redirect here
    path("home/", views.home, name="home"),
    path("info/", views.info, name="info"),
    path("upload/", include("uploadform.urls")),
    path("archiv/", include("archive.urls")),
    path("admin/", admin.site.urls),
]

# Serve MEDIA files through Django.
# This just does the same thing that static(...) does, but unconditionally.
# (Whereas static() is a no-op unless DEBUG is set.)
# Not generally recommended but probably fine here since we're behind CloudFlare:
urlpatterns += (
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
)

# Serve MEDIA files through Django (DEBUG only):
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar:
urlpatterns += debug_toolbar_urls()
