import random

class BaseBot:
    
    def __init__(self):
        
        self.name = "BaseBot"

    def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # This should return a string of the action card you want to play
        # For example: 'smithy'
        return 'action'
    
    def buy(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # bonus_coin is extra coin gotten from other effects such as moneylender
        # This should return the card you want to buy
        # For example: 'province'
           
        return 'buy'

    def remodel(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # this should return an array with the card you want to trash followed by the card you want to gain.
        # For example: ['silver', 'duchy']
        return ['trashed_card', 'gained_card']

    def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # If cards are erroneously returned, nothing will be trashed. If some of the cards are
        # erroneous but some are correct, the correct returns will still be trashed.

        return ['card_1', 'card_2', 'up_to_4']

    def militia(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # YOU SHOULD HAVE THIS METHOD EVEN IF YOU DON'T BUY MILLITIA
        # Return a list of 2 cards that you want to discard if your opponent militias you
        # Any sort of bad return will result in 2 random cards being discarded

        return ['card_1', 'card_2']

    def workshop(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
        # Return a single card you want to gain

        return 'gained_card'


    # HELPER FUNCTIONS:

    def get_coin(self, card_map, hand, bonus_coin):
        coin = 0
        for card in card_map:
            coin += hand[card] * card_map[card]['coin']
        return coin + bonus_coin

    def get_opponents_vp(self, card_map, deck, hand, trash, discard, in_play):
        vp = 0
        for card in card_map:
            vp += (card_map[card]['vp'] * 
                    (card_map[card]['start_supply'] - 
                        (deck[card] + hand[card] + discard[card] + in_play[card]) - 
                        card_map[card]['supply'] -
                        trash[card]
                    )
            )
        return vp + 3

    def get_my_vp(self, card_map, deck, hand, discard, in_play):
        vp = 0
        for card in card_map:
            vp += card_map[card]['vp'] * (deck[card] + hand[card] + discard[card] + in_play[card])
        return vp

    def get_num_actions_in_deck(self, card_map, deck, hand, discard, in_play):
        num_actions = 0
        for card in card_map:
            if 'action' in card_map[card]['types']:
                num_actions += deck[card] + hand[card] + discard[card] + in_play[card]
        return num_actions

    def get_num_cards(self, deck, hand, discard, in_play):
        return sum(deck.values()) + sum(discard.values()) + sum(hand.values()) + sum(in_play.values())

    def get_average_coin(self, card_map, deck, hand, discard, in_play):
        total_coin = 0
        for card in card_map:
            total_coin += (deck[card] + discard[card] + hand[card] + in_play[card]) * card_map[card]['coin']
        return total_coin / self.get_num_cards(card_map, deck, hand, discard, in_play)

