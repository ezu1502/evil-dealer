from dataclasses import dataclass
from enums import Ranks, Suits
import random

@dataclass(frozen = True)
class Card:
    rank: Ranks
    suit: Suits

    def __repr__(self) -> str:
        return f"Card Object: Rank = {self.rank}, Suit = {self.suit}"

    def __str__(self) -> str:
        return f"{self.rank.name.lower().capitalize()} of {self.suit.name.lower().capitalize()}"

class Deck:
    def __init__(self, deck_count: int = 6) -> None:
        self.deck_count = deck_count
        self.cards = self.generate_cards(self.deck_count)

    @staticmethod
    def generate_cards(deck_count: int) -> list[Card]:
        if not 1 <= deck_count <= 8:
            raise ValueError("Deck amount must be between 1 and 8")
        
        cards = [Card(rank = rank, suit = suit) for rank in Ranks for suit in Suits] * deck_count

        return cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError("Cannot draw from empty deck!")

        return self.cards.pop()
    

    def give_cards(self, target: Player, amount: int = 1):
        for _ in range(amount):
            card = self.draw()
            target.receive_card(card)

    def __str__(self) -> str:
        return f"Deck object containing {self.deck_count} decks"

class Player:
    def __init__(self):
        self.cards: list[Card] = []

    def receive_card(self, card: Card):
        self.cards.append(card)

class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()