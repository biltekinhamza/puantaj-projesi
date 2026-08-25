from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase
from django.core.exceptions import PermissionDenied

from apps.puantaj.mobile_views import MOBIL_KODLAR, _mobil_yetkisini_kontrol_et
from apps.puantaj.maas_hakedis_raporlar import _resmi_tatil_dusulmus_hak_gunu, _resmi_tatil_gunu
from apps.puantaj.raporlar import (
    _hakedis_gunlerini_ayir,
    _mesai_gunu,
    _sirket_hafta_sonu_gunu,
    _toplam_puantaj_gunu,
)
from apps.puantaj.services.maas_service import MaasService
from apps.puantaj.services.puantaj_service import PuantajService
from apps.puantaj.views import _parse_decimal_input


class OtuzGunSiniriTest(SimpleTestCase):
    def _puantaj_servisi(self, personel_turu):
        servis = PuantajService.__new__(PuantajService)
        servis.personel = SimpleNamespace(personel_turu=personel_turu)
        servis.puantajlar = [SimpleNamespace(kod="G") for _ in range(31)]
        return servis

    def test_taseron_ucretli_ve_hak_edilen_gun_30_ile_sinirlanir(self):
        puantaj = self._puantaj_servisi("taseron")
        maas = MaasService.__new__(MaasService)
        maas.personel = SimpleNamespace(
            personel_turu="taseron",
            gunluk_yevmiyesi=Decimal("935.85"),
        )
        maas.puantaj_service = puantaj

        self.assertEqual(puantaj.ucretli_gun(), Decimal("30"))
        self.assertEqual(puantaj.gorunen_toplam_gun(), Decimal("30"))
        self.assertEqual(puantaj.hak_edilen_gun(), Decimal("30"))
        self.assertEqual(maas.brut_hakedis(), Decimal("28075.50"))

    def test_sirket_personelinin_gorunen_gunu_de_30_ile_sinirlanir(self):
        puantaj = self._puantaj_servisi("sirket")

        self.assertEqual(puantaj.gorunen_toplam_gun(), Decimal("30"))

    def test_sirket_personelinin_fiilen_calistigi_gun_eksik_gunlerle_sifirlanmaz(self):
        puantaj = PuantajService.__new__(PuantajService)
        puantaj.gecerli_aralik_var = lambda: True
        puantaj._tam_ay_calisan_mi = lambda: True
        puantaj.eksik_gun = lambda: Decimal("30")
        puantaj.ucretli_gun = lambda: Decimal("1")

        self.assertEqual(puantaj.sirket_maas_gunu(), Decimal("1"))


class MaasHakedisRaporuTest(SimpleTestCase):
    def test_resmi_tatil_gun_oranlarini_toplar(self):
        mesailer = [
            SimpleNamespace(tur="RESMI_TATIL", gun_orani=Decimal("1.00")),
            SimpleNamespace(tur="RESMI_TATIL", gun_orani=Decimal("0.50")),
            SimpleNamespace(tur="NORMAL", gun_orani=None),
        ]

        self.assertEqual(_resmi_tatil_gunu(mesailer), Decimal("1.50"))

    def test_resmi_tatil_hak_edilen_gunden_dusulur(self):
        hak_edilen_gun = _resmi_tatil_dusulmus_hak_gunu(Decimal("30"), Decimal("1"))

        self.assertEqual(hak_edilen_gun, Decimal("29"))

    def test_resmi_tatil_ayrilirken_ana_maas_azalmaz(self):
        maas = MaasService.__new__(MaasService)
        maas.personel = SimpleNamespace(personel_turu="sirket", aylik_maas=Decimal("55000.00"))
        maas.puantaj_service = SimpleNamespace(sirket_maas_gunu=lambda: Decimal("30"))

        self.assertEqual(maas.brut_hakedis(), Decimal("55000.00"))


class TopluHakedisRaporuTest(SimpleTestCase):
    def _sirket_subat_ozeti(self, yil, ay_gun_sayisi):
        tarihler = [date(yil, 2, gun) for gun in range(1, ay_gun_sayisi + 1)]
        calisma_gunleri = [tarih for tarih in tarihler if tarih.weekday() != 6]
        puantaj = SimpleNamespace(
            personel=SimpleNamespace(personel_turu="sirket"),
            gecerli_aralik_var=lambda: True,
            baslangic=tarihler[0],
            bitis=tarihler[-1],
            puantajlar=[SimpleNamespace(tarih=tarih, kod="G") for tarih in calisma_gunleri],
            ucretli_gun=lambda: Decimal(str(len(calisma_gunleri))),
        )
        hafta_sonu = _sirket_hafta_sonu_gunu(puantaj)
        toplam = _toplam_puantaj_gunu(puantaj, hafta_sonu)
        hakedis, toplam = _hakedis_gunlerini_ayir(toplam, Decimal("0"), hafta_sonu)
        return hakedis, hafta_sonu, toplam

    def test_ozel_gunleri_hakedisten_ayirir(self):
        hakedis_gun, toplam_gun = _hakedis_gunlerini_ayir(
            Decimal("30"), Decimal("1"), Decimal("4")
        )

        self.assertEqual(hakedis_gun, Decimal("25"))
        self.assertEqual(toplam_gun, Decimal("30"))

    def test_mesai_turunun_gun_oranlarini_toplar(self):
        mesailer = [
            SimpleNamespace(tur="PAZAR", gun_orani=Decimal("1.00")),
            SimpleNamespace(tur="PAZAR", gun_orani=Decimal("0.50")),
            SimpleNamespace(tur="RESMI_TATIL", gun_orani=Decimal("1.00")),
        ]

        self.assertEqual(_mesai_gunu(mesailer, "PAZAR"), Decimal("1.50"))

    def test_sirket_personelinin_hafta_sonunu_takvimden_hesaplar(self):
        puantaj = SimpleNamespace(
            gecerli_aralik_var=lambda: True,
            baslangic=date(2026, 7, 1),
            bitis=date(2026, 7, 31),
            puantajlar=[],
        )

        self.assertEqual(_sirket_hafta_sonu_gunu(puantaj), Decimal("4"))

    def test_sirket_personelinin_otomatik_hafta_sonunu_toplama_ekler(self):
        puantaj = SimpleNamespace(
            personel=SimpleNamespace(personel_turu="sirket"),
            puantajlar=[SimpleNamespace(tarih=date(2026, 7, 1), kod="G")],
            ucretli_gun=lambda: Decimal("25"),
        )

        self.assertEqual(_toplam_puantaj_gunu(puantaj, Decimal("4")), Decimal("29"))

    def test_ucretsiz_izin_girilen_pazarlari_hafta_sonuna_eklemez(self):
        pazarlar = [date(2026, 7, gun) for gun in (5, 12, 19, 26)]
        puantaj = SimpleNamespace(
            gecerli_aralik_var=lambda: True,
            baslangic=date(2026, 7, 1),
            bitis=date(2026, 7, 31),
            puantajlar=[SimpleNamespace(tarih=tarih, kod="U") for tarih in pazarlar],
        )

        self.assertEqual(_sirket_hafta_sonu_gunu(puantaj), Decimal("0"))

    def test_28_gunluk_subati_puantaj_esasli_hesaplar(self):
        hakedis, hafta_sonu, toplam = self._sirket_subat_ozeti(2026, 28)

        self.assertEqual(hakedis, Decimal("24"))
        self.assertEqual(hafta_sonu, Decimal("4"))
        self.assertEqual(toplam, Decimal("28"))

    def test_29_gunluk_subati_puantaj_esasli_hesaplar(self):
        hakedis, hafta_sonu, toplam = self._sirket_subat_ozeti(2028, 29)

        self.assertEqual(hakedis, Decimal("25"))
        self.assertEqual(hafta_sonu, Decimal("4"))
        self.assertEqual(toplam, Decimal("29"))


class BankaTutariTest(SimpleTestCase):
    def test_nokta_ve_virgul_ayni_tutari_olusturur(self):
        self.assertEqual(_parse_decimal_input("1250.50"), Decimal("1250.50"))
        self.assertEqual(_parse_decimal_input("1250,50"), Decimal("1250.50"))


class MobilPuantajYetkiTest(SimpleTestCase):
    class _Gruplar:
        def __init__(self, yetkili):
            self.yetkili = yetkili

        def filter(self, **kwargs):
            return self

        def exists(self):
            return self.yetkili

    def test_mobil_grup_uyesi_erisebilir(self):
        user = SimpleNamespace(is_superuser=False, groups=self._Gruplar(True))
        self.assertIsNone(_mobil_yetkisini_kontrol_et(user))

    def test_yetkisiz_kullanici_reddedilir(self):
        user = SimpleNamespace(is_superuser=False, groups=self._Gruplar(False))
        with self.assertRaises(PermissionDenied):
            _mobil_yetkisini_kontrol_et(user)

    def test_mobil_istemci_yalniz_geldi_ucretsiz_izin_gelmedi_kodlarini_kullanir(self):
        self.assertEqual(MOBIL_KODLAR, {"G", "U", "X"})
