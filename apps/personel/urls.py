from django.urls import path
from .views import (
    personel_liste,
    personel_ekle,
    personel_guncelle,
    personel_bilgi_raporu,
    personel_bilgi_excel,
    personel_maas_zarfi,
    istifa_dilekcesi, 
   
)

from .views_sozlesme import (
    personel_sozlesme_sec,
    personel_belirli_sureli_sozlesme,
    personel_belirli_sureli_sozlesme_pdf,
)
from .views import devamsizlik_tutanagi_sec, devamsizlik_tutanagi

urlpatterns = [
    # PERSONEL
    path("", personel_liste, name="personel_liste"),
    path("yeni/", personel_ekle, name="personel_ekle"),
    path("<int:pk>/guncelle/", personel_guncelle, name="personel_guncelle"),
    path("istifa-dilekcesi/", istifa_dilekcesi, name="istifa_dilekcesi"),
    path("devamsizlik-tutanagi/", devamsizlik_tutanagi_sec, name="devamsizlik_tutanagi_sec"),
    path("devamsizlik-tutanagi/yazdir/", devamsizlik_tutanagi, name="devamsizlik_tutanagi"),

    # RAPORLAR
    path(
        "raporlar/personel-bilgi/",
        personel_bilgi_raporu,
        name="personel_bilgi_raporu",
    ),
    path(
        "raporlar/personel-bilgi/excel/",
        personel_bilgi_excel,
        name="personel_bilgi_excel",
    ),

    # SÖZLEŞME
    path("sozlesme-sec/", personel_sozlesme_sec, name="personel_sozlesme_sec"),
    path("<int:pk>/sozlesme/", personel_belirli_sureli_sozlesme, name="personel_sozlesme"),
    path(
        "<int:pk>/sozlesme/pdf/",
        personel_belirli_sureli_sozlesme_pdf,
        name="personel_sozlesme_pdf",
    ),

    # MAAŞ / EVRAK ZARFI
    path("maas-zarfi/", personel_maas_zarfi, name="personel_maas_zarfi"),

    
]
