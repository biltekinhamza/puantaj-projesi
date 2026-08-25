from django.urls import path
from . import views
urlpatterns = [
    path("mesai/", views.mesai_liste, name="ek_kazanc_mesai_liste"),
    path("mesai/yeni/", views.mesai_yeni, name="ek_kazanc_mesai_yeni"),
    path("mesai/toplu/", views.mesai_toplu, name="ek_kazanc_mesai_toplu"),
    path("mesai/<int:pk>/sil/", views.mesai_sil, name="ek_kazanc_mesai_sil"),
    path("prim/", views.prim_liste, name="ek_kazanc_prim_liste"),
    path("prim/yeni/", views.prim_yeni, name="ek_kazanc_prim_yeni"),
    path("prim/<int:pk>/sil/", views.prim_sil, name="ek_kazanc_prim_sil"),
]
