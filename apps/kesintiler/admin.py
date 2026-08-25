from django.contrib import admin
from .models import Avans, Icra

@admin.register(Avans)
class AvansAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tarih', 'tutar')

@admin.register(Icra)
class IcraAdmin(admin.ModelAdmin):
    list_display = ('personel', 'tarih', 'tutar')
