import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.personel.models import Personel

class Command(BaseCommand):
    help = "data/personeller.json içindeki eski personel kartlarını yeni temiz sisteme aktarır."

    def add_arguments(self, parser):
        parser.add_argument("--path", default="data/personeller.json")

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            self.stdout.write(self.style.WARNING(f"Personel aktarım dosyası yok: {path}"))
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        if Personel.objects.exists():
            self.stdout.write("Personel tablosu boş değil; otomatik aktarım atlandı.")
            return
        created = 0
        for row in data:
            fields = {k: row.get(k) for k in [
                "ad_soyad", "personel_turu", "aylik_maas", "gunluk_yevmiyesi", "telefon",
                "tc_kimlik_no", "iban", "gorevi", "departman", "dogum_tarihi", "adres",
                "ise_giris_tarihi", "isten_cikis_tarihi", "isten_cikis_nedeni", "aktif"
            ]}
            if fields.get("tc_kimlik_no") and Personel.objects.filter(tc_kimlik_no=fields["tc_kimlik_no"]).exists():
                fields["tc_kimlik_no"] = None
            Personel.objects.create(**fields)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} personel aktarıldı."))
