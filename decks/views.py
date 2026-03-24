from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.http import JsonResponse
from .sample_data import SAMPLE_DECKS, SAMPLE_CARDS
from .serializers import DeckSerializer, CardSerializer

@api_view(['GET'])
def get_decks(request):
    serializer = DeckSerializer(SAMPLE_DECKS, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_deck(request, deck_id):
    deck = next((d for d in SAMPLE_DECKS if d['deck_id'] == deck_id), None)
    if deck is None:
        return JsonResponse({'error': 'Deck not found'}, status=404)
    serializer = DeckSerializer(deck)
    '''
    return Response(serializer.data)
    if using Response instead of JsonResponse, add safe=False since it's expecting a 
  
    '''
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_cards_for_deck(request, deck_id):
    cards = [c for c in SAMPLE_CARDS if c['deck_id'] == deck_id]
    serializer = CardSerializer(cards, many=True)
    return JsonResponse(serializer.data, safe=False)