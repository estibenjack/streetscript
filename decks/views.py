from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.http import JsonResponse
# from .sample_data import SAMPLE_DECKS, SAMPLE_CARDS
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer

@api_view(['GET'])
def get_decks(request):
    decks = Deck.objects.all()
    serializer = DeckSerializer(decks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_deck(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return JsonResponse({'error': 'Deck not found'}, status=404)
    serializer = DeckSerializer(deck)
    return JsonResponse(serializer.data, safe=False)
    '''
    return Response(serializer.data)
    if using Response instead of JsonResponse, add safe=False since it's expecting a 
  
    '''

@api_view(['GET'])
def get_cards_for_deck(request, deck_id):
    cards = Card.objects.filter(deck_id=deck_id)
    serializer = CardSerializer(cards, many=True)
    return JsonResponse(serializer.data, safe=False)