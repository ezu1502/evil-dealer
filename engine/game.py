from core import Deck, Player, Dealer
from enums import TurnState, Actions
from typing import Self

class Game:
    def __init__(self, deck_count: int = 6):
        self.deck = Deck(deck_count = deck_count)
        self.dealer = Dealer()
        self.player = Player()

        self.state = TurnState.PLAYER_TURN

    def prepare_game(self) -> Self:
        if len(self.deck) < self.deck.deck_count * 52 // 4:
            self.deck.regenerate()

        self.deck.shuffle()

        self.player.clear_hand()
        self.dealer.clear_hand()

        for _ in range(2):
            self.deck.give_cards(self.dealer, 1)
            self.deck.give_cards(self.player, 1)

        self.state = TurnState.PLAYER_TURN
        return self

    def view(self):
        return (
            f"-- GAME --\n\n"

            f"Dealer: {self.dealer.card_view(hidden = True)}\n"
            f"YOU: {self.player.card_view()} - ({self.player.score})\n\n"

            "[H] - Hit me!\n"
            "[S] - Stand\n"
            # "[D] - Double Down\n"
            # "[P] - Split\n"
            # "[R] - Surrender...\n"
        )

    def player_turn(self) -> bool | None:
        if not self.state == TurnState.PLAYER_TURN:
            return

        if len(self.player.cards) == 2 and self.player.score == 21:
            print(
                f"{self.player.card_view()}\n"

                "BLACKJACK!"
            )
            self.state = TurnState.DEALER_TURN

            return True
        
        print(self.view())
        option: str = self.player.choose_action()

        attempts: int = 0

        while (not option or option[0] not in Actions) and attempts < 3:
            attempts += 1
            option: str = self.player.choose_action()
            

        if attempts >= 3:
            # explodir o mundo
            return False

        option = option[0]

        match option:
            case Actions.HIT:
                self.deck.give_cards(self.player, amount = 1)

                if self.player.busted:
                    # busted!

                    self.state = TurnState.FINISHED

                elif self.player.score == 21:
                    # 21!

                    self.state = TurnState.DEALER_TURN

            case Actions.STAND:
                self.state = TurnState.DEALER_TURN
            # case Actions.DOUBLE:
            #     ...
            # case Actions.SPLIT:
            #     ...
            # case Actions.SURRENDER:
            #     ...
            case _:
                raise RuntimeError(f"Invalid Action: {option}")

        return True

    def dealer_turn(self):
        if not self.state == TurnState.DEALER_TURN:
            return
        
        print(
            "DEALER'S TURN!\n\n"
            "The Evil Dealer reveals his hidden card...\n"
            f"{self.dealer.card_view(hidden = False)}\n"
        )

        cards_hitted: int = 0

        while(self.dealer.score < 17): #S17
            self.deck.give_cards(self.dealer, amount = 1)
            print(f"{self.dealer.card_view(hidden = False)} - {self.dealer.score}")
            cards_hitted += 1

        if cards_hitted == 0:
            print("The Dealer stands. No more cards for him.")

        self.state = TurnState.FINISHED

    def determine_winner(self) -> Player | None:
        if not self.state == TurnState.FINISHED:
            return
        
        if self.player.busted:
            return self.dealer

        elif self.dealer.busted:
            return self.player

        if self.player.score == self.dealer.score:
            return None

        return self.player if self.player.score > self.dealer.score else self.dealer

    def play(self) -> Self:
        while True:
            self.prepare_game()

            explode = False

            while self.state == TurnState.PLAYER_TURN:
                player_turn = self.player_turn()

                if player_turn is False:
                    print("Your sins caused the world to explode. Hope you are proud of yourself.")
                    explode = True
                    break
                elif player_turn is None:
                    raise RuntimeError("It is not player's turn.")

            if explode:
                continue

            while self.state == TurnState.DEALER_TURN:
                self.dealer_turn()

            if self.state == TurnState.FINISHED:
                winner: Player | None = self.determine_winner()

                winner_str: str = "The Evil Dealer" if winner == self.dealer else "YOU" if winner == self.player else "None! Both of you got the same points"

                print(
                    f"Dealer: {self.dealer.card_view(hidden = False)}: ({self.dealer.score})\n"
                    f"YOU: {self.player.card_view()}: ({self.player.score})\n\n"

                    f"The winner is... {winner_str}!"
                )

                # recompensas

                print(
                    "Wanna play against this malevolent dealer again?\n\n"

                    "[Y] - Yes\n"
                    "[N] - No\n"
                )
                answer = self.player.choose_action()

                if answer and answer[0] == "Y":
                    continue
                else:
                    print("Thank you for your patience (and your chips).")
                    break
            else:
                raise RuntimeError(f"This shouldn't happen... TurnState is {self.state}")

        return self
        


if __name__ == "__main__":
    game = Game().play()

