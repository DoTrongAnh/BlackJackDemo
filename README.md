# BlackJackDemo

![Unittests status badge](https://github.com/DoTrongAnh/BlackJackDemo/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/DoTrongAnh/BlackJackDemo/workflows/Coverage/badge.svg)

A simple project for coding practice

## Sketching ideas
- Card: class
  - Has a suit (enum)
  - Has a value (enum)
- Player: class
  - Has a hand (list of Cards)
  - Calculates score from hand
- Deck: class
  - Has a list of all the Cards (all enum combinations)
  - Shuffles the cards
- Game: class
  - Has a dealer (Player)
  - Has a list of Players
  - Shuffles and deals two cards to dealer and each player
  - Dealer keeps drawing cards until hand exceeds 17
  - If dealer busts, every player wins
  - If dealer hits Blackjack, every player loses
  - Players take turns making decisions (hit or call)
  - Players with lower score than dealer or busting, lose
  - Players with higher score than dealer or hitting Blackjack, win
- Interface: console print
  - Initialize the Game
  - Each player's turn, show their hand and ask for input (hit or call)
  - End player's turn if player calls, busts, or hits Blackjack.
  - Show dealer's hand after everyone's turn ends
  - List outcome for each player (win, lose, draw)
