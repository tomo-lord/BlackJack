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


cards_value = {}
import random

def game_of_blackjack(players_engine="rand"):
    #define the outcome of 1 BJ game (1 player vs casino)
    global deck
    def get_value(hand):
        #hand should be a list argument
        
        #calculate value and adjust for aces
        value = 0
        for card in hand:
            value += cards_value[card]
            
        aces = 0
        for card in hand: 
            if card[-1] == "A":
                aces += 1

        while value > 21 and aces >0:
            aces -= 1
            value -= 10
        return value

               
    def check_for_bust(played_hand):
        value_hand = get_value(played_hand)
        if value_hand > 21:
            print("Casino wins")
            lost_hands.append(played_hand)
            active_hands.remove(played_hand)
            return False
        else:
            #results = df.append(new_row, ignore_index=True)
            return True


    def split(played_hand):
        if len(played_hand) != 2 or played_hand[0] != played_hand[1]:
            return False
        hand2 = [played_hand[1]]
        played_hand.pop(1)
        played_hand += [deck[0]]
        deck.pop(0)
        active_hands.append(hand2)

    
    def double(played_hand):
        if len(played_hand) != 2:
            return False
        played_hand += [deck[0]]
        deck.pop(0)
        check_for_bust(played_hand)
        stand(played_hand)

    
    def hit(played_hand):
        played_hand.append(deck[0])
        deck.pop(0)
        check_for_bust(played_hand)

    def stand(played_hand):
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



    print("Game starts...")
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
    #checking for BlackJack
    if get_value(players_cards) == 21:
        print("Player wins")
        won_hands.append(players_cards)
        active_hands.remove(players_cards)
        #results = df.append(new_row, ignore_index=True)
        
        
        
        
    #players decision engine
    #in future there should be rand (random choices), basic (BJ basic strategy - proven best possible move)
    if players_engine == "rand":
        moves = [stand, hit, double, split]
        while len(active_hands) > 0:
            played_hand = active_hands[0]
            if len(played_hand) == 1:
                hit(played_hand)
            move = random.choice(moves)
            if move == "stand":
                stand(played_hand)
            if move == "hit":
                hit(played_hand)
            if move == "double":
                double(played_hand)
            if move == "split":
                split(played_hand)
        casino_move()

    # if players_engine == "manual":
    #     print(f"Dealers cards: {dealers_cards}")
    #     print(f"Your cards: {players_cards}")
    #     response = input("Your move: ")
    #     if response == "stand":
    #         stand()

    #if players_engine == "basic":