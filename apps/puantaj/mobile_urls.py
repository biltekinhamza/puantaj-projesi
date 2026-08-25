from django.urls import path

from apps.puantaj import mobile_views

urlpatterns = [
    path("", mobile_views.mobil_puantaj, name="mobil_puantaj"),
    path("durum-kaydet/", mobile_views.mobil_durum_kaydet, name="mobil_durum_kaydet"),
    path("gunu-tamamla/", mobile_views.mobil_gunu_tamamla, name="mobil_gunu_tamamla"),
]
