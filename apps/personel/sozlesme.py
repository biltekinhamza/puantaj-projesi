from datetime import datetime

from apps.ayarlar.models import SirketBilgisi


def sgk_isyeri_sicil_no_from_departman(departman):
    if departman == "SDÜ YEMEKHANE":
        return "4.4100.01.01.1067692.032.01.20.001"
    if departman == "TAVSAN MERKEZ":
        return "2.2825.01.01.1066289.032.01.72.000"
    return ""


def _fmt_tr_date(s: str) -> str:
    """
    2026-01-08 -> 08.01.2026
    """
    if not s:
        return ""
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return s


def build_sozlesme_context(
    personel,
    baslangic="",
    bitis="",
    imza="",
    isin_adi="",
):
    sirket = SirketBilgisi.get_solo()
    return {
        "isveren": {
            "unvan": sirket.ticari_unvan,
            "adres": sirket.adres,
            "sgk_sicil_no": sgk_isyeri_sicil_no_from_departman(
                personel.departman
            ),
        },
        "personel": {
            "ad_soyad": personel.ad_soyad or "",
            "tc_kimlik_no": personel.tc_kimlik_no or "",
            "dogum_tarihi": (
                personel.dogum_tarihi.strftime("%d.%m.%Y")
                if personel.dogum_tarihi
                else ""
            ),
            "adres": personel.adres or "",
            "telefon": personel.telefon or "",
            "gorevi": personel.gorevi or "",
        },
        "sozlesme": {
            # ✅ TARİHLER TÜRKÇE FORMAT
            "baslangic": _fmt_tr_date(baslangic),
            "bitis": _fmt_tr_date(bitis),
            "imza": _fmt_tr_date(imza),

            # ✅ İŞİN ADI CÜMLEYE DÖNÜŞTÜRÜLDÜ
            "isin_adi": (
                f"{isin_adi}"
                if isin_adi
                else ""
            ),
        },
    }
