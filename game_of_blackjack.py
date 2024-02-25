import pandas as pd
from dataclasses import dataclass
import numpy as np
from master_data import CARDS_VALUE, HARD_TOTALS, SOFT_TOTALS, PAIR_SPLITTING


# @dataclass
class game_of_blackjack:
    """plays single game of blackjack


    Parameters
    ----------
    players_engine: str
        type of engine to be used

    Returns
    -------
    pd.DataFrame
        DataFrame with the results of the game
    """


    def __init__(self, deck, bet : int = 1, players_engine : str = 'basic', true_count : float = 0):
        self.deck = deck
        self.array_pairs=None
        self.array_soft=None
        self.array_hard=None
        self.bet = bet
        self.players_engine = players_engine
        self.true_count = true_count

        #drawing cards
        self.players_cards = [deck[0]]
        self.deck.pop(0)
        self.players_cards += [deck[0]]
        self.deck.pop(0)
        self.dealers_cards = [deck[0]]
        self.deck.pop(0)
        self.dealers_cards += [deck[0]]
        self.deck.pop(0)


        #DataFrame for trackability of hands and bets
        self.df = pd.DataFrame(columns=['Hand', 'Bet', 'Status', 'Outcome'])
        #Hand is a list of stings containing hands cards
        #Bet is an integer of the bet size for given hand 
        #Status is a sting to indicate if hand is active, played or finished
        #Outcome is the financial result
        self.df.loc[0,:] = [self.players_cards, self.bet, 'Active', None]

    def play_hand(self)-> pd.DataFrame:

        #checking for dealers BlackJack
        if CARDS_VALUE[self.dealers_cards[0]] in [10, 11]:
            value_dealer, aces_dealer = self.get_value(self.dealers_cards)
            if value_dealer == 21:
                for index, row in self.df.iterrows():
                    hand_value, hand_aces = self.get_value(row['Hand'])
                    if hand_value ==21:
                        self.df.at[index, 'Outcome'] = self.df.at[index, "Bet"]
                        self.df.at[index, 'Status'] = 'Finished'
                    else:
                        self.df.at[index, 'Outcome'] = 0
                        self.df.at[index, 'Status'] = 'Finished'
        
        #checking for BlackJack
        v1, a1 = self.get_value(self.players_cards)
        value_dealer, aces_dealer = self.get_value(self.dealers_cards)
        if v1 == 21:
            if value_dealer != 21:
                self.df.at[0, 'Outcome'] = 2.5*int(self.df.at[0, 'Bet'])
                self.df.at[0, 'Status'] = 'Finished'



        if self.players_engine == 'basic':
            while len(self.df[self.df['Status'] == 'Active']) > 0:
                f_active_hand_index = self.df[self.df['Status'] == 'Active'].index[0] #defines the index of first active hand
                f_active_hand = self.df.at[f_active_hand_index, 'Hand'] #defines the first active hand
                value, aces = self.get_value(f_active_hand)
                if len(f_active_hand) == 1:
                    self.hit(f_active_hand_index)
                    continue
                    #defining spliting logic for basic strategy
                if CARDS_VALUE[f_active_hand[0]] == CARDS_VALUE[f_active_hand[1]] and len(f_active_hand) == 2:    
                    if CARDS_VALUE[f_active_hand[0]] in [8, 11]:
                        self.split(f_active_hand_index)
                        continue
                    elif CARDS_VALUE[f_active_hand[0]] == 9:
                        if CARDS_VALUE[self.dealers_cards[0]] not in [7, 10, 11]:
                            self.split(f_active_hand_index)
                            continue
                    elif CARDS_VALUE[f_active_hand[0]] in [2, 3, 7]:
                        if CARDS_VALUE[self.dealers_cards[0]] < 8:
                            self.split(f_active_hand_index)
                            continue
                    elif CARDS_VALUE[f_active_hand[0]] == 6:
                        if CARDS_VALUE[self.dealers_cards[0]] < 7:
                            self.split(f_active_hand_index)
                            continue
                    elif CARDS_VALUE[f_active_hand[0]] == 4:
                        if CARDS_VALUE[self.dealers_cards[0]] in [5, 6]:
                            self.split(f_active_hand_index)
                            continue

                f_active_hand_index = self.df[self.df['Status'] == 'Active'].index[0] #defines the index of first active hand
                f_active_hand = self.df.at[f_active_hand_index, 'Hand'] #defines the first active hand
                
                if aces == 0:
                #this corresponds to a 'hard' hand, below the logic for this scenario
                    if value > 16:
                        self.stand(f_active_hand_index)
                    elif value in range(13, 17):
                        if CARDS_VALUE[self.dealers_cards[0]] < 7:
                            self.stand(f_active_hand_index)
                        else: self.hit(f_active_hand_index)
                    elif value == 12:
                        if CARDS_VALUE[self.dealers_cards[0]] in [4, 5, 6]:
                            self.stand(f_active_hand_index)
                        else: self.hit(f_active_hand_index)
                    elif value == 11:
                        if self.double(f_active_hand_index) == False:
                            self.hit(f_active_hand_index)
                    elif value == 10:
                        if CARDS_VALUE[self.dealers_cards[0]] < 10:
                            if self.double(f_active_hand_index) == False:
                                self.hit(f_active_hand_index)
                        else: self.hit(f_active_hand_index)
                    elif value == 9:
                        if CARDS_VALUE[self.dealers_cards[0]] in range(3,7):
                            if self.double(f_active_hand_index) == False:
                                self.hit(f_active_hand_index)
                        else: self.hit(f_active_hand_index)
                    else: self.hit(f_active_hand_index)
                        

                elif aces > 0:
                #this correcponds to a 'soft' hand, below the logic for this scenario 
                    if value > 19:
                        self.stand(f_active_hand_index)
                    elif value == 19:
                        if CARDS_VALUE[self.dealers_cards[0]] == 6:
                            if self.double(f_active_hand_index) == False:
                                self.stand(f_active_hand_index)
                        else: self.stand(f_active_hand_index)
                    elif value == 18:
                        if CARDS_VALUE[self.dealers_cards[0]] in range(2,7):
                            if self.double(f_active_hand_index) == False:
                                self.stand(f_active_hand_index)
                        elif CARDS_VALUE[self.dealers_cards[0]] in [7, 8]:
                            self.stand(f_active_hand_index)
                        else: self.hit(f_active_hand_index)
                    elif value in range(13, 18) and CARDS_VALUE[self.dealers_cards[0]] in [5, 6]:
                        if self.double(f_active_hand_index) == False:
                            self.hit(f_active_hand_index)
                    elif value in range(15,18) and CARDS_VALUE[self.dealers_cards[0]] == 4:
                        if self.double(f_active_hand_index) == False:
                            self.hit(f_active_hand_index)
                    elif value == 17 and CARDS_VALUE[self.dealers_cards[0]] == 3:
                        if self.double(f_active_hand_index) == False:
                            self.hit(f_active_hand_index)
                    else: self.hit(f_active_hand_index)
        
            self.casino_move()
            return self.df, self.dealers_cards
        
        else:


            while len(self.df[self.df['Status'] == 'Active']) > 0:
                f_active_hand_index = self.df[self.df['Status'] == 'Active'].index[0] #defines the index of first active hand
                f_active_hand = self.df.at[f_active_hand_index, 'Hand'] #defines the first active hand
                value, aces = self.get_value(f_active_hand)
                if len(f_active_hand) == 1:
                    self.hit(f_active_hand_index)
                    continue

                if CARDS_VALUE[self.dealers_cards[0]] == 11:
                    col = 9
                elif CARDS_VALUE[self.dealers_cards[0]] == 10:
                    col = 8
                else:
                    col = CARDS_VALUE[self.dealers_cards[0]] - 2

                #checking for splits
                if CARDS_VALUE[f_active_hand[0]] == CARDS_VALUE[f_active_hand[1]] and len(f_active_hand) == 2:
                    if CARDS_VALUE[f_active_hand[0]] == 11:
                        row = 0
                    elif CARDS_VALUE[f_active_hand[0]] == 10:
                        row = 1
                    else:
                        row = 11 - CARDS_VALUE[f_active_hand[0]]

                    
                    if np.isnan(PAIR_SPLITTING[row, col, 0]):
                        if PAIR_SPLITTING[row, col, 1] == 'Y':
                            self.split(f_active_hand_index)
                            continue

                    if self.true_count > PAIR_SPLITTING[row, col, 0]:
                        if PAIR_SPLITTING[row, col, 2] == 'Y':
                            self.split(f_active_hand_index)
                            continue
                            
                        if PAIR_SPLITTING[row, col, 1] == 'Y':
                            self.split(f_active_hand_index)
                            continue
            
                #checking for hard totals
                if aces == 0:
                    if value > 8 and value < 17:
                        row = value - 8
                    elif value <= 8:
                        row = 0
                    else:
                        row = 9

                    if np.isnan(HARD_TOTALS[row, col, 0]):
                        if HARD_TOTALS[row, col, 1] == 'H':
                            self.hit(f_active_hand_index)
                            continue
                        
                        if HARD_TOTALS[row, col, 1] == 'S':
                            self.stand(f_active_hand_index)
                            continue
                        
                        if self.double(f_active_hand_index):
                            pass
                        else:
                            self.hit(f_active_hand_index)
                        continue
                    
                    if self.compare(self.true_count, HARD_TOTALS[row, col, 0]):
                        if HARD_TOTALS[row, col, 2] == 'H':
                            self.hit(f_active_hand_index)
                            continue
                        
                        if HARD_TOTALS[row, col, 2] == 'S':
                            self.stand(f_active_hand_index)
                            continue
                        
                        if self.double(f_active_hand_index):
                            pass
                        else:
                            self.hit(f_active_hand_index)
                        continue
                   
                    if HARD_TOTALS[row, col, 1] == 'H':
                        self.hit(f_active_hand_index)
                        continue
                    
                    if HARD_TOTALS[row, col, 1] == 'S':
                        self.stand(f_active_hand_index)
                        continue
                    
                    if self.double(f_active_hand_index):
                        pass
                    else:
                        self.hit(f_active_hand_index)
                    continue
                            
                #soft totals
                row = 20 - value
                if np.isnan(SOFT_TOTALS[row, col, 0]):
                    if SOFT_TOTALS[row, col, 1] == 'H':
                        self.hit(f_active_hand_index)
                        continue
                    if SOFT_TOTALS[row, col, 1] == 'S':
                        self.stand(f_active_hand_index)
                        continue

                    if self.double(f_active_hand_index):
                        pass
                    else:
                        self.hit(f_active_hand_index)
                    continue

                if self.compare(self.true_count, SOFT_TOTALS[row, col, 0]):
                    if SOFT_TOTALS[row, col, 2] == 'H':
                        self.hit(f_active_hand_index)
                        continue
                    if SOFT_TOTALS[row, col, 2] == 'S':
                        self.stand(f_active_hand_index)
                        continue
                    if self.double(f_active_hand_index):
                        pass
                    else:
                        self.hit(f_active_hand_index)
                    continue
                if SOFT_TOTALS[row, col, 1] == 'H':
                    self.hit(f_active_hand_index)
                    continue
                if SOFT_TOTALS[row, col, 1] == 'S':
                    self.stand(f_active_hand_index)
                    continue
                if self.double(f_active_hand_index):
                    pass
                else:
                    self.hit(f_active_hand_index)
                continue

            
            self.casino_move()
            return self.df, self.dealers_cards

    def compare(self, x, y):
                return (y < 0 and x < y) or (y > 0 and x > y)

    def get_value(self, played_hand: list['str']):
        #hand should be a list argument
        
        #calculate value and adjust for aces
        value = 0
        for card in list(played_hand):
            value += CARDS_VALUE[card]
            
        aces = 0
        for card in list(played_hand): 
            if card[-1] == "A":
                aces += 1

        while value > 21 and aces >0:
            aces -= 1
            value -= 10
        
        else: return value, aces
          
    def check_for_bust(self, hand_index: int) -> bool:
        played_hand = self.df.at[hand_index, 'Hand']
        value_hand, aces_hand = self.get_value(played_hand)
        if value_hand > 21:
            self.df.at[hand_index, 'Status'] = 'Finished'
            self.df.at[hand_index, 'Outcome'] = 0
            return True
        else:
            return False

    def split(self, hand_index: int) -> None:
        played_hand = self.df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if len(played_hand) != 2 or CARDS_VALUE[played_hand[0]] != CARDS_VALUE[played_hand[1]]:
            return False
        hand2 = [played_hand[1]]
        list(hand2)
        played_hand.pop(1)
        played_hand.append(self.deck[0])
        self.deck.pop(0)
        self.df.at[hand_index, 'Hand'] = played_hand
        hand2.append(self.deck[0])
        self.deck.pop(0)
        self.df.loc[len(self.df)] = [hand2, self.df.at[hand_index, 'Bet'], 'Active', None]
        return

    def double(self, hand_index : int) -> None:
        played_hand = self.df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if len(played_hand) != 2 or self.get_value(played_hand) == 21:
            return False
        played_hand.append(self.deck[0])
        self.deck.pop(0)
        self.df.at[hand_index, 'Hand'] = played_hand
        self.df.at[hand_index, 'Bet'] = 2*int(self.df.at[hand_index, 'Bet'])
        if self.check_for_bust(hand_index = hand_index) == False:
            self.stand(hand_index = hand_index)
        return True

    def hit(self, hand_index : int) -> None:
        played_hand = self.df.at[hand_index, 'Hand']
        played_hand = list(played_hand)
        if self.get_value(played_hand) == 21:
            return False
        played_hand.append(self.deck[0])
        self.deck.pop(0)
        self.df.at[hand_index, 'Hand'] = played_hand
        self.check_for_bust(hand_index=hand_index)
        return True

    def stand(self, hand_index : int) -> None:
        self.df.loc[hand_index, "Status"] = 'Played'
        return

    def casino_move(self):

        value_dealer, aces_dealer = self.get_value(self.dealers_cards)
                        
        while value_dealer < 17:
            self.dealers_cards.append(self.deck[0])
            self.deck.pop(0)
            value_dealer, aces_dealer = self.get_value(self.dealers_cards)
            if value_dealer > 21:
                for index, row in self.df.iterrows():
                    if self.df.at[index, 'Status'] == 'Played':
                        self.df.at[index, 'Outcome'] = 2*int(self.df.at[index, 'Bet'])
                        self.df.at[index, 'Status'] = 'Finished'

                            
        for index, row in self.df.iterrows():
            value_hand, hand_aces = self.get_value(self.df.at[index, 'Hand'])
            if self.df.at[index, 'Status'] == 'Played':
                if value_dealer == value_hand:
                    self.df.at[index, 'Outcome'] = self.df.at[index, 'Bet']
                    self.df.at[index, 'Status'] = 'Finished'
                elif value_dealer > value_hand:
                    self.df.at[index, 'Outcome'] = 0
                    self.df.at[index, 'Status'] = 'Finished'
                else:
                    self.df.at[index, 'Outcome'] = 2*int(self.df.at[index, 'Bet'])
                    self.df.at[index, 'Status'] = 'Finished'