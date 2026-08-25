from django import forms
from apps.personel.selectors import tarihte_calisanlar
from .models import Mesai, Prim

class MesaiForm(forms.ModelForm):
    class Meta:
        model = Mesai
        fields = ["personel", "tarih", "saat", "aciklama"]
        widgets = {"tarih": forms.DateInput(attrs={"type": "date"}), "saat": forms.NumberInput(attrs={"step": "0.25", "min": "0"}), "aciklama": forms.TextInput(attrs={"placeholder": "Opsiyonel açıklama"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["personel"].queryset = tarihte_calisanlar()

class TopluMesaiForm(forms.Form):
    tarih = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    saat = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    personeller = forms.ModelMultipleChoiceField(queryset=tarihte_calisanlar(), widget=forms.CheckboxSelectMultiple)
    aciklama = forms.CharField(required=False, max_length=255)

class PrimForm(forms.ModelForm):
    class Meta:
        model = Prim
        fields = ["personel", "tarih", "tutar", "aciklama"]
        widgets = {"tarih": forms.DateInput(attrs={"type": "date"}), "tutar": forms.NumberInput(attrs={"step": "0.01", "min": "0"}), "aciklama": forms.TextInput(attrs={"placeholder": "Opsiyonel açıklama"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["personel"].queryset = tarihte_calisanlar()
