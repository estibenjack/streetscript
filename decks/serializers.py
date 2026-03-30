from rest_framework import serializers
from .models import Deck, Card

'''
used sample data previously, now using models and postgres db so:
using serializers.ModelSerializer instead of .Serializer
--> instead of defining the fields manually, it reads the model and knows
    the fields already
Meta class tells it which model to use

- in terms of order, Card depends on Deck in the model bc of foreign key
-- child before parent: parent serializer will reference the child serializer
'''

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