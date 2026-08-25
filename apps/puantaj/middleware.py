from django.shortcuts import redirect

from apps.puantaj.mobile_views import MOBIL_GRUP


class MobilKullaniciSiniriMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not user.is_superuser and user.groups.filter(name=MOBIL_GRUP).exists():
            izinli_yollar = ("/mobil/", "/logout/", "/static/", "/media/")
            if not request.path.startswith(izinli_yollar):
                return redirect("/mobil/")
        return self.get_response(request)
