from dataclasses import dataclass
from master_data import CARDS_VALUE


@dataclass
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


        #DataFrame for trackability of hands and bets, implemented as distionary of lists
        self.df = {'Hand': [], 'Bet': [], 'Status': [], 'Outcome': []}
        #Hand is a list of stings containing hands cards
        #Bet is an integer of the bet size for given hand 
        #Status is a sting to indicate if hand is active, played or finished
        #Outcome is the financial result
        # Add a row to the dictionary
        self.df['Hand'].append(self.players_cards)  
        self.df['Bet'].append(self.bet)            
        self.df['Status'].append('Active')         
        self.df['Outcome'].append(None)


    def play_hand(self) -> dict:
        # Checking for dealer's BlackJack
        if CARDS_VALUE[self.dealers_cards[0]] in [10, 11]:
            value_dealer, aces_dealer = self.get_value(self.dealers_cards)
            if value_dealer == 21:
                for i in range(len(self.df['Hand'])):
                    hand_value, hand_aces = self.get_value(self.df['Hand'][i])
                    if hand_value == 21:
                        self.df['Outcome'][i] = self.df['Bet'][i]  # Player wins with Blackjack
                        self.df['Status'][i] = 'Finished'
                    else:
                        self.df['Outcome'][i] = 0  # Player loses
                        self.df['Status'][i] = 'Finished'

        # Checking for player's BlackJack
        v1, a1 = self.get_value(self.players_cards)
        value_dealer, aces_dealer = self.get_value(self.dealers_cards)
        if v1 == 21:
            if value_dealer != 21:
                self.df['Outcome'][0] = 2.5 * self.df['Bet'][0]  # Payout for Blackjack
                self.df['Status'][0] = 'Finished'

        if self.players_engine == 'basic':
            while 'Active' in self.df['Status']:
                # Defining the first active hand
                f_active_hand_index = self.df['Status'].index('Active')
                f_active_hand = self.df['Hand'][f_active_hand_index]

                value, aces = self.get_value(f_active_hand)

                if len(f_active_hand) == 1:
                    self.hit(f_active_hand_index)
                    continue

                # Basic strategy logic for splitting
                if len(f_active_hand) == 2 and CARDS_VALUE[f_active_hand[0]] == CARDS_VALUE[f_active_hand[1]]:
                    card_value = CARDS_VALUE[f_active_hand[0]]
                    dealer_card_value = CARDS_VALUE[self.dealers_cards[0]]

                    if card_value in [8, 11]:
                        self.split(f_active_hand_index)
                        continue
                    elif card_value == 9 and dealer_card_value not in [7, 10, 11]:
                        self.split(f_active_hand_index)
                        continue
                    elif card_value in [2, 3, 7] and dealer_card_value < 8:
                        self.split(f_active_hand_index)
                        continue
                    elif card_value == 6 and dealer_card_value < 7:
                        self.split(f_active_hand_index)
                        continue
                    elif card_value == 4 and dealer_card_value in [5, 6]:
                        self.split(f_active_hand_index)
                        continue

                # Logic for hard hands
                if aces == 0:
                    if value > 16:
                        self.stand(f_active_hand_index)
                    elif value in range(13, 17):
                        if CARDS_VALUE[self.dealers_cards[0]] < 7:
                            self.stand(f_active_hand_index)
                        else:
                            self.hit(f_active_hand_index)
                    elif value == 12:
                        if CARDS_VALUE[self.dealers_cards[0]] in [4, 5, 6]:
                            self.stand(f_active_hand_index)
                        else:
                            self.hit(f_active_hand_index)
                    elif value == 11:
                        if not self.double(f_active_hand_index):
                            self.hit(f_active_hand_index)
                    elif value == 10:
                        if CARDS_VALUE[self.dealers_cards[0]] < 10:
                            if not self.double(f_active_hand_index):
                                self.hit(f_active_hand_index)
                        else:
                            self.hit(f_active_hand_index)
                    elif value == 9:
                        if CARDS_VALUE[self.dealers_cards[0]] in range(3, 7):
                            if not self.double(f_active_hand_index):
                                self.hit(f_active_hand_index)
                        else:
                            self.hit(f_active_hand_index)
                    else:
                        self.hit(f_active_hand_index)

                # Logic for soft hands
                elif aces > 0:
                    if value > 19:
                        self.stand(f_active_hand_index)
                    elif value == 19:
                        if CARDS_VALUE[self.dealers_cards[0]] == 6:
                            if not self.double(f_active_hand_index):
                                self.stand(f_active_hand_index)
                        else:
                            self.stand(f_active_hand_index)
                    elif value == 18:
                        if CARDS_VALUE[self.dealers_cards[0]] in range(2, 7):
                            if not self.double(f_active_hand_index):
                                self.stand(f_active_hand_index)
                        elif CARDS_VALUE[self.dealers_cards[0]] in [7, 8]:
                            self.stand(f_active_hand_index)
                        else:
                            self.hit(f_active_hand_index)
                    elif value in range(13, 18) and CARDS_VALUE[self.dealers_cards[0]] in [5, 6]:
                        if not self.double(f_active_hand_index):
                            self.hit(f_active_hand_index)
                    elif value in range(15, 18) and CARDS_VALUE[self.dealers_cards[0]] == 4:
                        if not self.double(f_active_hand_index):
                            self.hit(f_active_hand_index)
                    elif value == 17 and CARDS_VALUE[self.dealers_cards[0]] == 3:
                        if not self.double(f_active_hand_index):
                            self.hit(f_active_hand_index)
                    else:
                        self.hit(f_active_hand_index)

            self.casino_move()
            return self.df, self.dealers_cards

        else:
            while 'Active' in self.df['Status']:
                f_active_hand_index = self.df['Status'].index('Active')
                f_active_hand = self.df['Hand'][f_active_hand_index]
                value, aces = self.get_value(f_active_hand)

                if len(f_active_hand) == 1:
                    self.hit(f_active_hand_index)
                    continue

                # Additional logic for advanced strategies would go here

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
        played_hand = self.df['Hand'][hand_index]
        value_hand, aces_hand = self.get_value(played_hand)
        if value_hand > 21:
            self.df['Status'][hand_index] = 'Finished'
            self.df['Outcome'][hand_index] = 0
            return True
        return False


    def split(self, hand_index: int) -> None:
        played_hand = self.df['Hand'][hand_index]
        if len(played_hand) != 2 or CARDS_VALUE[played_hand[0]] != CARDS_VALUE[played_hand[1]]:
            return False

        hand2 = [played_hand.pop(1)]
        played_hand.append(self.deck.pop(0))
        hand2.append(self.deck.pop(0))

        self.df['Hand'][hand_index] = played_hand
        self.df['Hand'].append(hand2)
        self.df['Bet'].append(self.df['Bet'][hand_index])
        self.df['Status'].append('Active')
        self.df['Outcome'].append(None)

        return


    def double(self, hand_index: int) -> bool:
        played_hand = self.df['Hand'][hand_index]
        if len(played_hand) != 2 or self.get_value(played_hand)[0] == 21:
            return False

        played_hand.append(self.deck.pop(0))
        self.df['Hand'][hand_index] = played_hand
        self.df['Bet'][hand_index] *= 2

        if not self.check_for_bust(hand_index):
            self.stand(hand_index)

        return True


    def hit(self, hand_index: int) -> bool:
        played_hand = self.df['Hand'][hand_index]
        if self.get_value(played_hand)[0] == 21:
            return False

        played_hand.append(self.deck.pop(0))
        self.df['Hand'][hand_index] = played_hand
        self.check_for_bust(hand_index)

        return True


    def stand(self, hand_index: int) -> None:
        self.df['Status'][hand_index] = 'Played'
        return


    def casino_move(self):
        value_dealer, aces_dealer = self.get_value(self.dealers_cards)

        while value_dealer < 17:
            self.dealers_cards.append(self.deck.pop(0))
            value_dealer, aces_dealer = self.get_value(self.dealers_cards)

            if value_dealer > 21:
                for i, status in enumerate(self.df['Status']):
                    if status == 'Played':
                        self.df['Outcome'][i] = 2 * self.df['Bet'][i]
                        self.df['Status'][i] = 'Finished'

        for i, status in enumerate(self.df['Status']):
            if status == 'Played':
                value_hand, hand_aces = self.get_value(self.df['Hand'][i])
                if value_dealer == value_hand:
                    self.df['Outcome'][i] = self.df['Bet'][i]
                    self.df['Status'][i] = 'Finished'
                elif value_dealer > value_hand:
                    self.df['Outcome'][i] = 0
                    self.df['Status'][i] = 'Finished'
                else:
                    self.df['Outcome'][i] = 2 * self.df['Bet'][i]
                    self.df['Status'][i] = 'Finished'

