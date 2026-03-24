from django.urls import path
from . import views

urlpatterns = [
  path('decks/', views.decks_list, name='decks_list'),
  path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
  path('decks/<int:deck_id>/cards/', views.cards_for_deck, name='cards_for_deck'),
]