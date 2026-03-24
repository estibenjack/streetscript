from django.urls import path
from . import views

urlpatterns = [
  path('decks/', views.get_decks, name='get_decks'),
  path('decks/<int:deck_id>/', views.get_deck, name='get_deck'),
  path('decks/<int:deck_id>/cards/', views.get_cards_for_deck, name='get_cards_for_deck')
]