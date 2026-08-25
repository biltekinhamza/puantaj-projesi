from django.contrib import admin
from .models import Puantaj, BankaOdeme

@admin.register(Puantaj)
class PuantajAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tarih', 'kod')
    list_filter = ('kod', 'tarih')

@admin.register(BankaOdeme)
class BankaOdemeAdmin(admin.ModelAdmin):
    list_display = ('personel', 'baslangic', 'bitis', 'banka_tutar')
