from django.urls import path
from . import views
urlpatterns = [path("", views.raporlar_index, name="raporlar_index_main")]
