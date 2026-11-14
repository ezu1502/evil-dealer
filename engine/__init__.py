"""
    Evil Dealer Engine v0.1.0
    -------------------------

    Blackjack engine for Evil Dealer Bots

    Developed by Ezu.
"""

from .enums import Ranks, Suits, TurnState
from .core import Card, Player, Deck, Dealer
from .game import Game

__all__ = ["Ranks", "Suits", "TurnState", "Card", "Player", "Deck", "Dealer", "Game"]

__version__ = "0.1.0"

__author__ = "Ezu"

__description__ = "Blackjack engine for Evil Dealer bots"