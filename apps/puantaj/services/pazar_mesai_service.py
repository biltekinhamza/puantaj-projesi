from apps.ek_kazanc.models import Mesai


def pazar_geldi_ise_mesai_ekle(puantaj):
    """
    KURAL:
    - Gün Pazar ise
    - Puantaj kodu 'G' ise
    → otomatik PAZAR mesaisi eklenir
    """

    if puantaj.tarih.weekday() != 6:
        return

    if puantaj.kod != "G":
        return

    Mesai.objects.get_or_create(
        personel=puantaj.personel,
        tarih=puantaj.tarih,
        tur="PAZAR",
        defaults={
            "saat": None,
        }
    )


def pazar_mesai_temizle(puantaj):
    """
    Pazar günü kod 'G' değilse
    otomatik eklenen PAZAR mesaisini sil
    """
    if puantaj.tarih.weekday() == 6 and puantaj.kod != "G":
        Mesai.objects.filter(
            personel=puantaj.personel,
            tarih=puantaj.tarih,
            tur="PAZAR"
        ).delete()
