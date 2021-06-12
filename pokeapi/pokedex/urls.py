from django.urls import path

from .views import Insert, TemplatePokemonView, Search
from . import views

urlpatterns = [
	path('insert/<int:id>', Insert),
	path('', views.TemplatePokemonView.as_view(), name='index'),
	path('search', Search, name='search'),
]
