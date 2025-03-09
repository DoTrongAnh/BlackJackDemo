from dataclasses import dataclass
from enum import Enum
from typing import List


BLACKJACK_WIN = 21
INITIAL_HAND_SIZE = 2
MIN_DEALER_SCORE = 17


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
    return self.score == BLACKJACK_WIN


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
  players: List[Player] = []

  def __init__(self, num_of_players):
    self.dealer = Player()
    self.deck = Deck()
    self.outcome = {}
    self.ended = False
    self.players = [Player() for _ in range(num_of_players)]
    while len(self.dealer.hand) < INITIAL_HAND_SIZE or self.dealer.score < MIN_DEALER_SCORE:
      self.dealer.add_card(self.deck.cards.pop())

    for _ in range(INITIAL_HAND_SIZE):
      [p.add_card(self.deck.cards.pop()) for p in self.players if not self.deck.is_empty()]

  def announce_outcome(self) -> str:
    return '\n'.join([f'Player {p}: {o}' for p, o in self.outcome.items()])

  def is_ended(self) -> bool:
    return self.ended

  def update_outcome(self) -> None:
    # Check if the game can end from the dealer's hand
    if self.dealer.is_blackjack():
      self.outcome = {i: 'lose' for i, _ in enumerate(self.players)}
      print(f'Dealer scores {self.dealer.score}. Dealer hits Blackjack!')
      self.ended = True
      return

    if self.dealer.is_bust():
      self.outcome = {i: 'win' for i, _ in enumerate(self.players)}
      print(f'Dealer scores {self.dealer.score}. Dealer is bust!')
      self.ended = True
      return

    # Only calculate this if the dealer is neither bust nor blackjack
    self.outcome = {}
    for i, p in enumerate(self.players):
      self.outcome[i] = 'win' if p.is_blackjack() or p.score > self.dealer.score else ('lose' if p.is_bust() or p.score < self.dealer.score else 'draw')
