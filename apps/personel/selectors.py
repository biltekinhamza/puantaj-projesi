from datetime import date
from django.db.models import Q
from .models import Personel

def ay_icinde_calisanlar(baslangic: date, bitis: date):
    return Personel.objects.filter(ise_giris_tarihi__lte=bitis).filter(
        Q(isten_cikis_tarihi__isnull=True) | Q(isten_cikis_tarihi__gte=baslangic)
    ).order_by("ad_soyad")

def tarihte_calisanlar(tarih: date | None = None):
    tarih = tarih or date.today()
    return Personel.objects.filter(ise_giris_tarihi__lte=tarih).filter(
        Q(isten_cikis_tarihi__isnull=True) | Q(isten_cikis_tarihi__gte=tarih)
    ).order_by("ad_soyad")
