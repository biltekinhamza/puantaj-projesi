from django import forms
from .models import Personel

class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        fields = [
            "ad_soyad", "personel_turu", "departman", "gorevi", "telefon",
            "tc_kimlik_no", "iban", "dogum_tarihi", "adres",
            "aylik_maas", "gunluk_yevmiyesi", "ise_giris_tarihi",
            "isten_cikis_tarihi", "isten_cikis_nedeni",
        ]
        widgets = {
            # HTML date input değerleri tarayıcıda görünebilmesi için mutlaka
            # YYYY-MM-DD formatında render edilmelidir. Aksi halde güncelleme
            # ekranında mevcut tarih boş görünür ve zorunlu alan yeniden istenir.
            "ise_giris_tarihi": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "isten_cikis_tarihi": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "dogum_tarihi": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "adres": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("ise_giris_tarihi", "isten_cikis_tarihi", "dogum_tarihi"):
            self.fields[field_name].input_formats = ["%Y-%m-%d"]
