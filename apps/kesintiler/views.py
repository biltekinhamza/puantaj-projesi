from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.personel.selectors import tarihte_calisanlar
from .forms import AvansForm, IcraForm
from .models import Avans, Icra

def _filtrele(qs, request):
    personel_id = request.GET.get("personel"); ay = request.GET.get("ay"); yil = request.GET.get("yil")
    if personel_id: qs = qs.filter(personel_id=personel_id)
    if ay:
        try: qs = qs.filter(tarih__month=int(ay))
        except ValueError: pass
    if yil:
        try: qs = qs.filter(tarih__year=int(yil))
        except ValueError: pass
    return qs, personel_id, ay, yil

@login_required
def avans_liste(request):
    qs, personel_id, ay, yil = _filtrele(Avans.objects.select_related("personel").order_by("-tarih", "-id"), request)
    return render(request, "kesintiler/avans_liste.html", {"personeller": tarihte_calisanlar(), "kayitlar": qs, "sec_personel": int(personel_id) if personel_id else None, "sec_ay": int(ay) if ay else None, "sec_yil": int(yil) if yil else None, "toplam": sum(float(x.tutar) for x in qs)})

@login_required
def avans_yeni(request):
    form = AvansForm(request.POST or None, initial={"tarih": date.today()})
    if request.method == "POST" and form.is_valid():
        form.save(); return redirect("kesintiler_avans_liste")
    return render(request, "kesintiler/avans_form.html", {"form": form, "title": "Avans Girişi"})

@require_POST
@login_required
def avans_sil(request, pk):
    get_object_or_404(Avans, pk=pk).delete()
    return redirect(request.META.get("HTTP_REFERER", "kesintiler_avans_liste"))

@login_required
def icra_liste(request):
    qs, personel_id, ay, yil = _filtrele(Icra.objects.select_related("personel").order_by("-tarih", "-id"), request)
    return render(request, "kesintiler/icra_liste.html", {"personeller": tarihte_calisanlar(), "kayitlar": qs, "sec_personel": int(personel_id) if personel_id else None, "sec_ay": int(ay) if ay else None, "sec_yil": int(yil) if yil else None, "toplam": sum(float(x.tutar) for x in qs)})

@login_required
def icra_yeni(request):
    form = IcraForm(request.POST or None, initial={"tarih": date.today()})
    if request.method == "POST" and form.is_valid():
        form.save(); return redirect("kesintiler_icra_liste")
    return render(request, "kesintiler/icra_form.html", {"form": form, "title": "İcra Girişi"})

@require_POST
@login_required
def icra_sil(request, pk):
    get_object_or_404(Icra, pk=pk).delete()
    return redirect(request.META.get("HTTP_REFERER", "kesintiler_icra_liste"))
