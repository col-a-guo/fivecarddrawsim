import random
suits = ['d','c','h','s']
nums = [1,2,3,4,5,6,7,8,9,10,11,12,13]

def drawCard(hand):
    deck_size = len(deck)
    rand_card_i = random.randint(0,deck_size-1)
    rand_card = deck.pop(rand_card_i)
    hand.append(rand_card)
    return hand

def drawCards(hand, num_cards):
    for i in range(num_cards):
        hand = drawCard(hand)
    return hand


def straightCheck(hand):
    matches = [0 for i in range(9)]
    best_match = -1
    straight_start = -1
    straights = [[num1+num2+1 for num1 in range(5)] for num2 in range(8)]
    straights.append([10,11,12,13,1])
    hand_nums = [card[0] for card in hand]
    for i, straight in enumerate(straights):
        straight_matches = 0
        for straight_check_num in straight:
            if straight_check_num in hand_nums:
                straight_matches += 1
        if straight_matches > best_match:
            best_match = straight_matches
            straight_start = i+1
    return best_match, straight_start

def flushCheck(hand):
    matches = [0,0,0,0]
    for i, suit in enumerate(suits):
        for card in hand:
            if card[1] == suit:
                matches[i] += 1
    max_value = max(matches)
    max_index = matches.index(max_value)
    return max_value, suits[max_index]


def hand_AI(hand):
    #check for pairs and trips
    card_memory = []
    pair_flag = False
    pair_memory = []
    trip_id = -1
    
    for card in hand:
        if card[0] in pair_memory:
            trip_id = card[0]

        if card[0] in card_memory:
            pair_flag = True
            pair_memory.append(card[0])

        card_memory.append(card[0])

#Always try to extend trips if present
    if trip_id != -1:
        discards = 0
        for i, card in enumerate(hand):
            if card[0] != trip_id:
                hand.pop(i)
                discards += 1
        hand = drawCards(hand, discards)

#Pair Handling
    elif pair_flag == True:
        #Two pair: Try for full house
        if len(pair_memory) == 4:
            discards = 0
            for i, card in enumerate(hand):
                if card[0] not in pair_memory:
                    hand.pop(i)
                    discards += 1
            hand = drawCards(hand, discards)
        #High pair: Try for trips
        elif pair_memory[0] > 9 or pair_memory[0] == 1:
            discards = 0
            for i, card in enumerate(hand):
                if card[0] not in pair_memory:
                    hand.pop(i)
                    discards += 1
            hand = drawCards(hand, discards)
        else:
            #check for straights and flushes
            
            flush_matches, flush_suit = flushCheck(hand)
            straight_matches, straight_start = straightCheck(hand)
            if flush_matches > 3:
                discards = 0
                for i, card in enumerate(hand):
                    if card[1] != flush_suit:
                        hand.pop(i)
                        discards += 1
                hand = drawCards(hand, discards)
            elif straight_matches > 3:
                card_memory_straight = []
                discards = 0
                for i, card in enumerate(hand):
                    if card in card_memory_straight:
                        hand.pop(i)
                        discards += 1
                    else:
                        card_memory_straight.append(card)
            else:
                discards = 0
                for i, card in enumerate(hand):
                    if card[0] not in pair_memory:
                        hand.pop(i)
                        discards += 1
                hand = drawCards(hand, discards)

#High card handling:
    else:
        flush_matches, flush_suit = flushCheck(hand)
        straight_matches, straight_start = straightCheck(hand)
        hand_nums = [card[0] for card in hand]
        highcard = max(hand_nums)
        #Four for flush is best
        if flush_matches > 3:
            discards = 0
            for i, card in enumerate(hand):
                if card[1] != flush_suit:
                    hand.pop(i)
                    discards += 1
            hand = drawCards(hand, discards)
        #Then four for straight
        elif straight_matches > 3:
            card_memory_straight = []
            discards = 0
            for i, card in enumerate(hand):
                if card in card_memory_straight:
                    hand.pop(i)
                    discards += 1
                else:
                   card_memory_straight.append(card)
        #Then highcard
        elif highcard > 9 or highcard == 1:
            discards = 0
            for i, card in enumerate(hand):
                    if card[0] != highcard:
                        hand.pop(i)
                        discards += 1
            hand = drawCards(hand, discards)
        #Then 3 flush
        elif flush_matches > 2:
            discards = 0
            for i, card in enumerate(hand):
                if card[1] != flush_suit:
                    hand.pop(i)
                    discards += 1
            hand = drawCards(hand, discards)
        else:
            discards = 0
            for i, card in enumerate(hand):
                if card[0] != highcard:
                    hand.pop(i)
                    discards += 1
            hand = drawCards(hand, discards)
    return hand
        
straights = 0
flushes = 0
raw_straights = 0
raw_flushes = 0
three_flushes = 0
three_flush_conversions = 0

for round in range(100000):

    deck = [(num, suit) for suit in suits for num in nums]
    hands = [[],[],[],[]]

    three_flush_hand = -1
    for i, hand in enumerate(hands):
        hand = drawCards(hand, 5)
        if straightCheck(hand)[0] > 4:
            raw_straights += 1
        if flushCheck(hand)[0] > 4:
            raw_flushes += 1
        if flushCheck(hand)[0] == 3:
            three_flushes += 1
            three_flush_hand = i


    for i, hand in enumerate(hands):
        hand = hand_AI(hand)
        if straightCheck(hand)[0] > 4:
            straights += 1
        if flushCheck(hand)[0] > 4:
            flushes += 1
            if i == three_flush_hand:
                three_flush_conversions += 1

print("Straights, Flushes:")
print(straights, flushes)
print("First Draw Straights, Flushes:")
print(raw_straights, raw_flushes)
print("3Flushes")
print(three_flushes)
print("3Flushes that became flushes")
print(three_flush_conversions)