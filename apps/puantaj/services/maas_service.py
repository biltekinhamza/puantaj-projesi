from decimal import Decimal, ROUND_HALF_UP
from apps.puantaj.services.puantaj_service import PuantajService

Q2 = Decimal("0.01")
def q2(x):
    return Decimal(x).quantize(Q2, rounding=ROUND_HALF_UP)

class MaasService:
    def __init__(self, personel, baslangic, bitis):
        self.personel = personel
        self.baslangic = baslangic
        self.bitis = bitis
        self.puantaj_service = PuantajService(personel, baslangic, bitis)

    def hak_edilen_gun(self):
        return self.puantaj_service.hak_edilen_gun()

    def brut_hakedis(self):
        if self.personel.personel_turu == "sirket":
            aylik = Decimal(str(self.personel.aylik_maas or 0))
            gunluk = aylik / Decimal("30")
            return q2(gunluk * self.puantaj_service.sirket_maas_gunu())
        gunluk = Decimal(str(self.personel.gunluk_yevmiyesi or 0))
        return q2(gunluk * self.puantaj_service.ucretli_gun())
