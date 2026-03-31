from django.urls import path
from . import views


urlpatterns = [
  path('decks/', views.decks_list, name='decks_list'),
  path('decks/from-song/', views.from_song, name='from_song'),
  path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
  path('decks/<int:deck_id>/cards/', views.cards_for_deck, name='cards_for_deck'),
  path('decks/<int:deck_id>/cards/<int:card_id>/', views.card_detail, name='card_detail'),
  path('decks/<int:deck_id>/cards/generate/', views.generate_cards, name="generate_cards"),
]