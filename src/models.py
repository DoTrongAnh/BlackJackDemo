from dataclass import dataclass
from enum import Enum
from typing import List


class CardSuit(Enum):
  HEART = 1
  DIAMOND = 2
  SPADE = 3
  CLUB = 4


class CardValue(Enum):
  ACE = 0
  ONE = 1
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6
  SEVEN = 7
  EIGHT = 8
  NINE = 9
  TEN = 10
  JACK = 11
  QUEEN = 12
  KING = 13


@dataclass
class Card:
  value: CardValue
  suit: CardSuite


class Player:
  hand: List[Card] = []
