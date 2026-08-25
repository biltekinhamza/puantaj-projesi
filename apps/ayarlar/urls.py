from django.urls import path
from . import views
urlpatterns = [
    path("sirket-bilgileri/", views.sirket_bilgileri, name="ayarlar_sirket_bilgileri"),
    path("resmi-tatiller/", views.resmi_tatil_liste, name="ayarlar_resmi_tatil_liste"),
    path("resmi-tatiller/<int:pk>/duzenle/", views.resmi_tatil_duzenle, name="ayarlar_resmi_tatil_duzenle"),
    path("resmi-tatiller/<int:pk>/sil/", views.resmi_tatil_sil, name="ayarlar_resmi_tatil_sil"),
    path("katsayilar/", views.katsayi_liste, name="ayarlar_katsayi_liste"),
    path("katsayilar/<int:pk>/duzenle/", views.katsayi_duzenle, name="ayarlar_katsayi_duzenle"),
]
