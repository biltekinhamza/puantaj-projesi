from datetime import date
from decimal import Decimal
from .models import Katsayi, ResmiTatil

DEFAULT_KATSAYILAR = {
    "AYLIK_BAZ_GUN": ("Aylık Maaş Baz Günü", Decimal("30"), "Şirket personeli maaş bazı"),
    "YARIM_GUN_ORANI": ("Yarım Gün Oranı", Decimal("0.5"), "Y kodunun gün oranı"),
    "SAATLIK_MESAI_KATSAYI": ("Saatlik Mesai Katsayısı", Decimal("1.5"), "Normal saatlik mesai çarpanı"),
    "GUNLUK_CALISMA_SAATI": ("Günlük Çalışma Saati", Decimal("7.5"), "Saatlik ücret hesabı"),
    "PAZAR_MESAI_ORANI": ("Pazar Mesaisi Gün Oranı", Decimal("1"), "G kodunda ek gün oranı"),
    "RESMI_TATIL_MESAI_ORANI": ("Resmi Tatil Mesaisi Gün Oranı", Decimal("1"), "G kodunda ek gün oranı"),
}

SABIT_TATILLER = [
    (1, 1, "Yılbaşı"),
    (4, 23, "Ulusal Egemenlik ve Çocuk Bayramı"),
    (5, 1, "Emek ve Dayanışma Günü"),
    (5, 19, "Atatürk'ü Anma, Gençlik ve Spor Bayramı"),
    (7, 15, "Demokrasi ve Milli Birlik Günü"),
    (8, 30, "Zafer Bayramı"),
    (10, 29, "Cumhuriyet Bayramı"),
]

def seed_katsayilar():
    for kod, (ad, deger, aciklama) in DEFAULT_KATSAYILAR.items():
        Katsayi.objects.get_or_create(kod=kod, defaults={"ad": ad, "deger": deger, "aciklama": aciklama})

def seed_sabit_resmi_tatiller(yil: int | None = None):
    yil = yil or date.today().year
    for y in range(yil - 1, yil + 3):
        for ay, gun, ad in SABIT_TATILLER:
            ResmiTatil.objects.get_or_create(tarih=date(y, ay, gun), defaults={"ad": ad, "gun_tipi": ResmiTatil.TAM, "sabit": True})

def resmi_tatil_bul(tarih: date):
    return ResmiTatil.objects.filter(tarih=tarih).first()
