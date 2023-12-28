import pandas as pd
import numpy as np
import random

possible_cards = ("Spade 2",
                  "Spade 3",
                  "Spade 4",
                  "Spade 5",
                  "Spade 6",
                  "Spade 7",
                  "Spade 8",
                  "Spade 9",
                  "Spade 10",
                  "Spade J",
                  "Spade Q",
                  "Spade K",
                  "Spade A",
                  "Club 2",
                  "Club 3",
                  "Club 4",
                  "Club 5",
                  "Club 6",
                  "Club 7",
                  "Club 8",
                  "Club 9",
                  "Club 10",
                  "Club J",
                  "Club Q",
                  "Club K",
                  "Club A",
                  "Diamond 2",
                  "Diamond 3",
                  "Diamond 4",
                  "Diamond 5",
                  "Diamond 6",
                  "Diamond 7",
                  "Diamond 8",
                  "Diamond 9",
                  "Diamond 10",
                  "Diamond J",
                  "Diamond Q",
                  "Diamond K",
                  "Diamond A",
                  "Heart 2",
                  "Heart 3",
                  "Heart 4",
                  "Heart 5",
                  "Heart 6",
                  "Heart 7",
                  "Heart 8",
                  "Heart 9",
                  "Heart 10",
                  "Heart J",
                  "Heart Q",
                  "Heart K",
                  "Heart A")

starting_deck = list(possible_cards)

def shuffle(decks):
    #building a deck
    global deck
    deck = random.sample(starting_deck, len(starting_deck))
    for i in range(decks - 1):
        deck += random.sample(starting_deck, len(starting_deck))
    return deck


cards_value = {
    'Spade 2' :2,
    'Spade 3' :3,
    'Spade 4' :4,
    'Spade 5' :5,
    'Spade 6' :6,
    'Spade 7' :7,
    'Spade 8' :8,
    'Spade 9' :9,
    'Spade 10' : 10,
    'Spade J' : 10,
    'Spade Q' :10,
    'Spade K' :10,
    'Spade A' :11,
    'Club 2' :2,
    'Club 3' :3,
    'Club 4' :4,
    'Club 5' :5,
    'Club 6' :6,
    'Club 7' :7,
    'Club 8' :8,
    'Club 9' :9,
    'Club 10' :10,
    'Club J' : 10,
    'Club Q' : 10,
    'Club K' : 10,
    'Club A' : 11,
    'Diamond 2' :2,
    'Diamond 3' :3,
    'Diamond 4' :4,
    'Diamond 5' :5,
    'Diamond 6' :6,
    'Diamond 7' :7,
    'Diamond 8' :8,
    'Diamond 9' :9,
    'Diamond 10' :10,
    'Diamond J' : 10,
    'Diamond Q' : 10,
    'Diamond K' : 10,
    'Diamond A' : 11,
    'Heart 2' :2,
    'Heart 3' :3,
    'Heart 4' :4,
    'Heart 5' :5,
    'Heart 6' :6,
    'Heart 7' :7,
    'Heart 8' :8,
    'Heart 9' :9,
    'Heart 10' :10,
    'Heart J' : 10,
    'Heart Q' : 10,
    'Heart K' : 10,
    'Heart A' : 11}



#here I am just assuming the hand played is the first from active hands

#TODO: create enum for engine type ["rand", ...]
def game_of_blackjack0(players_engine : str = "rand") -> int:  
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
    active_hands = [players_cards] #list of active players' hands
    played_hands = [] #list of inactive players' hands
    lost_hands = [] #list of hands that lost
    won_hands = [] #list of hands that won
    pushed_hands = []
    def get_value(played_hand=active_hands[0]):
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
        return value

               
    def check_for_bust(played_hand : list[str] = active_hands[0]) -> bool:
        value_hand = get_value(played_hand)
        if value_hand > 21:
            print("Casino wins")
            lost_hands.append(played_hand)
            active_hands.remove(played_hand)
            return False
        else:
            #results = df.append(new_row, ignore_index=True)
            return True


    def split(played_hand : list[str] = active_hands[0]) -> None:
        if len(played_hand) != 2 or played_hand[0] != played_hand[1]:
            return
        hand2 = [played_hand[1]]
        played_hand.pop(1)
        played_hand.append(deck[0])
        deck.pop(0)
        active_hands.append(hand2)
        return


    
    def double(played_hand : list[str] = active_hands[0]) -> None:
        if len(played_hand) != 2:
            return
        played_hand.append(deck[0])
        deck.pop(0)
        check_for_bust(played_hand)
        stand(played_hand)
        return

    
    def hit(played_hand : list[str] = active_hands[0]) -> None:
        played_hand.append(deck[0])
        deck.pop(0)
        check_for_bust(played_hand)
        return

    def stand(played_hand : list[str] = active_hands[0]) -> None:
        played_hands.append(played_hand)
        active_hands.remove(played_hand)
        return

    def casino_move():
        #implement an after split scenario for multiple hands
        dealers_cards.append(deck[0])
        deck.pop(0)
        value_dealer = get_value(dealers_cards)
    
        if value_dealer == 21:
            #a scenario of dealers instatnt blackjack is dealt here
            print("Casino wins")
            for hand in played_hands:
                lost_hands.append(hand)
                played_hands.remove(hand)
                        
        while value_dealer < 17:
            dealers_cards.append(deck[0])
            deck.pop(0)
            value_dealer = get_value(dealers_cards)
            if value_dealer > 21:
                for hand in list(played_hands):
                    print("Player wins")
                    won_hands.append(hand)
                    played_hands.remove(hand)
                            
        for hand in list(played_hands):
            if value_dealer == get_value(hand):
                print("Push")
                pushed_hands.append(hand)
                played_hands.remove(hand)
            elif value_dealer > get_value(hand):
                print("Casino wins")
                lost_hands.append(hand)
                played_hands.remove(hand)
            else:
                print("Player wins")
                won_hands.append(hand)
                played_hands.remove(hand)
        return



    print("Game starts...")

    #checking for BlackJack
    if get_value(players_cards) == 21:
        print("Player wins")
        won_hands.append(players_cards)
        active_hands.remove(players_cards)
        #results = df.append(new_row, ignore_index=True)
    print(players_cards)
    print(dealers_cards)
        
        
        
    #players decision engine
    #in future there should be rand (random choices), basic (BJ basic strategy - proven best possible move)
 
    #for now implemented a random engine
    moves = ['stand', 'hit', 'double', 'split']
    def print_status():
        print("Active hands:  ")
        print(active_hands)
        
    while True:
        move = random.choice(moves)
        if move == "stand":
            print("player standing")
            print_status()
            stand()
        if len(active_hands)==0:
            break            
        if move == "hit":
            print("player hitting")
            print_status()
            hit()
        if len(active_hands)==0:
            break
        if move == "double":
            print("player doubling")
            print_status()
            double()
        if len(active_hands)==0:
            break
        if move == "split":
            print("split")
            print_status()
            split()
        if len(active_hands)==0:
            break
    casino_move()
    print(dealers_cards)

    # if players_engine == "manual":
    #     print(f"Dealers cards: {dealers_cards}")
    #     print(f"Your cards: {players_cards}")
    #     response = input("Your move: ")
    #     if response == "stand":
    #         stand()

    #if players_engine == "basic":



    shuffle(6)
    game_of_blackjack0()