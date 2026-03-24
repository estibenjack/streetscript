from rest_framework import serializers
from .models import Deck, Card

'''
used sample data previously, not using models and postgres db so:
using serializers.ModelSerializer instead of .Serializer
--> instead of deining the fields manually, it reads the model and knows
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
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'language', 'created_at']