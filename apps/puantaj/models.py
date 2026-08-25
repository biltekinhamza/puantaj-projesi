from django.core.exceptions import ValidationError
from django.db import models
from apps.personel.models import Personel
from .adapter import PUANTAJ_KODLARI

class Puantaj(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="puantajlar")
    tarih = models.DateField(verbose_name="Tarih")
    kod = models.CharField(max_length=1, verbose_name="Puantaj Kodu")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Puantaj"
        verbose_name_plural = "Puantajlar"
        unique_together = ("personel", "tarih")
        indexes = [models.Index(fields=["personel", "tarih"]), models.Index(fields=["tarih", "kod"])]
        ordering = ["personel", "tarih"]

    def __str__(self):
        return f"{self.personel.ad_soyad} | {self.tarih} | {self.kod}"

    def clean(self):
        if self.kod not in PUANTAJ_KODLARI:
            raise ValidationError({"kod": "Geçersiz puantaj kodu."})
        if not self.personel.calisiyor_mu(self.tarih):
            raise ValidationError("Personel bu tarihte çalışabilir aralıkta değil.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class BankaOdeme(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="banka_odemeleri")
    baslangic = models.DateField(verbose_name="Başlangıç Tarihi")
    bitis = models.DateField(verbose_name="Bitiş Tarihi")
    banka_tutar = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Banka Tutarı")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Banka Ödeme"
        verbose_name_plural = "Banka Ödemeleri"
        ordering = ["-baslangic", "-id"]
        unique_together = ("personel", "baslangic", "bitis")
        indexes = [models.Index(fields=["personel", "baslangic", "bitis"])]

    def __str__(self):
        return f"Banka Ödeme | {self.personel.ad_soyad} | {self.baslangic} - {self.bitis} | {self.banka_tutar}"
