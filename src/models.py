from dataclass import dataclass
from enum import Enum
from typing import List


BLACKJACK_WIN = 21


class CardSuit(Enum):
  HEART = 1
  DIAMOND = 2
  SPADE = 3
  CLUB = 4


class CardValue(Enum):
  ACE = 1
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

  @property
  def score(self) -> int:
    return self._score
  
  def _calculate_score(self) -> None:
    total = 0
    for card in self.hand:
      total += min(10, card.value.value)
      # Change ace from 1 to 11 if it doesn't cause busting
      total += 10 if card.value == CardValue.ACE and total <= BLACKJACK_WIN - 10 else 0

    self._score = total

  def add_card(self, card: Card) -> None:
    self.hand.append(card)
    self._calculate_score()


class Deck:
  cards: List[Card] = []

  def __init__(self):
    self.cards = [Card(suit, value) for suit in CardSuit for value in CardValue]
    self.shuffle()

  def shuffle(self):
    # Perform ruffle shuffle 7 times
    for _ in range(7):
      halves = [self.cards[:len(self.cards) // 2], self.cards[len(self.cards) // 2:]]
      picked_half = 0
      self.cards = []
      while halves[picked_half]:
        self.cards.append(halves[picked_half].pop())
        picked_half = (picked_half + 1) % 2
      self.cards += halves[0] + halves[1]
