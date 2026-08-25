from django import forms
from apps.personel.selectors import tarihte_calisanlar
from .models import Avans, Icra

class AvansForm(forms.ModelForm):
    class Meta:
        model = Avans
        fields = ["personel", "tarih", "tutar", "aciklama"]
        widgets = {"tarih": forms.DateInput(attrs={"type": "date"}), "tutar": forms.NumberInput(attrs={"step": "0.01", "min": "0"}), "aciklama": forms.TextInput(attrs={"placeholder": "Avans açıklaması"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["personel"].queryset = tarihte_calisanlar()

class IcraForm(forms.ModelForm):
    class Meta:
        model = Icra
        fields = ["personel", "tarih", "tutar", "aciklama"]
        widgets = {"tarih": forms.DateInput(attrs={"type": "date"}), "tutar": forms.NumberInput(attrs={"step": "0.01", "min": "0"}), "aciklama": forms.TextInput(attrs={"placeholder": "İcra açıklaması"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["personel"].queryset = tarihte_calisanlar()
