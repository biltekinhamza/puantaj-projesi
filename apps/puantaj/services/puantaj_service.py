from datetime import date, timedelta
from decimal import Decimal
from apps.puantaj.models import Puantaj

class PuantajService:
    def __init__(self, personel, baslangic: date, bitis: date):
        self.personel = personel
        self.orijinal_baslangic = baslangic
        self.orijinal_bitis = bitis
        self.baslangic = max(baslangic, personel.ise_giris_tarihi)
        # Raporlarda secilen bitis bugunden ileriyse, henuz hak edilmeyen gelecek gunler hesaplanmaz.
        self.bitis = min(bitis, date.today())
        if personel.isten_cikis_tarihi and personel.isten_cikis_tarihi < self.bitis:
            self.bitis = personel.isten_cikis_tarihi
        self.puantajlar = Puantaj.objects.filter(personel=personel, tarih__range=(self.baslangic, self.bitis)) if self.gecerli_aralik_var() else Puantaj.objects.none()

    def gecerli_aralik_var(self):
        return self.baslangic <= self.bitis

    def calisabilir_gun_sayisi(self) -> int:
        if not self.gecerli_aralik_var():
            return 0
        return (self.bitis - self.baslangic).days + 1

    def kod_gunleri(self, kodlar):
        toplam = Decimal("0")
        for p in self.puantajlar.filter(kod__in=kodlar):
            if p.kod == "Y":
                toplam += Decimal("0.5")
            else:
                toplam += Decimal("1")
        return toplam

    def ucretli_gun(self) -> Decimal:
        # Fiili/ekranda gorunecek gun: sadece puantajda isaretlenen hak edilen gunler.
        # G=1, I=1, Y=0.5; U/X/boş=0.
        toplam = Decimal("0")
        for p in self.puantajlar:
            if p.kod in ("G", "İ"):
                toplam += Decimal("1")
            elif p.kod == "Y":
                toplam += Decimal("0.5")
        return min(toplam, Decimal("30"))

    def islenen_gun(self) -> Decimal:
        # Puantajda herhangi bir kod girilen gun sayisi. G/I/U/X=1, Y=0.5.
        toplam = Decimal("0")
        for p in self.puantajlar:
            if p.kod == "Y":
                toplam += Decimal("0.5")
            elif p.kod in ("G", "İ", "U", "X"):
                toplam += Decimal("1")
        return toplam

    def eksik_gun(self) -> Decimal:
        toplam = Decimal("0")
        for p in self.puantajlar:
            if p.kod in ("X", "U"):
                toplam += Decimal("1")
            elif p.kod == "Y" and self.personel.personel_turu == "sirket":
                toplam += Decimal("0.5")
        return toplam

    def devamsiz_gun(self) -> Decimal:
        return Decimal(str(self.puantajlar.filter(kod="X").count()))

    def ucretsiz_izin_gun(self) -> Decimal:
        return Decimal(str(self.puantajlar.filter(kod="U").count()))

    def yarim_gun(self) -> Decimal:
        return Decimal(str(self.puantajlar.filter(kod="Y").count())) * Decimal("0.5")

    def _tum_calisabilir_gunler_islenmis_mi(self) -> bool:
        if not self.gecerli_aralik_var():
            return False
        beklenen = self.calisabilir_gun_sayisi()
        girilen = self.puantajlar.filter(kod__in=("G", "Y", "İ", "U", "X")).count()
        return beklenen > 0 and girilen >= beklenen

    def _tam_ay_calisan_mi(self) -> bool:
        if not self.gecerli_aralik_var():
            return False
        # Sirket personeli ancak secilen tam ay icin, ayin basindan sonuna kadar calisabilir durumdaysa
        # ve o ayin butun calisabilir gunleri puantajda islenmisse 30 gun bazina normalize edilir.
        ay_basi = self.orijinal_baslangic.replace(day=1)
        try:
            sonraki_ay = ay_basi.replace(month=ay_basi.month + 1)
        except ValueError:
            sonraki_ay = ay_basi.replace(year=ay_basi.year + 1, month=1)
        ay_sonu = sonraki_ay - timedelta(days=1)
        secim_tam_ay = self.orijinal_baslangic == ay_basi and self.orijinal_bitis == ay_sonu
        personel_ay_basi_calisiyor = self.personel.ise_giris_tarihi <= ay_basi
        personel_ay_sonu_calisiyor = (not self.personel.isten_cikis_tarihi) or self.personel.isten_cikis_tarihi >= ay_sonu
        # Tam ay ancak ay bittikten sonra 30 gun bazina normalize edilir.
        # Boylece ay ortasinda 01-31 raporu alinsa bile gelecekteki hak edilmeyen maas gorunmez.
        ay_hesabi_bitti = self.bitis == ay_sonu
        return secim_tam_ay and ay_hesabi_bitti and personel_ay_basi_calisiyor and personel_ay_sonu_calisiyor

    def sirket_maas_gunu(self) -> Decimal:
        if not self.gecerli_aralik_var():
            return Decimal("0")

        # Sirket personeli icin gunluk ucret her zaman aylik maas / 30 olarak hesaplanir.
        # Ancak personel ay icinde ise girdiyse/ciktiysa sadece calisabilir tarih araligi maasa dahil edilir.
        # Pazar veya resmi tatilde gelmemek sirket personelinden dusulmez; sadece X/U ve Y kadar kesinti uygulanir.
        if self._tam_ay_calisan_mi():
            sonuc = Decimal("30") - self.eksik_gun()
        else:
            sonuc = Decimal(str(self.calisabilir_gun_sayisi())) - self.eksik_gun()

        # 31 gunluk ayda girilen eksik gunler, gercekte calisilan gunu sifirlayamaz.
        sonuc = max(sonuc, self.ucretli_gun())

        if sonuc < 0:
            return Decimal("0")
        if sonuc > 30:
            return Decimal("30")
        return sonuc

    def hak_edilen_gun(self) -> Decimal:
        if self.personel.personel_turu == "sirket":
            return self.sirket_maas_gunu()
        return self.ucretli_gun()

    def gorunen_toplam_gun(self) -> Decimal:
        # Puantaj ekraninda ve raporda gorunen gun, sirket/taseron ayrimi yapmadan fiili isaretlenen gundur.
        return self.ucretli_gun()

    def gun_ozeti(self) -> dict:
        return {
            "ucretli_gun": self.ucretli_gun(),
            "islenen_gun": self.islenen_gun(),
            "eksik_gun": self.eksik_gun(),
            "devamsiz_gun": self.devamsiz_gun(),
            "ucretsiz_izin_gun": self.ucretsiz_izin_gun(),
            "yarim_gun": self.yarim_gun(),
            "hak_edilen_gun": self.hak_edilen_gun(),
            "gorunen_toplam_gun": self.gorunen_toplam_gun(),
        }
