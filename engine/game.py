from engine.core import Deck, Player, Dealer, Message
from engine.enums import TurnState, Actions
from typing import Self


class Game:
    def __init__(self, deck_count: int = 6):
        self.deck = Deck(deck_count = deck_count)
        self.dealer = Dealer()
        self.player = Player()

        self.state = TurnState.PLAYER_TURN

        self._messages: list[Message] = []


    def check_state(self, state: TurnState) -> bool:
        return self.state == state
    
    def get_message(self) -> Message | None:
        if not self._messages:
            return None
        
        return self._messages.pop(0)
    
    def add_message(self, message: Message) -> None:
        if not message:
            return
        
        self._messages.append(message)
        
    def prepare_game(self) -> Self:
        self._messages.clear()

        if len(self.deck) < self.deck.deck_count * 52 // 4:
            self.deck.regenerate()

        self.deck.shuffle()

        self.player.clear_hand()
        self.dealer.clear_hand()

        for _ in range(2):
            self.deck.give_cards(self.dealer, 1)
            self.deck.give_cards(self.player, 1)

        self.set_state(TurnState.PLAYER_TURN)

        if self.check_state(TurnState.PLAYER_TURN):
            self.add_message(self.view())

            
        return self

    def view(self) -> Message:
        return Message(
            f"-- GAME --\n\n"

            f"Dealer: {self.dealer.card_view(hidden = True)}\n"
            f"YOU: {self.player.card_view()} - ({self.player.score})\n\n"

            # "[D] - Double Down\n"
            # "[P] - Split\n"
            # "[R] - Surrender...\n"
            ,

            options = (
                ("Hit me!", Actions.HIT),
                ("Stand", Actions.STAND)
            )
        )

    def set_state(self, state: TurnState) -> None:
        self.state = state

        if self.state == TurnState.PLAYER_TURN:
            if len(self.player.cards) == 2 and self.player.score == 21:
                self.add_message(Message(
                    f"{self.player.card_view()}\n"

                    "BLACKJACK!"
                ))
                self.set_state(TurnState.DEALER_TURN)


    def player_action(self, action: Actions) -> bool | None:
        if not self.state == TurnState.PLAYER_TURN:
            return

        self.add_message(self.view())
        option: Actions = action

        match option:
            case Actions.HIT:
                self.deck.give_cards(self.player, amount = 1)

                if self.player.busted:
                    # busted!

                    self.set_state(TurnState.FINISHED)

                elif self.player.score == 21:
                    # 21!

                    self.set_state(TurnState.DEALER_TURN)
                    

            case Actions.STAND:
                self.set_state(TurnState.DEALER_TURN)
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
        
        self.add_message(Message(
            "DEALER'S TURN!\n\n"
            "The Evil Dealer reveals his hidden card...\n"
            f"{self.dealer.card_view(hidden = False)}\n"
        ))

        cards_hitted: int = 0

        while(self.dealer.score < 17): #S17
            self.deck.give_cards(self.dealer, amount = 1)
            self.add_message(Message(f"{self.dealer.card_view(hidden = False)} - {self.dealer.score}"))
            cards_hitted += 1

        if cards_hitted == 0:
            self.add_message(Message("The Dealer stands. No more cards for him."))

        self.set_state(TurnState.FINISHED)

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
        # while True:
        #     self.prepare_game()

        #     explode = False

        #     while self.state == TurnState.PLAYER_TURN:
        #         player_turn = self.player_action()

        #         if player_turn is False:
        #             self.add_message("Your sins caused the world to explode. Hope you are proud of yourself.")
        #             explode = True
        #             break
        #         elif player_turn is None:
        #             raise RuntimeError("It is not player's turn.")

        #     if explode:
        #         continue

        #     while self.state == TurnState.DEALER_TURN:
        #         self.dealer_turn()

        #     if self.state == TurnState.FINISHED:
        #         winner: Player | None = self.determine_winner()

        #         winner_str: str = "The Evil Dealer" if winner == self.dealer else "YOU" if winner == self.player else "None! Both of you got the same points"

        #         self.add_message(
        #             f"Dealer: {self.dealer.card_view(hidden = False)}: ({self.dealer.score})\n"
        #             f"YOU: {self.player.card_view()}: ({self.player.score})\n\n"

        #             f"The winner is... {winner_str}!"
        #         )

        #         # recompensas

        #         self.add_message(
        #             "Wanna play against this malevolent dealer again?\n\n"

        #             "[Y] - Yes\n"
        #             "[N] - No\n"
        #         )
        #         answer = self.player.choose_action()

        #         if answer and answer[0] == "Y":
        #             continue
        #         else:
        #             self.add_message("Thank you for your patience (and your chips).")
        #             break
        #     else:
        #         raise RuntimeError(f"This shouldn't happen... TurnState is {self.state}")

        # return self
        ...
        


if __name__ == "__main__":
    game = Game().play()

