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
                 games_per_deck = 8,
                 min_table_bet: int = 100,
                 max_table_bet: int = 10000,
                 decision_engine='basic') -> dict:
    """
    shoe_size: the amount of full decks of cards (52) that are shuffled to make the shoe
    games_per_deck: the amount of games per deck in shoe the simulation will deal before reshuffling
    decision_engine: defines the decision engine of player. Possible: 'basic', 'kelly', 'kelly_and_exceptions'
        decision engine is different than players_engine inside the game_of_blackjack
        'basic' is neither adjusting bet sizes nor playing True Count exceptions
        'kelly' is adjusting the bet sizes but not playing True Count exceptions
        'kelly_and_exceptions' is both adjusting the bet sizes and playing True Count exceptions
        decision_engine may also be a dictionary with ranges for True Count in key and bet size in value
    """


    data = {
    'Starting cards': [],
    'Dealers card': [],
    'Hands amount': [],
    '$result': [],
    '$account': [],
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
            true_count = running_count / ((cards_at_start + 1) / 52)
            
            if decision_engine == 'kelly':
                # Kelly criterion implementation
                players_engine = 'basic'
                if true_count <= 2:
                    bet = min_table_bet
                elif true_count > 2:
                    p = 0.495 + (true_count * 0.005)
                    bet = bankroll * (2 * p - 1)
                    if bet < min_table_bet:
                        bet = min_table_bet
                    elif bet > max_table_bet:
                        bet = max_table_bet

            elif decision_engine == 'kelly_and_exceptions':
                # Kelly criterion implementation and exceptions play
                players_engine = 'exceptions'
                if true_count <= 2:
                    bet = min_table_bet
                elif true_count > 2:
                    p = 0.495 + (true_count * 0.005)
                    bet = bankroll * (2 * p - 1)
                    if bet < min_table_bet:
                        bet = min_table_bet
                    elif bet > max_table_bet:
                        bet = max_table_bet



            elif isinstance(decision_engine, dict):
                players_engine = 'exceptions'
                for (low,high), bet_value in decision_engine.items(): #bet_value is value from dict
                    if low <= true_count < high: #checking if current True Count is in range
                        bet = bet_value
                
            else:
                bet = bet_size
                players_engine = 'basic'


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

                # Calculating current bankroll
                bankroll += result

                # Append game data to the dictionary
                data['Starting cards'].append(starting_cards)
                data['Dealers card'].append(dealer_cards[0])
                data['Hands amount'].append(len(df['Hand']))
                data['$result'].append(result)
                data['$account'].append(bankroll)
                data['Running count'].append(running_count)
                data['True count'].append(true_count)
                data['Cards left at start'].append(cards_at_start)
                data['Cards Left after the game'].append(cards_left)
                
            except IndexError:
                pass  # Handle cases where the deck runs out of cards

    return data


if __name__ == '__main__':
    data = BJ_simulator(iterations=1000, games_per_deck = 8, shoe_size = 1, decision_engine = 'kelly_and_exceptions')
    print(data)
    #print(sum(data['$result']))
