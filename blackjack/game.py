from core import Card, Deck, Player, Dealer

class Game:
    def __init__(self, deck_count: int = 6):
        self.deck = Deck(deck_count = deck_count)
        self.dealer = Dealer()
        self.player = Player()

    def start(self):
        self.deck.shuffle()

        for _ in range(2):
            self.deck.give_cards(self.dealer, 1)
            self.deck.give_cards(self.player, 1)

    def view(self):
        return (
            f"-- BLACKJACK --\n"
        )