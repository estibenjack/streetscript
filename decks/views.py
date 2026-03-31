from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer
from .generate import generate_flashcards
from .genius import fetch_lyrics


@api_view(['GET', 'POST'])
def decks_list(request):
    if request.method == 'GET':
        decks = Deck.objects.filter(user=request.user)
        serializer = DeckSerializer(decks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = DeckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) # user assigned from token, not req body
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def deck_detail(request, deck_id):
    try:
        # filter by user so users only see their own decks
        deck = Deck.objects.get(id=deck_id, user=request.user)
    except Deck.DoesNotExist:
        return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DeckSerializer(deck)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = DeckSerializer(deck, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        serializer = DeckSerializer(deck, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        deck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cards_for_deck(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id, user=request.user)
    except Deck.DoesNotExist:
        return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        cards = Card.objects.filter(deck=deck)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def card_detail(request, deck_id, card_id):
    try:
        deck = Deck.objects.get(id=deck_id, user=request.user)
    except Deck.DoesNotExist:
        return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)
        
    try:
        card = Card.objects.get(id=card_id, deck=deck)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def generate_cards(request, deck_id):
    try:
        deck = Deck.objects.get(id=deck_id, user=request.user)
    except Deck.DoesNotExist:
        return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    lyrics = request.data.get('lyrics')
    if not lyrics:
        return Response({'error': 'No lyrics provided'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = generate_flashcards(lyrics)
        flashcards = result['cards']
    except Exception as e:
        return Response(
            {'error': 'Failed to generate flashcards. Please try again.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    created_cards = []
    
    # cards saved individually rather than bulk_create to use 
    # serializer validation on each card
    for card_data in flashcards:
        card_data['deck'] = deck.id
        serializer = CardSerializer(data=card_data)
        if serializer.is_valid():
            serializer.save()
            created_cards.append(serializer.data)
    return Response(created_cards, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def from_song(request):
    song_title = request.data.get('song_title')
    artist = request.data.get('artist')
    
    if not song_title or not artist:
        return Response({'error': 'song_title and artist are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lyrics = fetch_lyrics(song_title, artist)
    except Exception as e:
        return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not lyrics:
        return Response({'error': 'No lyrics provided'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = generate_flashcards(lyrics)
        flashcards = result['cards']
        language = result['language']
    except Exception as e:
        return Response({
            'error': 'Failed to generate flashcards. Please try again.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    deck = Deck.objects.create(
        name=f"{artist} - {song_title}",
        description=f"Auto-generated from {song_title} by {artist}",
        language=language,
        user=request.user
    )
    
    created_cards = []
    
    for card_data in flashcards:
        card_data['deck'] = deck.id
        serializer = CardSerializer(data=card_data)
        if serializer.is_valid():
            serializer.save()
            created_cards.append(serializer.data)
    return Response(created_cards, status=status.HTTP_201_CREATED)
        