from datetime import date
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

class Personel(models.Model):
    PERSONEL_TURU_CHOICES = (
        ("sirket", "Şirket Personeli"),
        ("taseron", "Taşeron Personel"),
    )

    ad_soyad = models.CharField(max_length=150, verbose_name="Ad Soyad")
    personel_turu = models.CharField(max_length=10, choices=PERSONEL_TURU_CHOICES, verbose_name="Personel Türü")
    aylik_maas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Aylık Maaş")
    gunluk_yevmiyesi = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Günlük Yevmiye")
    telefon = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    tc_kimlik_no = models.CharField(max_length=11, null=True, blank=True, verbose_name="TC Kimlik No")
    iban = models.CharField(max_length=34, null=True, blank=True, verbose_name="IBAN")
    gorevi = models.CharField(max_length=100, null=True, blank=True, verbose_name="Görevi")
    departman = models.CharField(max_length=100, null=True, blank=True, verbose_name="Departman")
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    adres = models.TextField(null=True, blank=True, verbose_name="Adres")
    ise_giris_tarihi = models.DateField(verbose_name="İşe Giriş Tarihi")
    isten_cikis_tarihi = models.DateField(null=True, blank=True, verbose_name="İşten Çıkış Tarihi")
    isten_cikis_nedeni = models.CharField(max_length=150, null=True, blank=True, verbose_name="İşten Çıkış Nedeni")

    # Ana karar verici değildir. Sadece arşiv/gizleme gibi ikincil kullanım için bırakıldı.
    aktif = models.BooleanField(default=True, verbose_name="Arşivde Göster")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ad_soyad"]
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        constraints = [
            models.UniqueConstraint(
                fields=["tc_kimlik_no"],
                condition=~Q(tc_kimlik_no__isnull=True) & ~Q(tc_kimlik_no=""),
                name="unique_dolu_tc_kimlik_no",
            )
        ]

    def __str__(self):
        return self.ad_soyad

    def calisiyor_mu(self, tarih: date | None = None) -> bool:
        tarih = tarih or date.today()
        if self.ise_giris_tarihi and self.ise_giris_tarihi > tarih:
            return False
        if self.isten_cikis_tarihi and self.isten_cikis_tarihi < tarih:
            return False
        return True

    # Eski kodlar bozulmasın diye alias.
    def aktif_mi(self, tarih: date | None = None) -> bool:
        return self.calisiyor_mu(tarih)

    @property
    def durum(self) -> str:
        bugun = date.today()
        if self.isten_cikis_tarihi and self.isten_cikis_tarihi < bugun:
            return "İşten Çıktı"
        if self.isten_cikis_tarihi and self.isten_cikis_tarihi >= bugun:
            return "Çıkışı Planlandı"
        return "Çalışıyor"

    @property
    def gunluk_ucret(self):
        if self.personel_turu == "taseron":
            return self.gunluk_yevmiyesi or 0
        if self.aylik_maas:
            return self.aylik_maas / 30
        return 0

    def clean(self):
        if self.personel_turu == "sirket":
            if not self.aylik_maas:
                raise ValidationError({"aylik_maas": "Şirket personeli için aylık maaş zorunludur."})
            self.gunluk_yevmiyesi = None
        elif self.personel_turu == "taseron":
            if not self.gunluk_yevmiyesi:
                raise ValidationError({"gunluk_yevmiyesi": "Taşeron personel için günlük yevmiye zorunludur."})
            self.aylik_maas = None

        if self.isten_cikis_tarihi:
            if self.ise_giris_tarihi and self.isten_cikis_tarihi < self.ise_giris_tarihi:
                raise ValidationError({"isten_cikis_tarihi": "İşten çıkış tarihi, işe giriş tarihinden önce olamaz."})
            if not self.isten_cikis_nedeni:
                raise ValidationError({"isten_cikis_nedeni": "İşten çıkış tarihi varsa çıkış nedeni zorunludur."})

        if self.tc_kimlik_no:
            self.tc_kimlik_no = self.tc_kimlik_no.strip()
            if not re.fullmatch(r"\d{11}", self.tc_kimlik_no):
                raise ValidationError({"tc_kimlik_no": "TC Kimlik No 11 haneli ve sadece rakamlardan oluşmalıdır."})
            qs = Personel.objects.filter(tc_kimlik_no=self.tc_kimlik_no)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({"tc_kimlik_no": "Bu TC Kimlik No başka bir personelde kayıtlı."})
        else:
            self.tc_kimlik_no = None

        if self.iban:
            iban = self.iban.replace(" ", "").upper()
            self.iban = iban
            if not re.fullmatch(r"TR\d{24}", iban):
                raise ValidationError({"iban": 'IBAN "TR" ile başlamalı ve toplam 26 karakter olmalıdır.'})

        if self.telefon and not re.fullmatch(r"[0-9+\-\s()]{7,20}", self.telefon):
            raise ValidationError({"telefon": "Telefon formatı geçersiz."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
