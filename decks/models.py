from django.db import models

'''
- django models inherit from models.Model to get django's orm functionality
- having CASCADE in the foreign key r/ship means all related cards are deleted
  from a deck if it's deleted
- related_name='cards' let's us do deck.cards.all() to get all cards for a deck
'''
class Deck(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="decks")
    description = models.TextField()
    language = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    front = models.CharField(max_length=200)
    back = models.CharField(max_length=200)
    context = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.front} -> {self.back}"