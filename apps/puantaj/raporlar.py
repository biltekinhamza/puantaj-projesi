from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from apps.ek_kazanc.models import Mesai
from apps.personel.models import Personel
from apps.puantaj.maas_hakedis_raporlar import donemde_calisanlar
from apps.puantaj.services.puantaj_service import PuantajService

@dataclass
class TopluHakedisRow:
    personel: Personel
    hakedis_gun: Decimal
    resmi_tatil_gun: Decimal
    hafta_sonu_gun: Decimal
    toplam_gun: Decimal

def _mesai_gunu(mesailer, tur):
    return sum(
        (Decimal(str(m.gun_orani if m.gun_orani is not None else 1)) for m in mesailer if m.tur == tur),
        Decimal("0"),
    )

def _hakedis_gunlerini_ayir(hak_edilen_gun, resmi_tatil_gun, hafta_sonu_gun):
    hakedis_gun = max(
        Decimal(str(hak_edilen_gun)) - resmi_tatil_gun - hafta_sonu_gun,
        Decimal("0"),
    )
    return hakedis_gun, hakedis_gun + resmi_tatil_gun + hafta_sonu_gun

def _sirket_hafta_sonu_gunu(puantaj_service):
    if not puantaj_service.gecerli_aralik_var():
        return Decimal("0")
    kod_map = {puantaj.tarih: puantaj.kod for puantaj in puantaj_service.puantajlar}
    gun_sayisi = (puantaj_service.bitis - puantaj_service.baslangic).days + 1
    return Decimal(str(sum(
        1 for i in range(gun_sayisi)
        if (tarih := puantaj_service.baslangic + timedelta(days=i)).weekday() == 6
        and kod_map.get(tarih) not in ("U", "X")
    )))

def _toplam_puantaj_gunu(puantaj_service, hafta_sonu_gun):
    ucretli_gun = puantaj_service.ucretli_gun()
    if puantaj_service.personel.personel_turu != "sirket":
        return ucretli_gun

    isaretli_hafta_sonu = Decimal("0")
    for puantaj in puantaj_service.puantajlar:
        if puantaj.tarih.weekday() != 6:
            continue
        if puantaj.kod in ("G", "İ"):
            isaretli_hafta_sonu += Decimal("1")
        elif puantaj.kod == "Y":
            isaretli_hafta_sonu += Decimal("0.5")

    otomatik_eklenecek = max(hafta_sonu_gun - isaretli_hafta_sonu, Decimal("0"))
    return min(ucretli_gun + otomatik_eklenecek, Decimal("30"))

def toplu_hakedis_hesapla(baslangic, bitis):
    rows = []
    for personel in donemde_calisanlar(baslangic, bitis):
        ps = PuantajService(personel, baslangic, bitis)
        mesailer = Mesai.objects.filter(personel=personel, tarih__range=(baslangic, bitis), aktif=True)
        resmi_tatil_gun = _mesai_gunu(mesailer, "RESMI_TATIL")
        if personel.personel_turu == "sirket":
            hafta_sonu_gun = _sirket_hafta_sonu_gunu(ps)
        else:
            hafta_sonu_gun = _mesai_gunu(mesailer, "PAZAR")
        toplam_puantaj_gun = _toplam_puantaj_gunu(ps, hafta_sonu_gun)
        hakedis_gun, toplam_gun = _hakedis_gunlerini_ayir(
            toplam_puantaj_gun, resmi_tatil_gun, hafta_sonu_gun
        )
        rows.append(TopluHakedisRow(
            personel=personel,
            hakedis_gun=hakedis_gun,
            resmi_tatil_gun=resmi_tatil_gun,
            hafta_sonu_gun=hafta_sonu_gun,
            toplam_gun=toplam_gun,
        ))
    return rows
