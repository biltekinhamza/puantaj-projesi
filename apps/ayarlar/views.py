from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import KatsayiForm, ResmiTatilForm, SirketBilgisiForm
from .models import Katsayi, ResmiTatil, SirketBilgisi
from .services import seed_katsayilar, seed_sabit_resmi_tatiller


@login_required
def sirket_bilgileri(request):
    sirket = SirketBilgisi.get_solo()
    form = SirketBilgisiForm(request.POST or None, instance=sirket)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("ayarlar_sirket_bilgileri")
    return render(request, "ayarlar/sirket_bilgileri.html", {"form": form})

@login_required
def resmi_tatil_liste(request):
    seed_sabit_resmi_tatiller()
    form = ResmiTatilForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("ayarlar_resmi_tatil_liste")
    return render(request, "ayarlar/resmi_tatil_liste.html", {"form": form, "tatiller": ResmiTatil.objects.all()})

@login_required
def resmi_tatil_duzenle(request, pk):
    tatil = get_object_or_404(ResmiTatil, pk=pk)
    form = ResmiTatilForm(request.POST or None, instance=tatil)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("ayarlar_resmi_tatil_liste")
    return render(request, "ayarlar/form.html", {"form": form, "title": "Resmi Tatil Düzenle"})

@require_POST
@login_required
def resmi_tatil_sil(request, pk):
    get_object_or_404(ResmiTatil, pk=pk).delete()
    return redirect("ayarlar_resmi_tatil_liste")

@login_required
def katsayi_liste(request):
    seed_katsayilar()
    return render(request, "ayarlar/katsayi_liste.html", {"katsayilar": Katsayi.objects.all()})

@login_required
def katsayi_duzenle(request, pk):
    katsayi = get_object_or_404(Katsayi, pk=pk)
    form = KatsayiForm(request.POST or None, instance=katsayi)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("ayarlar_katsayi_liste")
    return render(request, "ayarlar/form.html", {"form": form, "title": "Katsayı Düzenle"})
