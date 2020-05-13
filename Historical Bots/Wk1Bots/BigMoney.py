import random

class BigMoney:

    def __init__(self):
        self.name = "BigMoney"
        # 0 == buy money, 1 == be creative, 2 == buy vps
        self.strategy_mode = 0

        # tweakables:
        self.sample_hand_enough_money = 8
        self.number_of_sample_hands = 3
    def get_moves(self, env, deck, hand, discard):
        money = total_money(hand)

        if (any_sample_hand_has_enough_money(sample_hands(deck, discard, self.number_of_sample_hands), self.sample_hand_enough_money)):
            return buy_best_vp_card(env.card_map, money)
        else:
            return buy_best_money_card(env.card_map, money)


def buy_best_money_card(card_map, money):
    if money >= card_map['gold']['cost'] and card_map['gold']['supply'] > 0:
        return 'gold'
    if money >= card_map['silver']['cost'] and card_map['silver']['supply'] > 0:
        return 'silver'
    return -1 # dont buy copper dummy

def buy_best_vp_card(card_map, money):
    if money >= card_map['province']['cost'] and card_map['province']['supply'] > 0:
        return 'province'
    if money >= card_map['duchy']['cost'] and card_map['duchy']['supply'] > 0:
        return 'duchy'
    else:
        return 'estate'

# not used, but probably good to have
def all_sample_hands_have_enough_money(hands, value):
    for hand in hands:
        if total_money(hand) < value:
            return False
    return True

def any_sample_hand_has_enough_money(hands, value):
    for hand in hands:
        if total_money(hand) >= value:
            return True
    return False

def sample_hands(deck, discard, n):
    hands = []
    for i in range(n):
        hands.append(sample_hand(deck, discard))
    return hands

def total_money(hand):
    return hand['copper'] + hand['silver']*2 + hand['gold']*3

def sample_hand(deck, discard):
    total_deck = {}
    hand = {}
    for card in deck.keys():
        total_deck[card] = deck[card] + discard[card]
        hand[card] = 0

    for i in range(5):
        draw = random.randint(1, sum(total_deck.values()))
        for card in total_deck.keys():
            if draw <= total_deck[card]:
                total_deck[card] -= 1
                hand[card] += 1
                break
            draw -= total_deck[card]

    return hand

def average_money_in_deck(deck, hand, discard):
    return (money_in_object(deck) / num_cards_i_got(deck, hand, discard)) * 5

def average_money_in_total(deck, hand, discard):
    return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand)) / num_cards_i_got(deck, hand, discard)) * 5

def money_in_object(array):
    return array[0] + array[1]*2 + array[2]*3

def num_cards_i_got(deck, hand, discard):
    return sum(deck) + sum(hand) + sum(discard)


