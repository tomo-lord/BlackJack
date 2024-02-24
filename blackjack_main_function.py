import pandas as pd
import numpy as np
import random
from master_data import STARTING_DECK, CARDS_VALUE
from game_of_blackjack import game_of_blackjack

def shuffle(decks):
    #building a deck
    deck = []
    for i in range(decks):
        deck += STARTING_DECK
    random.shuffle(deck)
    return deck             


def BJ_simulator(iterations: int, bankroll: float = 10000, shoe_size: int = 8, bet_size: int = 100, games_per_deck=8, min_table_bet: int = 100, max_table_bet: int = 10000) -> pd.DataFrame:
    
    data = pd.DataFrame({'Starting cards': [], 'Dealers card': [], 'Hands amount': [], '$result': [], 'Running count': [],'True count':[], 'Cards left at start': [], 'Cards Left after the game':[]})
    
    for i in range(iterations):
        deck = shuffle(decks=shoe_size)
        for n in range(games_per_deck*shoe_size):
            running_count = 0
            for card in list(deck):
                if CARDS_VALUE[card] in [10, 11]:
                    running_count += 1
                elif CARDS_VALUE[card] in range(2, 7):
                    running_count -= 1

            cards_at_start = len(deck)
            true_count = running_count/(cards_at_start/52)
            
            # Kelly criterion implementation (assumes OR = 1, and p = 0.495 + (true_count*0.005))
            if true_count <= 2:
                bet = min_table_bet
            elif true_count > 2:
                p = 0.495 + (true_count*0.005)
                bet = bankroll*(2*p-1)
                if bet < min_table_bet:
                    bet = min_table_bet
                elif bet > max_table_bet:
                    bet = max_table_bet

            single_game_of_blackjack = game_of_blackjack(deck=deck, bet = bet, players_engine = 'deviation', true_count=true_count)

            df, dealer_cards = single_game_of_blackjack.play_hand()
            cards_left = len(deck)
            result = df['Outcome'].sum() - df['Bet'].sum()
            starting_cards = list(df.loc[0,'Hand'])[:2]
            w = pd.DataFrame({'Starting cards': [starting_cards], 'Dealers card': [dealer_cards[0]],'Hands amount':[len(df)], '$result': [result], 'Running count': [running_count],'True count':[true_count], 'Cards left at start': [cards_at_start], 'Cards Left after the game':[cards_left]})
            data = pd.concat([data, w], ignore_index=True, axis=0)
            
    return data


if __name__ == '__main__':
    # FIX area
    # shuffle(1)
    # deck[0] = 'Club A'
    # deck[1] = 'Diamond Q'
    # deck[2] = 'Spade A'
    # deck[3] = 'Heart J'


    # df, dealers_cards = game_of_blackjack(bet=100)
    # print(df)
    # print(dealers_cards)

    data = BJ_simulator(iterations=1)
    print(data['$result'].sum())
    print(data)

