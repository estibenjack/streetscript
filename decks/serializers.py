from rest_framework import serializers

class CardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    deck_id = serializers.IntegerField()
    front = serializers.CharField()
    back = serializers.CharField()
    context = serializers.CharField()

class DeckSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    language = serializers.CharField()