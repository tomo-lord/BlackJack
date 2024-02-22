import pandas as pd
import numpy as np
import random


suits = ['Spade', 'Club', 'Diamond', 'Heart']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
possible_cards = [f'{suit} {rank}' for suit in suits for rank in ranks]
starting_deck = list(possible_cards)
cards_value = {f'{suit} {rank}': int(rank) if rank.isdigit() else 10 if rank in ['J', 'Q', 'K'] else 11 for suit in suits for rank in ranks}

def shuffle(decks):
    #building a deck
    global deck
    deck = random.sample(starting_deck, len(starting_deck))
    for i in range(decks - 1):
        deck += random.sample(starting_deck, len(starting_deck))
    return deck




#here I am just assuming the hand played is the first from active hands

#TODO: create enum for engine type ["rand", ...]
#TODO: do a check for BJ for dealer if the upcard is a 10 or A - fix it so it is not reviewed again on casino_move()
def game_of_blackjack(bet : int = 1, players_engine : str = "basic", array_pairs=None, array_soft=None, array_hard=None, true_count : float = 0) -> pd.DataFrame:
    """plays single game of blackjack


    Parameters
    ----------
    players_engine: str
        type of engine to be used

    Returns
    -------
    int
        calculated value of a game
    """
    global deck
    #drawing cards
    players_cards = [deck[0]]
    deck.pop(0)
    players_cards += [deck[0]]
    deck.pop(0)
    dealers_cards = [deck[0]]
    deck.pop(0)
    dealers_cards += [deck[0]]
    deck.pop(0)


    #DataFrame for trackability of hands and bets
    df = pd.DataFrame(columns=['Hand', 'Bet', 'Status', 'Outcome'])
    #Hand is a list of stings containing hands cards
    #Bet is an integer of the bet size for given hand 
    #Status is a sting to indicate if hand is active, played or finished
    #Outcome is the financial result
    df.loc[0,:] = [players_cards, bet, 'Active', None]

    
    def get_value(played_hand: list['str']):
        #hand should be a list argument
        
        #calculate value and adjust for aces
        value = 0
        for card in list(played_hand):
            value += cards_value[card]
            
        aces = 0
        for card in list(played_hand): 
            if card[-1] == "A":
                aces += 1

        while value > 21 and aces >0:
            aces -= 1
            value -= 10
        
        if players_engine == 'rand':
            return value
        else: return value, aces

    #checking for dealers BlackJack
    if cards_value[dealers_cards[0]] in [10, 11]:
        value_dealer, aces_dealer = get_value(dealers_cards)
        if value_dealer == 21:
            for index, row in df.iterrows():
                hand_value, hand_aces = get_value(row['Hand'])
                if hand_value ==21:
                    df.at[index, 'Outcome'] = df.at[index, "Bet"]
                    df.at[index, 'Status'] = 'Finished'
                else:
                    df.at[index, 'Outcome'] = 0
                    df.at[index, 'Status'] = 'Finished'


               
    def check_for_bust(hand_index: int) -> bool:
        played_hand = df.at[hand_index, 'Hand']
        value_hand, aces_hand = get_value(played_hand)
        if value_hand > 21:
            if players_engine == 'rand':
                print("Casino wins")
            df.at[hand_index, 'Status'] = 'Finished'
            df.at[hand_index, 'Outcome'] = 0
            return True
        else:
            return False


    def split(hand_index: int) -> None:
        played_hand = df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if len(played_hand) != 2 or cards_value[played_hand[0]] != cards_value[played_hand[1]]:
            return False
        hand2 = [played_hand[1]]
        list(hand2)
        played_hand.pop(1)
        played_hand.append(deck[0])
        deck.pop(0)
        df.at[hand_index, 'Hand'] = played_hand
        hand2.append(deck[0])
        deck.pop(0)
        df.loc[len(df)] = [hand2, df.at[hand_index, 'Bet'], 'Active', None]
        return


    
    def double(hand_index : int) -> None:
        played_hand = df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if len(played_hand) != 2 or get_value(played_hand) == 21:
            return False
        played_hand.append(deck[0])
        deck.pop(0)
        df.at[hand_index, 'Hand'] = played_hand
        df.at[hand_index, 'Bet'] = 2*int(df.at[hand_index, 'Bet'])
        if check_for_bust(hand_index = hand_index) == False:
            stand(hand_index = hand_index)
        return True

    
    def hit(hand_index : int) -> None:
        played_hand = df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if get_value(played_hand) == 21:
            return False
        played_hand.append(deck[0])
        deck.pop(0)
        df.at[hand_index, 'Hand'] = played_hand
        check_for_bust(hand_index=hand_index)
        return True


    def stand(hand_index : int) -> None:
        df.loc[hand_index, "Status"] = 'Played'
        return


    def casino_move():

        value_dealer, aces_dealer = get_value(dealers_cards)
                        
        while value_dealer < 17:
            dealers_cards.append(deck[0])
            deck.pop(0)
            value_dealer, aces_dealer = get_value(dealers_cards)
            if value_dealer > 21:
                for index, row in df.iterrows():
                    if df.at[index, 'Status'] == 'Played':
                        df.at[index, 'Outcome'] = 2*int(df.at[index, 'Bet'])
                        df.at[index, 'Status'] = 'Finished'

                            
        for index, row in df.iterrows():
            value_hand, hand_aces = get_value(df.at[index, 'Hand'])
            if df.at[index, 'Status'] == 'Played':
                if value_dealer == value_hand:
                    df.at[index, 'Outcome'] = df.at[index, 'Bet']
                    df.at[index, 'Status'] = 'Finished'
                elif value_dealer > value_hand:
                    df.at[index, 'Outcome'] = 0
                    df.at[index, 'Status'] = 'Finished'
                else:
                    df.at[index, 'Outcome'] = 2*int(df.at[index, 'Bet'])
                    df.at[index, 'Status'] = 'Finished'


    # if players_engine == 'rand':
    #     print("Game starts...")

    #checking for BlackJack
    v1, a1 = get_value(players_cards)
    if v1 == 21:
        if value_dealer != 21:
            df.at[0, 'Outcome'] = 2.5*int(df.at[0, 'Bet'])
            df.at[0, 'Status'] = 'Finished'



    if players_engine == "basic":
        while len(df[df['Status'] == 'Active']) > 0:
            f_active_hand_index = df[df['Status'] == 'Active'].index[0] #defines the index of first active hand
            f_active_hand = df.at[f_active_hand_index, 'Hand'] #defines the first active hand
            value, aces = get_value(f_active_hand)
            if len(f_active_hand) == 1:
                hit(f_active_hand_index)
                f_active_hand = df.at[f_active_hand_index, 'Hand']
                #defining spliting logic for basic strategy
            f_active_hand_index = df[df['Status'] == 'Active'].index[0] #defines the index of first active hand
            f_active_hand = df.at[f_active_hand_index, 'Hand'] #defines the first active hand
            if cards_value[f_active_hand[0]] == cards_value[f_active_hand[1]] and len(f_active_hand) == 2:    
                if cards_value[f_active_hand[0]] in [8, 11]:
                    split(f_active_hand_index)
                    continue
                elif cards_value[f_active_hand[0]] == 9:
                    if cards_value[dealers_cards[0]] not in [7, 10, 11]:
                        split(f_active_hand_index)
                        continue
                elif cards_value[f_active_hand[0]] in [2, 3, 7]:
                    if cards_value[dealers_cards[0]] < 8:
                        split(f_active_hand_index)
                        continue
                elif cards_value[f_active_hand[0]] == 6:
                    if cards_value[dealers_cards[0]] < 7:
                        split(f_active_hand_index)
                        continue
                elif cards_value[f_active_hand[0]] == 4:
                    if cards_value[dealers_cards[0]] in [5, 6]:
                        split(f_active_hand_index)
                        continue

            f_active_hand_index = df[df['Status'] == 'Active'].index[0] #defines the index of first active hand
            f_active_hand = df.at[f_active_hand_index, 'Hand'] #defines the first active hand
             
            if aces == 0:
            #this corresponds to a 'hard' hand, below the logic for this scenario
                if value > 16:
                    stand(f_active_hand_index)
                elif value in range(13, 17):
                    if cards_value[dealers_cards[0]] < 7:
                        stand(f_active_hand_index)
                    else: hit(f_active_hand_index)
                elif value == 12:
                    if cards_value[dealers_cards[0]] in [4, 5, 6]:
                        stand(f_active_hand_index)
                    else: hit(f_active_hand_index)
                elif value == 11:
                    if double(f_active_hand_index) == False:
                        hit(f_active_hand_index)
                elif value == 10:
                    if cards_value[dealers_cards[0]] < 10:
                        if double(f_active_hand_index) == False:
                            hit(f_active_hand_index)
                    else: hit(f_active_hand_index)
                elif value == 9:
                    if cards_value[dealers_cards[0]] in range(3,7):
                        if double(f_active_hand_index) == False:
                            hit(f_active_hand_index)
                    else: hit(f_active_hand_index)
                else: hit(f_active_hand_index)
                    

            elif aces > 0:
            #this correcponds to a 'soft' hand, below the logic for this scenario 
                if value > 19:
                    stand(f_active_hand_index)
                elif value == 19:
                    if cards_value[dealers_cards[0]] == 6:
                        if double(f_active_hand_index) == False:
                            stand(f_active_hand_index)
                    else: stand(f_active_hand_index)
                elif value == 18:
                    if cards_value[dealers_cards[0]] in range(2,7):
                        if double(f_active_hand_index) == False:
                            stand(f_active_hand_index)
                    elif cards_value[dealers_cards[0]] in [7, 8]:
                        stand(f_active_hand_index)
                    else: hit(f_active_hand_index)
                elif value in range(13, 18) and cards_value[dealers_cards[0]] in [5, 6]:
                    if double(f_active_hand_index) == False:
                        hit(f_active_hand_index)
                elif value in range(15,18) and cards_value[dealers_cards[0]] == 4:
                    if double(f_active_hand_index) == False:
                        hit(f_active_hand_index)
                elif value == 17 and cards_value[dealers_cards[0]] == 3:
                    if double(f_active_hand_index) == False:
                        hit(f_active_hand_index)
                else: hit(f_active_hand_index)
    
        casino_move()
        return df, dealers_cards
    
    else:
            # DEFINING THE BASIC STRATEGY DEVIATIONS
            # Defining the players engine as a numpy array
            # The columns represent dealer's up card: 2, 3, 4, 5, 6, 7, 8, 9, 10, A
            # H = Hit, S = Stand, D = Double, 
            # for splits Y = Yes, N = No
        
            # all arrays are 3 dimensional, with exactly 3 layers
                # main layer (0) defines the true count value to enable an exception
                # layer (1) defines the standard play
                # layer (2) is for the exceptions, where the player should play differently based on the true count


        hard_totals = np.array([
            # 8 or less
            [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [5, 'H', 'D'], [3, 'H', 'D'], [1, 'H', 'D'], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan],[np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 9
            [[1, 'H', 'D'], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [3, 'H', 'D'], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 10
            [[np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 11
            [[np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan]],
            # 12
            [[3, 'H', 'S'], [2, 'H', 'S'], [0, 'H', 'S'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 13
            [[-1, 'H', 'S'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 14
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # 15
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [4, 'H', 'S']],
            # 16
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [4, 'H', 'S'], [0, 'H', 'S'], [np.nan,'H',np.nan]],
            # 17+
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]]
        ], dtype=object)

        soft_totals = np.array([
            # A9
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]], 
            # A8
            [[np.nan,'S',np.nan], [np.nan,'S',np.nan], [3, 'S', 'D'], [1, 'S', 'D'], [1, 'S', 'D'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'S',np.nan]], 
            # A7
            [[0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [0, 'S', 'D'], [np.nan,'S',np.nan], [np.nan,'S',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # A6
            [[1, 'H', 'D'], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # A5
            [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # A4
            [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # A3
            [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]],
            # A2
            [[np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'D',np.nan], [np.nan,'D',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan], [np.nan,'H',np.nan]]
        ], dtype=object)


        pair_splitting = np.array([
            # AA
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan]],
            # TT
            [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [6, 'N', 'Y'], [5, 'N', 'Y'], [4, 'N', 'Y'], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 99
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]], 
            # 88
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan]],
            # 77
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 66
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 55
            [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 44
            [[np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [[np.nan,'Y',np.nan]], [[np.nan,'Y',np.nan]], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 33
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]],
            # 22
            [[np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'Y',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan], [np.nan,'N',np.nan]]
        ], dtype=object)

        def compare(x, y):
            return (y < 0 and x < y) or (y > 0 and x > y)

        while len(df[df['Status'] == 'Active']) > 0:
            f_active_hand_index = df[df['Status'] == 'Active'].index[0] #defines the index of first active hand
            f_active_hand = df.at[f_active_hand_index, 'Hand'] #defines the first active hand
            value, aces = get_value(f_active_hand)

            if cards_value[dealers_cards[0]] == 11:
                col = 9
            elif cards_value[dealers_cards[0]] == 10:
                col = 8
            else:
                col = cards_value[dealers_cards[0]] - 2

            #checking for splits
            if cards_value[f_active_hand[0]] == cards_value[f_active_hand[1]] and len(f_active_hand) == 2:
                if cards_value[f_active_hand[0]] == 11:
                    row = 0
                elif cards_value[f_active_hand[0]] == 10:
                    row = 1
                else:
                    row = 11 - cards_value[f_active_hand[0]]

                
                if np.isnan(pair_splitting[row, col, 0]):
                    if pair_splitting[row, col, 1] == 'Y':
                        split(f_active_hand_index)
                        continue
                else:
                    if true_count > pair_splitting[row, col, 0]:
                        if pair_splitting[row, col, 2] == 'Y':
                            split(f_active_hand_index)
                            continue
                        else: pass
                    else:
                        if pair_splitting[row, col, 1] == 'Y':
                            split(f_active_hand_index)
                            continue
                        else: pass
            
            #checking for hard totals
            if aces == 0:
                if value > 8 and value < 17:
                    row = value - 8
                elif value <= 8:
                    row = 0
                else:
                    row = 9

                if np.isnan(hard_totals[row, col, 0]):
                    if hard_totals[row, col, 1] == 'H':
                        hit(f_active_hand_index)
                        continue
                    elif hard_totals[row, col, 1] == 'S':
                        stand(f_active_hand_index)
                        continue
                    else:
                        double(f_active_hand_index)
                        continue
                else:
                    if compare(true_count, hard_totals[row, col, 0]):
                        if hard_totals[row, col, 2] == 'H':
                            hit(f_active_hand_index)
                            continue
                        elif hard_totals[row, col, 2] == 'S':
                            stand(f_active_hand_index)
                            continue
                        else:
                            double(f_active_hand_index)
                            continue
                    else:
                        if hard_totals[row, col, 1] == 'H':
                            hit(f_active_hand_index)
                            continue
                        elif hard_totals[row, col, 1] == 'S':
                            stand(f_active_hand_index)
                            continue
                        else:
                            double(f_active_hand_index)
                            continue
                        
            #checking for soft totals
            else:
                row = 20 - value
                if np.isnan(soft_totals[row, col, 0]):
                    if soft_totals[row, col, 1] == 'H':
                        hit(f_active_hand_index)
                        continue
                    elif soft_totals[row, col, 1] == 'S':
                        stand(f_active_hand_index)
                        continue
                    else:
                        double(f_active_hand_index)
                        continue
                else:
                    if compare(true_count, soft_totals[row, col, 0]):
                        if soft_totals[row, col, 2] == 'H':
                            hit(f_active_hand_index)
                            continue
                        elif soft_totals[row, col, 2] == 'S':
                            stand(f_active_hand_index)
                            continue
                        else:
                            double(f_active_hand_index)
                            continue
                    else:
                        if soft_totals[row, col, 1] == 'H':
                            hit(f_active_hand_index)
                            continue
                        elif soft_totals[row, col, 1] == 'S':
                            stand(f_active_hand_index)
                            continue
                        else:
                            double(f_active_hand_index)
                            continue


                



def BJ_simulator(iterations: int, shoe_size: int, bet_size: int, games_per_deck=5):
    
    data = pd.DataFrame({'Starting cards': [], 'Dealers card': [], 'Hands amount': [], '$result': [], 'Starting running count': [],'Cards left at start': [], 'Cards Left after the game':[]})
    # $result = game winnings - bets(game cost)
    
    for i in range(iterations):
        deck = shuffle(decks=shoe_size)
        for n in range(games_per_deck*shoe_size):
            true_count = 0
            for card in list(deck):
                if cards_value[card] in [10, 11]:
                    true_count += 1
                elif cards_value[card] in range(2, 7):
                    true_count -= 1
            try:
                cards_at_start = len(deck)
                df, dealer_cards = game_of_blackjack(bet = bet_size, players_engine = 'basic')
                cards_left = len(deck)
                result = df['Outcome'].sum() - df['Bet'].sum()
                starting_cards = list(df.loc[0,'Hand'])[:2]
                w = pd.DataFrame({'Starting cards': [starting_cards], 'Dealers card': [dealer_cards[0]],'Hands amount':[len(df)], '$result': [result], 'Starting running count': [true_count], 'Cards left at start': [cards_at_start], 'Cards Left after the game':[cards_left]})
                data = pd.concat([data, w], ignore_index=True, axis=0)
            except IndexError as e:
                pass
    return data



# FIX area
shuffle(1)
deck[0] = 'Club A'
deck[1] = 'Diamond Q'
deck[2] = 'Spade A'
deck[3] = 'Heart J'


df, dealers_cards = game_of_blackjack(bet=100)
print(df)
print(dealers_cards)



# data=BJ_simulator(iterations=1,shoe_size=1,bet_size=100, games_per_deck=5)
# print(data['$result'].sum())
# data