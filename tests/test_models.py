from blackjack_demo.models import Card, CardSuit, CardValue, Player
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
    assert len(new_player.hand) == hand_size, 'Player should have {hand_size} cards, not {len(new_player.hand)}'
