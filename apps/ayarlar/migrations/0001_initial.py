from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Katsayi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kod", models.CharField(max_length=50, unique=True)),
                ("ad", models.CharField(max_length=150)),
                ("deger", models.DecimalField(decimal_places=4, default=Decimal("0"), max_digits=10)),
                ("aciklama", models.TextField(blank=True, null=True)),
            ],
            options={"verbose_name": "Katsayı", "verbose_name_plural": "Katsayılar", "ordering": ["kod"]},
        ),
        migrations.CreateModel(
            name="ResmiTatil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ad", models.CharField(max_length=150)),
                ("tarih", models.DateField(unique=True)),
                ("gun_tipi", models.CharField(choices=[("TAM", "Tam Gün"), ("YARIM", "Yarım Gün")], default="TAM", max_length=10)),
                ("sabit", models.BooleanField(default=False, help_text="Sabit tarihli standart resmi tatil")),
                ("aciklama", models.TextField(blank=True, null=True)),
            ],
            options={"verbose_name": "Resmi Tatil", "verbose_name_plural": "Resmi Tatiller", "ordering": ["tarih"]},
        ),
    ]
