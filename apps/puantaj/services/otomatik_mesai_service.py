from decimal import Decimal, ROUND_HALF_UP
from apps.ayarlar.models import Katsayi, ResmiTatil
from apps.ek_kazanc.models import Mesai

Q2 = Decimal("0.01")

def _q2(value: Decimal) -> Decimal:
    return Decimal(value).quantize(Q2, rounding=ROUND_HALF_UP)

def _gun_orani(kod: str, base: Decimal) -> Decimal:
    if kod == "G":
        return _q2(base)
    if kod == "Y":
        return _q2(base * Decimal("0.5"))
    return Decimal("0.00")

def puantaj_kaynakli_mesai_guncelle(puantaj):
    """Puantaj kaydı G/Y ise Pazar veya resmi tatil otomatik mesaisi oluşturur; değilse temizler."""
    tarih = puantaj.tarih
    personel = puantaj.personel
    olusan_turler = []

    if tarih.weekday() == 6:
        oran = _gun_orani(puantaj.kod, Katsayi.get_deger("PAZAR_MESAI_ORANI", "1"))
        if oran > 0:
            Mesai.objects.update_or_create(
                personel=personel, tarih=tarih, tur="PAZAR", kaynak="PUANTAJ_OTOMATIK",
                defaults={"saat": None, "gun_orani": oran, "aciklama": "Puantajdan otomatik Pazar mesaisi"},
            )
            olusan_turler.append("PAZAR")

    tatil = ResmiTatil.objects.filter(tarih=tarih).first()
    if tatil:
        base = Katsayi.get_deger("RESMI_TATIL_MESAI_ORANI", "1")
        if tatil.gun_tipi == ResmiTatil.YARIM:
            base = base * Decimal("0.5")
        oran = _gun_orani(puantaj.kod, base)
        if oran > 0:
            Mesai.objects.update_or_create(
                personel=personel, tarih=tarih, tur="RESMI_TATIL", kaynak="PUANTAJ_OTOMATIK",
                defaults={"saat": None, "gun_orani": oran, "aciklama": f"Puantajdan otomatik resmi tatil mesaisi: {tatil.ad}"},
            )
            olusan_turler.append("RESMI_TATIL")

    Mesai.objects.filter(personel=personel, tarih=tarih, kaynak="PUANTAJ_OTOMATIK").exclude(tur__in=olusan_turler).delete()

def puantaj_kaynakli_mesai_temizle(personel, tarih):
    Mesai.objects.filter(personel=personel, tarih=tarih, kaynak="PUANTAJ_OTOMATIK").delete()
