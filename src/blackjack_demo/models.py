from dataclasses import dataclass
from enum import Enum
from typing import List


BLACKJACK_WIN = 21
INITAL_HAND_SIZE = 2


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


@dataclass(eq=True, frozen=True)
class Card:
  value: CardValue
  suit: CardSuit

  def __str__(self):
    return f'{self.value.name} of {self.suit.name}'


class Player:
  hand: List[Card] = []
  _score: int = 0

  def __init__(self):
    self.hand = []
    self._score = 0

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

  def is_bust(self) -> bool:
    return self._score > BLACKJACK_WIN

  def is_blackjack(self) -> bool:
    return self._score == BLACKJACK_WIN


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

  def is_empty(self):
    return len(self.cards) == 0


class Game:
  dealer = Player()
  players: List[Player] = []
  outcome: List[str] = []
  deck = Deck()

  def __init__(self, num_of_players):
    self.players = [Player() for _ in range(num_of_players)]
    for _ in range(INITIAL_HAND_SIZE):
      dealer.add_card(self.deck.cards.pop())

    if dealer.is_blackjack():
      self.outcome = ['lose' for _ in self.players]
      print(f'Dealer scores {self.dealer.score}. Dealer hits Blackjack!')
      return

    if dealer.is_bust():
      self.outcome = ['win' for _ in self.players]
      print(f'Dealer scores {self.dealer.score}. Dealer is bust!')
      return

    for _ in range(INITIAL_HAND_SIZE):
      [p.add_card(self.deck.cards.pop()) for p in self.players if not self.deck.is_empty()]

  def announce_outcome(self) -> str:
    return '\n'.join([f'Player {p}: {o}' for p, o in enumerate(self.outcome)])

  def is_ended(self) -> bool:
    return len(self.outcome) == len(self.players)

  def calculate_outcome(self):
    # Only calculate this if the dealer is neither bust nor blackjack
    self.outcome = []
    for p in self.players:
      self.outcome.append('win' if p.is_blackjack() or p.score > self.dealer.score else ('lose' if p.is_bust() or p.score < self.dealer.score else 'draw'))
