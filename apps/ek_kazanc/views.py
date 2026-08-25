from datetime import date
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.personel.selectors import tarihte_calisanlar
from .forms import MesaiForm, PrimForm, TopluMesaiForm
from .models import Mesai, Prim

@login_required
def mesai_liste(request):
    personeller = tarihte_calisanlar()
    qs = Mesai.objects.select_related("personel").order_by("-tarih", "-id")
    personel_id = request.GET.get("personel"); ay = request.GET.get("ay"); yil = request.GET.get("yil"); tur = request.GET.get("tur")
    if personel_id: qs = qs.filter(personel_id=personel_id)
    if tur: qs = qs.filter(tur=tur)
    if ay:
        try: qs = qs.filter(tarih__month=int(ay))
        except ValueError: pass
    if yil:
        try: qs = qs.filter(tarih__year=int(yil))
        except ValueError: pass
    return render(request, "ek_kazanc/mesai_liste.html", {
        "personeller": personeller, "kayitlar": qs,
        "sec_personel": int(personel_id) if personel_id else None, "sec_ay": int(ay) if ay else None, "sec_yil": int(yil) if yil else None, "sec_tur": tur,
        "toplam_saat": sum(float(x.saat or 0) for x in qs), "toplam_tutar": sum(float(x.tutar or 0) for x in qs),
    })

@login_required
def mesai_yeni(request):
    form = MesaiForm(request.POST or None, initial={"tarih": date.today()})
    if request.method == "POST" and form.is_valid():
        mesai = form.save(commit=False); mesai.tur = "NORMAL"; mesai.kaynak = "MANUEL"; mesai.gun_orani = None; mesai.save()
        return redirect("ek_kazanc_mesai_liste")
    return render(request, "ek_kazanc/mesai_form.html", {"form": form, "title": "Saatlik Mesai Girişi"})

@login_required
def mesai_toplu(request):
    form = TopluMesaiForm(request.POST or None, initial={"tarih": date.today()})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            for personel in form.cleaned_data["personeller"]:
                Mesai.objects.update_or_create(
                    personel=personel, tarih=form.cleaned_data["tarih"], tur="NORMAL", kaynak="MANUEL",
                    defaults={"saat": form.cleaned_data["saat"], "aciklama": form.cleaned_data.get("aciklama") or "Toplu saatlik mesai", "gun_orani": None},
                )
        return redirect("ek_kazanc_mesai_liste")
    return render(request, "ek_kazanc/mesai_toplu.html", {"form": form, "title": "Toplu Saatlik Mesai Girişi"})

@require_POST
@login_required
def mesai_sil(request, pk):
    get_object_or_404(Mesai, pk=pk).delete()
    return redirect(request.META.get("HTTP_REFERER", "ek_kazanc_mesai_liste"))

@login_required
def prim_liste(request):
    personeller = tarihte_calisanlar(); qs = Prim.objects.select_related("personel").order_by("-tarih", "-id")
    personel_id = request.GET.get("personel"); ay = request.GET.get("ay"); yil = request.GET.get("yil")
    if personel_id: qs = qs.filter(personel_id=personel_id)
    if ay:
        try: qs = qs.filter(tarih__month=int(ay))
        except ValueError: pass
    if yil:
        try: qs = qs.filter(tarih__year=int(yil))
        except ValueError: pass
    return render(request, "ek_kazanc/prim_liste.html", {"personeller": personeller, "kayitlar": qs, "sec_personel": int(personel_id) if personel_id else None, "sec_ay": int(ay) if ay else None, "sec_yil": int(yil) if yil else None, "toplam_tutar": sum(float(x.tutar or 0) for x in qs)})

@login_required
def prim_yeni(request):
    form = PrimForm(request.POST or None, initial={"tarih": date.today()})
    if request.method == "POST" and form.is_valid():
        form.save(); return redirect("ek_kazanc_prim_liste")
    return render(request, "ek_kazanc/prim_form.html", {"form": form, "title": "Prim Girişi"})

@require_POST
@login_required
def prim_sil(request, pk):
    get_object_or_404(Prim, pk=pk).delete()
    return redirect(request.META.get("HTTP_REFERER", "ek_kazanc_prim_liste"))
