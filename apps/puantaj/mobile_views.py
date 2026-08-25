import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.personel.models import Personel
from apps.puantaj.models import Puantaj
from apps.puantaj.services.otomatik_mesai_service import puantaj_kaynakli_mesai_guncelle

MOBIL_GRUP = "Mobil Puantaj"
MOBIL_KODLAR = {"G", "U", "X"}


def _mobil_yetkisini_kontrol_et(user):
    if not (user.is_superuser or user.groups.filter(name=MOBIL_GRUP).exists()):
        raise PermissionDenied("Bu hesabın mobil puantaj yetkisi yok.")


def _bugun_calisanlar():
    bugun = date.today()
    return Personel.objects.filter(ise_giris_tarihi__lte=bugun).filter(
        Q(isten_cikis_tarihi__isnull=True) | Q(isten_cikis_tarihi__gte=bugun)
    ).order_by("ad_soyad")


def _ozet(personeller, bugun):
    toplam = personeller.count()
    kayitli = Puantaj.objects.filter(personel__in=personeller, tarih=bugun).count()
    return {"toplam": toplam, "kayitli": kayitli, "tamamlandi": toplam > 0 and kayitli >= toplam}


@login_required
def mobil_puantaj(request):
    _mobil_yetkisini_kontrol_et(request.user)
    bugun = date.today()
    personeller = _bugun_calisanlar()
    kod_map = dict(Puantaj.objects.filter(personel__in=personeller, tarih=bugun).values_list("personel_id", "kod"))
    rows = [{"personel": personel, "kod": kod_map.get(personel.id), "kayitli": personel.id in kod_map} for personel in personeller]
    return render(request, "puantaj/mobil_client.html", {
        "bugun": bugun,
        "rows": rows,
        "ozet": _ozet(personeller, bugun),
    })


@login_required
@require_POST
def mobil_durum_kaydet(request):
    _mobil_yetkisini_kontrol_et(request.user)
    try:
        payload = json.loads(request.body)
        personel_id = int(payload.get("personel_id"))
        kod = payload.get("kod")
    except (TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({"hata": "Geçersiz istek."}, status=400)
    if kod not in MOBIL_KODLAR:
        return JsonResponse({"hata": "Geçersiz puantaj durumu."}, status=400)

    bugun = date.today()
    personel = get_object_or_404(_bugun_calisanlar(), pk=personel_id)
    puantaj, _ = Puantaj.objects.update_or_create(personel=personel, tarih=bugun, defaults={"kod": kod})
    puantaj_kaynakli_mesai_guncelle(puantaj)
    return JsonResponse({"personel_id": personel.id, "kod": kod, "ozet": _ozet(_bugun_calisanlar(), bugun)})


@login_required
@require_POST
def mobil_gunu_tamamla(request):
    _mobil_yetkisini_kontrol_et(request.user)
    bugun = date.today()
    personeller = _bugun_calisanlar()
    eklenen = 0
    with transaction.atomic():
        kayitli_ids = set(Puantaj.objects.filter(personel__in=personeller, tarih=bugun).values_list("personel_id", flat=True))
        for personel in personeller:
            if personel.id in kayitli_ids:
                continue
            puantaj = Puantaj.objects.create(personel=personel, tarih=bugun, kod="X")
            puantaj_kaynakli_mesai_guncelle(puantaj)
            eklenen += 1
    return JsonResponse({"eklenen": eklenen, "ozet": _ozet(personeller, bugun)})
