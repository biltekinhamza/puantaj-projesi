from django.db import models
from apps.personel.models import Personel

class Avans(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="avanslar")
    tarih = models.DateField(verbose_name="Tarih")
    tutar = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    aciklama = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avans"
        verbose_name_plural = "Avanslar"
        ordering = ["-tarih", "-id"]
        indexes = [models.Index(fields=["personel", "tarih"])]

    def __str__(self):
        return f"Avans | {self.personel.ad_soyad} | {self.tarih} | {self.tutar}"

class Icra(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="icralar")
    tarih = models.DateField(verbose_name="Tarih")
    tutar = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    aciklama = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "İcra"
        verbose_name_plural = "İcralar"
        ordering = ["-tarih", "-id"]
        indexes = [models.Index(fields=["personel", "tarih"])]

    def __str__(self):
        return f"İcra | {self.personel.ad_soyad} | {self.tarih} | {self.tutar}"
