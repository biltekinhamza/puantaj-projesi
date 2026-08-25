from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from django.db.models import Q
from apps.ek_kazanc.models import Mesai, Prim
from apps.kesintiler.models import Avans, Icra
from apps.personel.models import Personel
from apps.puantaj.services.maas_service import MaasService
from apps.puantaj.services.puantaj_service import PuantajService

@dataclass
class MaasHakedisRow:
    personel: Personel
    resmi_tatil_gun: Decimal
    hak_edilen_gun: Decimal
    hak_edilen_maas: Decimal
    mesai_saat: Decimal
    mesai_tutar: Decimal
    prim_tutar: Decimal
    avans_tutar: Decimal
    icra_tutar: Decimal
    net_odenecek: Decimal

def donemde_calisanlar(baslangic: date, bitis: date):
    return Personel.objects.filter(ise_giris_tarihi__lte=bitis).filter(Q(isten_cikis_tarihi__isnull=True) | Q(isten_cikis_tarihi__gte=baslangic)).order_by("ad_soyad")

def _topla(qs, attr="tutar"):
    toplam = Decimal("0")
    for x in qs:
        toplam += Decimal(str(getattr(x, attr) or 0))
    return toplam

def _resmi_tatil_gunu(mesailer):
    return sum(
        (Decimal(str(m.gun_orani if m.gun_orani is not None else 1)) for m in mesailer if m.tur == "RESMI_TATIL"),
        Decimal("0"),
    )

def _resmi_tatil_dusulmus_hak_gunu(hak_edilen_gun, resmi_tatil_gun):
    return max(Decimal(str(hak_edilen_gun)) - resmi_tatil_gun, Decimal("0"))

def maas_hakedis_hesapla(baslangic: date, bitis: date):
    personeller = donemde_calisanlar(baslangic, bitis)
    rows = []
    for personel in personeller:
        ps = PuantajService(personel, baslangic, bitis)
        ms = MaasService(personel, baslangic, bitis)
        mesailer = Mesai.objects.filter(personel=personel, tarih__range=(baslangic, bitis), aktif=True)
        primler = Prim.objects.filter(personel=personel, tarih__range=(baslangic, bitis), aktif=True)
        avanslar = Avans.objects.filter(personel=personel, tarih__range=(baslangic, bitis))
        icralar = Icra.objects.filter(personel=personel, tarih__range=(baslangic, bitis))
        resmi_tatil_gun = _resmi_tatil_gunu(mesailer)
        hak_edilen_gun = _resmi_tatil_dusulmus_hak_gunu(ps.hak_edilen_gun(), resmi_tatil_gun)
        # Resmi tatil, raporda normal gunden ayrilir; ana maastan kesilmez.
        hak_edilen_maas = ms.brut_hakedis()
        mesai_saat = sum(Decimal(str(m.saat or 0)) for m in mesailer)
        mesai_tutar = _topla(mesailer)
        prim_tutar = _topla(primler)
        avans_tutar = _topla(avanslar)
        icra_tutar = _topla(icralar)
        rows.append(MaasHakedisRow(
            personel=personel,
            resmi_tatil_gun=resmi_tatil_gun,
            hak_edilen_gun=hak_edilen_gun,
            hak_edilen_maas=hak_edilen_maas,
            mesai_saat=mesai_saat,
            mesai_tutar=mesai_tutar,
            prim_tutar=prim_tutar,
            avans_tutar=avans_tutar,
            icra_tutar=icra_tutar,
            net_odenecek=hak_edilen_maas + mesai_tutar + prim_tutar - avans_tutar - icra_tutar,
        ))
    return rows
