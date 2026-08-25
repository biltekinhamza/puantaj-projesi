from django.urls import path
from . import views
urlpatterns = [
    path("", views.puantaj_taslak, name="hakedis"),
    path("raporlar/", views.raporlar_index, name="raporlar_index"),
    path("raporlar/toplu-hakedis/", views.toplu_hakedis_raporu, name="toplu_hakedis_raporu"),
    path("raporlar/maas-hakedis/", views.maas_hakedis_raporu, name="maas_hakedis_raporu"),
    path("raporlar/banka-elden/", views.banka_elden_listesi, name="banka_elden_listesi"),
    path("raporlar/personel-detay/", views.personel_detay_raporu, name="personel_detay_raporu"),
]
