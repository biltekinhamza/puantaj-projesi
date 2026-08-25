from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Personel


@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = (
        'ad_soyad',
        'personel_turu',
        'ise_giris_tarihi',
        'isten_cikis_tarihi',
        'aktif',
    )
    list_filter = ('personel_turu', 'aktif')
    search_fields = ('ad_soyad',)
