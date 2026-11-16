from __future__ import annotations
from dataclasses import dataclass, field
from engine.enums import Ranks, Suits
import random
from engine.enums import Actions

CARD_SCORES: dict[Ranks, int] = {
    Ranks.ACE: 1, # or 11
    Ranks.TWO: 2,
    Ranks.THREE: 3,
    Ranks.FOUR: 4,
    Ranks.FIVE: 5,
    Ranks.SIX: 6,
    Ranks.SEVEN: 7,
    Ranks.EIGHT: 8,
    Ranks.NINE: 9,
    Ranks.TEN: 10,
    Ranks.JACK: 10,
    Ranks.QUEEN: 10,
    Ranks.KING: 10,
}

RANK_SYMBOLS: dict[Ranks, str] = {
    Ranks.ACE: "A",
    Ranks.TWO: "2",
    Ranks.THREE: "3",
    Ranks.FOUR: "4",
    Ranks.FIVE: "5",
    Ranks.SIX: "6",
    Ranks.SEVEN: "7",
    Ranks.EIGHT: "8",
    Ranks.NINE: "9",
    Ranks.TEN: "10",
    Ranks.JACK: "J",
    Ranks.QUEEN: "Q",
    Ranks.KING: "K",
}

SUIT_SYMBOLS: dict[Suits, str] = {
    Suits.HEARTS: "♥",
    Suits.DIAMONDS: "♦",
    Suits.CLUBS: "♣",
    Suits.SPADES: "♠",
}

@dataclass(frozen = True)
class Card:
    rank: Ranks
    suit: Suits

    long_str: bool = field(default = False, compare = False, hash = False, repr = False) # Não afeta o hash da frozen dataclass

    def __repr__(self) -> str:
        return f"Card Object: Rank = {self.rank}, Suit = {self.suit}"

    def __str__(self) -> str:
        if self.long_str:
            return f"{self.rank.name.lower().capitalize()} of {self.suit.name.lower().capitalize()}"

        return f"{RANK_SYMBOLS[self.rank]}{SUIT_SYMBOLS[self.suit]}"

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

    def regenerate(self) -> None:
        self.cards.clear()
        self.cards = self.generate_cards(self.deck_count)

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

    def __len__(self):
        return len(self.cards)

class Player:
    def __init__(self):
        self.cards: list[Card] = []

        self._score: int | None = None

    def clear_hand(self) -> None:
        self.cards.clear()
        self._score = None

    def receive_card(self, card: Card) -> None:
        self.cards.append(card)
        self._score = None # invalida o cache

    def card_view(self) -> str:
        return ", ".join([str(card) for card in self.cards])

    def choose_action(self) -> str:
        return input().strip().upper()

    @property
    def score(self) -> int:
        if self._score is None:
            temp_cards: list[Card] = self.cards.copy()

            ace: bool = any(card.rank == Ranks.ACE for card in temp_cards)

            if ace:
                for card in temp_cards:
                    if card.rank == Ranks.ACE:
                        temp_cards.remove(card)
                        break

            score_partial: int = sum(CARD_SCORES[card.rank] for card in temp_cards)

            if ace:
                score_partial += 11 if score_partial + 11 <= 21 else 1

            self._score = score_partial

        return self._score

    @property
    def busted(self) -> bool:
        return self.score > 21

class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()

    def card_view(self, hidden: bool):
        cards_str = [str(card) for card in self.cards]

        if hidden and len(self.cards) > 1:
            cards_str[1] = "???"

        return ", ".join(cards_str)

    def choose_action(self):
        return super().choose_action() # depois lógica do dealer, mas depois vemos



@dataclass(frozen = True)
class Message:
    text: str

    options: tuple[tuple[str, Actions], ...] | None = field(default = None, kw_only = True)

    def __bool__(self):
        return bool(self.text.strip())

    def __str__(self):
        return self.text
    