from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from apps.personel.models import Personel
from apps.puantaj.models import Puantaj

DURUM_META = {
    "G": ("Geldi", "geldi"),
    "İ": ("Ücretli İzin", "izinli"),
    "X": ("Gelmedi", "gelmedi"),
    "U": ("Ücretsiz İzin", "izinli"),
    "Y": ("Yarım Gün", "diger"),
}


def _aktif_personeller(bugun):
    return Personel.objects.filter(ise_giris_tarihi__lte=bugun).filter(
        Q(isten_cikis_tarihi__isnull=True) | Q(isten_cikis_tarihi__gte=bugun)
    ).order_by("ad_soyad")


def _server_dashboard_data():
    bugun = date.today()
    personeller = list(_aktif_personeller(bugun))
    kayit_map = {
        puantaj.personel_id: puantaj
        for puantaj in Puantaj.objects.filter(personel__in=personeller, tarih=bugun).select_related("personel")
    }
    sayilar = {"geldi": 0, "izinli": 0, "gelmedi": 0, "diger": 0, "isaretlenmedi": 0}
    rows = []
    for personel in personeller:
        kayit = kayit_map.get(personel.id)
        if kayit:
            durum, durum_class = DURUM_META.get(kayit.kod, (kayit.kod, "diger"))
            sayilar[durum_class] += 1
        else:
            durum, durum_class = "İşaretlenmedi", "isaretlenmedi"
            sayilar[durum_class] += 1
        rows.append({
            "id": personel.id,
            "ad_soyad": personel.ad_soyad,
            "gorevi": personel.gorevi or "Görev belirtilmemiş",
            "durum": durum,
            "durum_class": durum_class,
            "saat": kayit.updated_at.strftime("%H:%M") if kayit else "-",
        })
    toplam = len(personeller)
    kayitli = toplam - sayilar["isaretlenmedi"]
    return {
        "bugun": bugun,
        "rows": rows,
        "sayilar": sayilar,
        "toplam": toplam,
        "kayitli": kayitli,
        "ilerleme": round(kayitli / toplam * 100) if toplam else 0,
        "tamamlandi": toplam > 0 and kayitli == toplam,
    }


@login_required
def server_dashboard(request):
    return render(request, "anasayfa.html", _server_dashboard_data())


@login_required
def server_dashboard_api(request):
    data = _server_dashboard_data()
    return JsonResponse({
        "rows": data["rows"],
        "sayilar": data["sayilar"],
        "toplam": data["toplam"],
        "kayitli": data["kayitli"],
        "ilerleme": data["ilerleme"],
        "tamamlandi": data["tamamlandi"],
    })
