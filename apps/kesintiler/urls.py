from django.urls import path
from . import views
urlpatterns = [
    path("avans/", views.avans_liste, name="kesintiler_avans_liste"),
    path("avans/yeni/", views.avans_yeni, name="kesintiler_avans_yeni"),
    path("avans/<int:pk>/sil/", views.avans_sil, name="kesintiler_avans_sil"),
    path("icra/", views.icra_liste, name="kesintiler_icra_liste"),
    path("icra/yeni/", views.icra_yeni, name="kesintiler_icra_yeni"),
    path("icra/<int:pk>/sil/", views.icra_sil, name="kesintiler_icra_sil"),
]
