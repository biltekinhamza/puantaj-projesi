from django.db import migrations, models


def varsayilan_sirketi_olustur(apps, schema_editor):
    apps.get_model("ayarlar", "SirketBilgisi").objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [("ayarlar", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="SirketBilgisi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kisa_ad", models.CharField(default="Tavsan Makine", max_length=100, verbose_name="Kısa ad")),
                ("ticari_unvan", models.CharField(default="Tavsan Makine İml. San. Tic. Ltd. Şti.", max_length=250, verbose_name="Ticari unvan")),
                ("adres", models.TextField(default="Vatan OSB Mah. 307. Cad. No:2 ISPARTA")),
                ("telefon", models.CharField(blank=True, max_length=30)),
                ("eposta", models.EmailField(blank=True, max_length=254, verbose_name="E-posta")),
                ("web_sitesi", models.URLField(blank=True, verbose_name="Web sitesi")),
                ("vergi_dairesi", models.CharField(blank=True, max_length=100, verbose_name="Vergi dairesi")),
                ("vergi_no", models.CharField(blank=True, max_length=20, verbose_name="Vergi numarası")),
                ("mersis_no", models.CharField(blank=True, max_length=20, verbose_name="MERSİS numarası")),
                ("yetkili_ad_soyad", models.CharField(blank=True, max_length=150, verbose_name="Yetkili ad soyad")),
                ("yetkili_unvan", models.CharField(blank=True, max_length=150, verbose_name="Yetkili unvanı")),
            ],
            options={"verbose_name": "Şirket Bilgisi", "verbose_name_plural": "Şirket Bilgileri"},
        ),
        migrations.RunPython(varsayilan_sirketi_olustur, migrations.RunPython.noop),
    ]
