from model import Card, CardSuit, CardValue
import pytest


@pytest.mark.parametrize('card_value', [value for value in CardValue])
@pytest.mark.parametrize('card_suit', [suit for suit in CardSuit])
def test_card_creation(card_value, card_suit):
    new_card = Card(card_value, card_suit)
    assert new_card.value == card_value, f'Card value should be {card_value.name}, not {new_card.value.name}'
    assert new_card.suit == card_suit, f'Card suit should be {card_suit.name}, not {new_card.suit.name}'
