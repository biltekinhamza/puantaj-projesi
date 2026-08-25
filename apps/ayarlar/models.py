from decimal import Decimal
from django.db import models


class SirketBilgisi(models.Model):
    kisa_ad = models.CharField("Kısa ad", max_length=100, default="Tavsan Makine")
    ticari_unvan = models.CharField(
        "Ticari unvan",
        max_length=250,
        default="Tavsan Makine İml. San. Tic. Ltd. Şti.",
    )
    adres = models.TextField(default="Vatan OSB Mah. 307. Cad. No:2 ISPARTA")
    telefon = models.CharField(max_length=30, blank=True)
    eposta = models.EmailField("E-posta", blank=True)
    web_sitesi = models.URLField("Web sitesi", blank=True)
    vergi_dairesi = models.CharField("Vergi dairesi", max_length=100, blank=True)
    vergi_no = models.CharField("Vergi numarası", max_length=20, blank=True)
    mersis_no = models.CharField("MERSİS numarası", max_length=20, blank=True)
    yetkili_ad_soyad = models.CharField("Yetkili ad soyad", max_length=150, blank=True)
    yetkili_unvan = models.CharField("Yetkili unvanı", max_length=150, blank=True)

    class Meta:
        verbose_name = "Şirket Bilgisi"
        verbose_name_plural = "Şirket Bilgileri"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None

    def __str__(self):
        return self.ticari_unvan

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class Katsayi(models.Model):
    kod = models.CharField(max_length=50, unique=True)
    ad = models.CharField(max_length=150)
    deger = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0"))
    aciklama = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Katsayı"
        verbose_name_plural = "Katsayılar"
        ordering = ["kod"]

    def __str__(self):
        return f"{self.ad}: {self.deger}"

    @classmethod
    def get_deger(cls, kod: str, default: str | Decimal = "0") -> Decimal:
        obj = cls.objects.filter(kod=kod).first()
        return obj.deger if obj else Decimal(str(default))

class ResmiTatil(models.Model):
    TAM = "TAM"
    YARIM = "YARIM"
    GUN_TIPI = ((TAM, "Tam Gün"), (YARIM, "Yarım Gün"))

    ad = models.CharField(max_length=150)
    tarih = models.DateField(unique=True)
    gun_tipi = models.CharField(max_length=10, choices=GUN_TIPI, default=TAM)
    sabit = models.BooleanField(default=False, help_text="Sabit tarihli standart resmi tatil")
    aciklama = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Resmi Tatil"
        verbose_name_plural = "Resmi Tatiller"
        ordering = ["tarih"]

    def __str__(self):
        return f"{self.tarih} - {self.ad}"
