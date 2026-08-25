from django.contrib import admin
from .models import Mesai, Prim

@admin.register(Mesai)
class MesaiAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tarih', 'tur', 'kaynak', 'saat', 'gun_orani', 'tutar')
    list_filter = ('tur', 'kaynak', 'tarih')

@admin.register(Prim)
class PrimAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tarih', 'tutar')
