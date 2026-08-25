from django.contrib import admin
from .models import Katsayi, ResmiTatil

@admin.register(Katsayi)
class KatsayiAdmin(admin.ModelAdmin):
    list_display = ('kod', 'ad', 'deger')
    search_fields = ('kod', 'ad')

@admin.register(ResmiTatil)
class ResmiTatilAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'ad', 'gun_tipi', 'sabit')
    list_filter = ('gun_tipi', 'sabit')
    search_fields = ('ad',)
