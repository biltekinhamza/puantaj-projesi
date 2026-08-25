from django.core.management.base import BaseCommand
from apps.ayarlar.services import seed_katsayilar, seed_sabit_resmi_tatiller

class Command(BaseCommand):
    help = "Varsayılan katsayıları ve sabit resmi tatilleri oluşturur."
    def handle(self, *args, **options):
        seed_katsayilar(); seed_sabit_resmi_tatiller()
        self.stdout.write(self.style.SUCCESS("Varsayılan ayarlar hazır."))
