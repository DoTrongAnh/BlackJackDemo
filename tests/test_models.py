import blackjack_demo
from blackjack_demo.models import Card, CardSuit, CardValue, Deck, Game, Player
import pytest
from random import choice


@pytest.mark.parametrize('card_value', [value for value in CardValue])
@pytest.mark.parametrize('card_suit', [suit for suit in CardSuit])
def test_card_creation(card_value, card_suit):
    new_card = Card(card_value, card_suit)
    assert new_card.value == card_value, f'Card value should be {card_value.name}, not {new_card.value.name}'
    assert new_card.suit == card_suit, f'Card suit should be {card_suit.name}, not {new_card.suit.name}'


@pytest.mark.parametrize('hand_size', [1, 2, 3, 4, 5])
def test_player_hand_size(hand_size):
    new_player = Player()
    for _ in range(hand_size):
        new_player.add_card(Card(choice([v for v in CardValue]), choice([s for s in CardSuit])))
    assert len(new_player.hand) == hand_size, f'Player should have {hand_size} cards, not {len(new_player.hand)}'


def test_deck_inventory():
    new_deck = Deck()
    expected_deck_size = len([v for v in CardValue]) * len([s for s in CardSuit])
    actual_deck = set(new_deck.cards)
    assert len(actual_deck) == expected_deck_size, f'Deck should have {expected_deck_size} unique cards, not {len(actual_deck)}'


def test_deck_empty():
    new_deck = Deck()
    new_deck.cards = []
    assert new_deck.is_empty(), 'Deck should be empty'


@pytest.mark.parametrize(
    'win_score,hand,is_bust,is_blackjack',
    [
        (21, [CardValue.ACE, CardValue.TEN], False, True),  # Classic blackjack
        (21, [CardValue.TEN, CardValue.ACE], False, True),
        (21, [CardValue.ACE, CardValue.JACK], False, True),
        (21, [CardValue.JACK, CardValue.ACE], False, True),
        (21, [CardValue.ACE, CardValue.QUEEN], False, True),
        (21, [CardValue.QUEEN, CardValue.ACE], False, True),
        (21, [CardValue.ACE, CardValue.KING], False, True),
        (21, [CardValue.KING, CardValue.ACE], False, True),
        (21, [CardValue.ACE, CardValue.ACE], False, False),
        (22, [CardValue.ACE, CardValue.ACE], False, True),  # Blackjack with two aces
        (20, [CardValue.ACE, CardValue.TEN], True, False),  # Bust with one ace
        (20, [CardValue.ACE, CardValue.NINE], False, True),  # Modified blackjack
    ]
)
def test_player_score(mocker, win_score, hand, is_bust, is_blackjack):
    new_player = Player()
    mocker.patch('blackjack_demo.models.BLACKJACK_WIN', new=win_score)
    for card_value in hand:
        new_player.add_card(Card(card_value, choice([s for s in CardSuit])))
    assert new_player.is_bust() == is_bust, f'Player busting should be {is_bust}'
    assert new_player.is_blackjack() == is_blackjack, f'Player blackjack should be {is_blackjack}'


@pytest.mark.parametrize(
    'min_dealer_score,min_hand_size,min_dealer_hand',
    [
        (17, 1, 2),  # At least 2 cards to reach score 17
        (1, 2, 2),
        (1, 5, 5),
        (23, 1, 3),  # At least 3 cards to reach score 23
    ]
)
def test_game_dealer_hand(mocker, min_dealer_score, min_hand_size, min_dealer_hand):
    mocker.patch('blackjack_demo.models.MIN_DEALER_SCORE', new=min_dealer_score)
    mocker.patch('blackjack_demo.models.INITIAL_HAND_SIZE', new=min_hand_size)
    new_game = Game(1)
    assert len(new_game.dealer.hand) >= min_dealer_hand, f'Dealer should have at least {min_dealer_hand}, not {len(new_game.dealer.hand)}'


@pytest.mark.parametrize(
    'min_dealer_score,win_score',
    [(20, 19), (21, 20), (22, 21)]
)
def test_game_dealer_bust(mocker, min_dealer_score, win_score):
    mocker.patch('blackjack_demo.models.BLACKJACK_WIN', new=win_score)
    mocker.patch('blackjack_demo.models.MIN_DEALER_SCORE', new=min_dealer_score)
    num_players = 3
    new_game = Game(num_players)
    assert new_game.dealer.is_bust(), 'Dealer should be bust'
    new_game.update_outcome()
    assert new_game.outcome == {i: 'win' for i in range(num_players)}
    assert new_game.is_ended(), 'Game should have ended'


@pytest.mark.parametrize('win_score', [21, 22, 25, 30, 41])
def test_game_dealer_blackjack(mocker, win_score):
    mocker.patch('blackjack_demo.models.BLACKJACK_WIN', new=win_score)
    num_players = 3
    new_game = Game(num_players)
    mocker.patch.object(Game, 'dealer._score', new=win_score)
    assert new_game.dealer.is_blackjack(), 'Dealer should be blackjack'
    new_game.update_outcome()
    assert new_game.outcome == {i: 'lose' for i in range(num_players)}
    assert new_game.is_ended(), 'Game should have ended'
