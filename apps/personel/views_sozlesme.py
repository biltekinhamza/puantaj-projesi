from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import Personel
from .sozlesme import build_sozlesme_context
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

@login_required
def personel_sozlesme_sec(request):
    if request.method == "POST":
        personel_id = request.POST.get("personel_id")
        baslangic = request.POST.get("baslangic")
        bitis = request.POST.get("bitis")
        imza = request.POST.get("imza")
        isin_adi = request.POST.get("isin_adi")

        return redirect(
            f"/personel/{personel_id}/sozlesme/"
            f"?baslangic={baslangic}"
            f"&bitis={bitis}"
            f"&imza={imza}"
            f"&isin_adi={isin_adi}"
        )

    from apps.personel.selectors import tarihte_calisanlar
    personeller = tarihte_calisanlar()
    return render(request, "personel/sozlesme_sec.html", {"personeller": personeller})

@login_required
def personel_belirli_sureli_sozlesme(request, pk):
    personel = get_object_or_404(Personel, pk=pk)

    baslangic = request.GET.get("baslangic", "")
    bitis = request.GET.get("bitis", "")
    imza = request.GET.get("imza", "")
    isin_adi = request.GET.get("isin_adi", "")

    context = build_sozlesme_context(
        personel=personel,
        baslangic=baslangic,
        bitis=bitis,
        imza=imza,
        isin_adi=isin_adi,
        
    )
    context["personel_id"] = personel.id

    return render(
        request,
        "personel/belirli_sureli_is_sozlesmesi_ekran.html",
        context,
    )

@login_required
def personel_belirli_sureli_sozlesme_pdf(request, pk):
    personel = Personel.objects.get(pk=pk)

    baslangic = request.GET.get("baslangic", "")
    bitis = request.GET.get("bitis", "")
    imza = request.GET.get("imza", "")
    isin_adi = request.GET.get("isin_adi", "")

    context = build_sozlesme_context(
        personel=personel,
        baslangic=baslangic,
        bitis=bitis,
        imza=imza,
        isin_adi=isin_adi,
    )

    html_string = render_to_string(
        "personel/belirli_sureli_is_sozlesmesi.html",
        context,
    )

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="sozlesme_{personel.ad_soyad}.pdf"'
    )
    return response
