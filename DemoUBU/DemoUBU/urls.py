from django.urls import include, path
from maindemo.admin import demo_site
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("", include("maindemo.urls")),
    path("AdminLogin/", demo_site.urls),
] + static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)