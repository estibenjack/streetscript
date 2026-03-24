from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
# from .sample_data import SAMPLE_DECKS, SAMPLE_CARDS
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer


@api_view(['GET', 'POST'])
def decks_list(request):
    if request.method == 'GET':
        decks = Deck.objects.all()
        serializer = DeckSerializer(decks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        # pass the request body to the serializer here
        serializer = DeckSerializer(data=request.data)
        # validate data against model's field rules
        if serializer.is_valid():
            #write to db (django handles INSERT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def deck_detail(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id)
    except Deck.DoesNotExist:
        return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DeckSerializer(deck)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def cards_for_deck(request, deck_id):
    if request.method == 'GET':
        cards = Card.objects.filter(deck_id=deck_id)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)