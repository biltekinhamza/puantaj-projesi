from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import models
from apps.ayarlar.models import Katsayi
from apps.personel.models import Personel

MESAI_TURU = (
    ("NORMAL", "Saatlik Mesai"),
    ("PAZAR", "Pazar Mesaisi"),
    ("RESMI_TATIL", "Resmi Tatil Çalışması"),
)
MESAI_KAYNAK = (("MANUEL", "Manuel"), ("PUANTAJ_OTOMATIK", "Puantaj Otomatik"))

def _q2(x: Decimal) -> Decimal:
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Mesai(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="mesailer")
    tarih = models.DateField(verbose_name="Tarih")
    tur = models.CharField(max_length=20, choices=MESAI_TURU, default="NORMAL", verbose_name="Mesai Türü")
    kaynak = models.CharField(max_length=20, choices=MESAI_KAYNAK, default="MANUEL", verbose_name="Kaynak")
    saat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Saat")
    gun_orani = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Gün Oranı")
    tutar = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), verbose_name="Tutar")
    aciklama = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mesai"
        verbose_name_plural = "Mesailer"
        ordering = ["-tarih", "-id"]
        indexes = [models.Index(fields=["personel", "tarih"]), models.Index(fields=["tur", "tarih"]), models.Index(fields=["kaynak", "tarih"])]
        constraints = [models.UniqueConstraint(fields=["personel", "tarih", "tur", "kaynak"], name="unique_mesai_personel_tarih_tur_kaynak")]

    def __str__(self):
        return f"Mesai | {self.personel.ad_soyad} | {self.tarih} | {self.tur} | {self.tutar}"

    def _gunluk_ucret(self) -> Decimal:
        if self.personel.personel_turu == "taseron":
            return Decimal(str(self.personel.gunluk_yevmiyesi or 0))
        return Decimal(str(self.personel.aylik_maas or 0)) / Decimal("30") if self.personel.aylik_maas else Decimal("0")

    def recalc_tutar(self):
        gunluk = self._gunluk_ucret()
        if self.tur in ("PAZAR", "RESMI_TATIL"):
            oran = Decimal(str(self.gun_orani if self.gun_orani is not None else 1))
            self.tutar = _q2(gunluk * oran)
            return
        saat = Decimal(str(self.saat or 0))
        gunluk_calisma_saati = Katsayi.get_deger("GUNLUK_CALISMA_SAATI", "7.5")
        katsayi = Katsayi.get_deger("SAATLIK_MESAI_KATSAYI", "1.5")
        saatlik = gunluk / gunluk_calisma_saati if gunluk_calisma_saati else Decimal("0")
        self.tutar = _q2(saat * saatlik * katsayi)

    def clean(self):
        if self.kaynak == "MANUEL" and self.tur != "NORMAL":
            raise ValidationError("Manuel mesai sadece saatlik mesai olabilir. Pazar/resmi tatil puantajdan otomatik gelir.")
        if self.tur == "NORMAL" and not self.saat:
            raise ValidationError({"saat": "Saatlik mesai için saat zorunludur."})

    def save(self, *args, **kwargs):
        # Katsayı tablosundaki değerler 4 ondalık saklanır; Mesai.gun_orani ise
        # 2 ondalık alır. full_clean() alan doğrulamasından önce normalize etmezsek
        # Decimal("1.0000") / Decimal("0.50000") gibi değerler ValidationError üretir.
        if self.saat is not None:
            self.saat = _q2(self.saat)
        if self.gun_orani is not None:
            self.gun_orani = _q2(self.gun_orani)
        self.full_clean()
        self.recalc_tutar()
        super().save(*args, **kwargs)

class Prim(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="primler")
    tarih = models.DateField(verbose_name="Tarih")
    tutar = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    aciklama = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Prim"
        verbose_name_plural = "Primler"
        ordering = ["-tarih", "-id"]
        indexes = [models.Index(fields=["personel", "tarih"]), models.Index(fields=["aktif", "tarih"])]

    def __str__(self):
        return f"Prim | {self.personel.ad_soyad} | {self.tarih} | {self.tutar}"
