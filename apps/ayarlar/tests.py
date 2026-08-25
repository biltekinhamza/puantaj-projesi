from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import SirketBilgisi


class SirketBilgisiTestleri(TestCase):
    def test_tek_sirket_kaydi_kullanilir(self):
        ilk = SirketBilgisi.get_solo()
        ikinci = SirketBilgisi(kisa_ad="Yeni Şirket", ticari_unvan="Yeni Şirket A.Ş.")
        ikinci.save()
        self.assertEqual(ilk.pk, ikinci.pk)
        self.assertEqual(SirketBilgisi.objects.count(), 1)
        self.assertEqual(SirketBilgisi.get_solo().kisa_ad, "Yeni Şirket")

    def test_sirket_bilgileri_ekranindan_guncellenir(self):
        user = get_user_model().objects.create_user(username="yonetici", password="test-parola")
        self.client.force_login(user)
        response = self.client.post(reverse("ayarlar_sirket_bilgileri"), {
            "kisa_ad": "Örnek Makine",
            "ticari_unvan": "Örnek Makine Sanayi A.Ş.",
            "adres": "Isparta",
            "telefon": "", "eposta": "", "web_sitesi": "",
            "vergi_dairesi": "", "vergi_no": "", "mersis_no": "",
            "yetkili_ad_soyad": "", "yetkili_unvan": "",
        })
        self.assertRedirects(response, reverse("ayarlar_sirket_bilgileri"))
        self.assertEqual(SirketBilgisi.get_solo().kisa_ad, "Örnek Makine")
