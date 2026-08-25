from django import forms
from .models import Katsayi, ResmiTatil, SirketBilgisi


class SirketBilgisiForm(forms.ModelForm):
    class Meta:
        model = SirketBilgisi
        fields = [
            "kisa_ad", "ticari_unvan", "adres", "telefon", "eposta",
            "web_sitesi", "vergi_dairesi", "vergi_no", "mersis_no",
            "yetkili_ad_soyad", "yetkili_unvan",
        ]
        widgets = {"adres": forms.Textarea(attrs={"rows": 3})}

class ResmiTatilForm(forms.ModelForm):
    class Meta:
        model = ResmiTatil
        fields = ["ad", "tarih", "gun_tipi", "aciklama"]
        widgets = {"tarih": forms.DateInput(attrs={"type": "date"}), "aciklama": forms.Textarea(attrs={"rows": 2})}

class KatsayiForm(forms.ModelForm):
    class Meta:
        model = Katsayi
        fields = ["ad", "deger", "aciklama"]
        widgets = {"deger": forms.NumberInput(attrs={"step": "0.0001"}), "aciklama": forms.Textarea(attrs={"rows": 2})}
