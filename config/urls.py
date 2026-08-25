from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.puantaj import server_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", server_views.server_dashboard, name="anasayfa"),
    path("server/durum/", server_views.server_dashboard_api, name="server_dashboard_api"),
    path("personel/", include("apps.personel.urls")),
    path("puantaj/", include("apps.puantaj.urls")),
    path("mobil/", include("apps.puantaj.mobile_urls")),
    path("ek-kazanc/", include("apps.ek_kazanc.urls")),
    path("kesintiler/", include("apps.kesintiler.urls")),
    path("raporlar/", include("apps.raporlar.urls")),
    path("ayarlar/", include("apps.ayarlar.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
