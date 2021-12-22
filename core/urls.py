"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import SITEMAPS

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("bailleurs/", include(("bailleurs.urls", "bailleurs"), namespace="bailleurs")),
    path(
        "conventions/",
        include(("conventions.urls", "conventions"), namespace="conventions"),
    ),
    path(
        "instructeurs/",
        include(("instructeurs.urls", "instructeurs"), namespace="instructeurs"),
    ),
    path(
        "programmes/",
        include(("programmes.urls", "programmes"), namespace="programmes"),
    ),
    path("stats/", include(("stats.urls", "stats"), namespace="stats")),
    path("", include(("users.urls", "users"), namespace="users")),
    path("upload/", include(("upload.urls", "upload"), namespace="upload")),
    path("comments/", include(("comments.urls", "comments"), namespace="comments")),
    path("cgu", TemplateView.as_view(template_name="editorial/cgu.html"), name="cgu"),
    path(
        "accessibilite",
        TemplateView.as_view(template_name="editorial/accessibilite.html"),
        name="accessibilite",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(("api.v1.urls", "api"), namespace="apis")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
