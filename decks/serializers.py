from rest_framework import serializers
from .models import Deck, Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'deck', 'front', 'back', 'context', 'created_at']
        
class DeckSerializer(serializers.ModelSerializer):
    # read-only so user is returned in responses but never set by the client
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Deck
        fields = ['id', 'name', 'user', 'description', 'language', 'created_at']