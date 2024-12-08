import random
from master_data import STARTING_DECK, CARDS_VALUE
from game_of_blackjack import game_of_blackjack

def shuffle(decks):
    # Building a deck
    deck = []
    for i in range(decks):
        deck += STARTING_DECK
    random.shuffle(deck)
    return deck             


def BJ_simulator(iterations: int = 1,
                 bankroll: float = 10000,
                 shoe_size: int = 8,
                 bet_size: int = 100,
                 games_per_deck=8,
                 min_table_bet: int = 100,
                 max_table_bet: int = 10000,
                 players_engine='basic') -> dict:
    
    data = {
    'Starting cards': [],
    'Dealers card': [],
    'Hands amount': [],
    '$result': [],
    'Running count': [],
    'True count': [],
    'Cards left at start': [],
    'Cards Left after the game': []}
    
    for i in range(iterations):
        deck = shuffle(decks=shoe_size)
        for n in range(games_per_deck * shoe_size):
            running_count = 0
            for card in list(deck):
                if CARDS_VALUE[card] in [10, 11]:
                    running_count += 1
                elif CARDS_VALUE[card] in range(2, 7):
                    running_count -= 1

            cards_at_start = len(deck)
            true_count = running_count / (cards_at_start / 52)
            
            if players_engine != 'basic':
                # Kelly criterion implementation
                if true_count <= 2:
                    bet = min_table_bet
                elif true_count > 2:
                    p = 0.495 + (true_count * 0.005)
                    bet = bankroll * (2 * p - 1)
                    if bet < min_table_bet:
                        bet = min_table_bet
                    elif bet > max_table_bet:
                        bet = max_table_bet
            else: 
                bet = bet_size

            try:
                single_game_of_blackjack = game_of_blackjack(deck=deck, bet=bet, players_engine=players_engine, true_count=true_count)
                df, dealer_cards = single_game_of_blackjack.play_hand()

                # Calculate result using df as a dictionary
                total_outcome = sum(df['Outcome'])  # Sum of outcomes
                total_bet = sum(df['Bet'])         # Sum of bets
                result = total_outcome - total_bet

                # Extract starting cards
                starting_cards = df['Hand'][0][:2]  # First two cards of the player's initial hand
                cards_left = len(deck)

                # Append game data to the dictionary
                data['Starting cards'].append(starting_cards)
                data['Dealers card'].append(dealer_cards[0])
                data['Hands amount'].append(len(df['Hand']))
                data['$result'].append(result)
                data['Running count'].append(running_count)
                data['True count'].append(true_count)
                data['Cards left at start'].append(cards_at_start)
                data['Cards Left after the game'].append(cards_left)

            except IndexError:
                pass  # Handle cases where the deck runs out of cards

    return data


if __name__ == '__main__':
    data = BJ_simulator(iterations=1)
    print(data['$result'].sum())
    print(data)
