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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from trommelkreis import views

urlpatterns = [
    path("", views.home),
    path("home/", views.home),
    path("info/", views.info),
    path("upload/", views.upload, name="upload"),
    path("upload/checkpassword/", views.check_password),
    path("abo/", views.subscribe),
    path("archiv/", include("archive.urls")),
    path("admin/", admin.site.urls),
    # Serve MEDIA files through Django (DEBUG only):
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
