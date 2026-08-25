from .models import SirketBilgisi


def sirket_bilgisi(request):
    return {"sirket": SirketBilgisi.get_solo()}
