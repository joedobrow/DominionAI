import BaseBot

class MilitiaMcCarthy(BaseBot.BaseBot):

    # MESS AROUND WITH THESE
    BIG_FAT_DUCHY_TIME = 4
    GAME_OF_INCHES = 2
    CHAPEL_COUNT = 0
    COUNCIL_ROOM_COUNT = 0.0
    VILLAGE_COUNT = 0.0
    MILITIA_COUNT = 0.0
    SILVER_COUNT = 0.0
    GOLDEN_COUNCIL_ROOM_RATIO = .1
    COPPERS_BURNED = 0
    ESTATES_BURNED = 0
    BURNED_ENOUGH = 6
    ENOUGH_SHIT_CARDS = 3

    def __init__ (self):

        self.name = 'Militia McCarthy'
        
    def action(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
        if (hand['village'] > 0):
            return 'village'
        elif (hand['chapel'] > 0): 
            if (hand['council_room'] == 0 and hand['militia'] == 0):
                return 'chapel'
            elif (hand['copper'] + hand['estate'] + hand['curse'] >= self.ENOUGH_SHIT_CARDS):
                return 'chapel'
            else:
                if (hand['council_room'] > 0):
                    return 'council_room'
                else:
                    return 'militia'
        else:
            if (hand['council_room'] > 0):
                return 'council_room'
            else:
                return 'militia'

    def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

        provinces_remaining = card_map['province']['supply']
        
        if (coin >= card_map['province']['cost'] and provinces_remaining > 0 and self.COUNCIL_ROOM_COUNT > 0 ):
            return 'province'

        elif (provinces_remaining < self.BIG_FAT_DUCHY_TIME and coin >= card_map['duchy']['cost'] and card_map['duchy']['supply'] > 0):
            return 'duchy'

        elif (provinces_remaining < self.GAME_OF_INCHES and coin >= card_map['estate']['cost'] and  card_map['estate']['supply'] > 0):
            return 'estate'

        else:
            if (coin >= card_map['gold']['cost'] and card_map['gold']['supply'] > 0 and self.COUNCIL_ROOM_COUNT > 0):
                return 'gold'
            elif (coin >= card_map['council_room']['cost'] and self.COUNCIL_ROOM_COUNT < 1):
                self.COUNCIL_ROOM_COUNT += 1
                return 'council_room'
            elif (coin >= card_map['chapel']['cost'] and self.CHAPEL_COUNT < 1):
                self.CHAPEL_COUNT += 1
                return 'chapel'
            elif (coin >= card_map['village']['cost'] and self.VILLAGE_COUNT < 2 and self.SILVER_COUNT > 1):
                self.VILLAGE_COUNT += 1
                return 'village'
            elif (coin >= card_map['militia']['cost'] and self.MILITIA_COUNT < 2 and self.VILLAGE_COUNT > 0):
                self.MILITIA_COUNT += 1
                return 'militia'
            elif (coin >= card_map['silver']['cost'] and card_map['silver']['supply'] > 0):
                self.SILVER_COUNT += 1
                return 'silver'
            else:
                return -1

    def chapel(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
        # If cards are erroneously returned, nothing will be trashed. If some of the cards are
        # erroneous but some are correct, the correct returns will still be trashed.
        provinces_remaining = card_map['province']['supply']
        trashTheseShitCards = []
        for i in range(hand['curse']):
            trashTheseShitCards.append('curse')
        for i in range(hand['copper']):
            trashTheseShitCards.append('copper')
            self.COPPERS_BURNED += 1
        if provinces_remaining == card_map['province']['supply'] > self.BIG_FAT_DUCHY_TIME:
            for i in range(hand['estate']):
                trashTheseShitCards.append('estate')
                self.ESTATES_BURNED += 1
        coin = 3 * hand['gold'] + 2 * hand['silver'] + hand['copper']
        if (coin - hand['copper']) == 4 or (coin - hand['copper']) == 2:
            if ('copper' in trashTheseShitCards):
                trashTheseShitCards.remove('copper')

        return trashTheseShitCards[0:4]

    def militia(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
        # YOU SHOULD HAVE THIS METHOD EVEN IF YOU DON'T BUY MILLITIA
        # Return a list of 2 cards that you want to discard if your opponent militias you
        # Any sort of bad return will result in 2 random cards being discarded
        shittiest_to_best = ['province', 'duchy', 'estate', 'curse', 'chapel', 'copper', 'silver', 'militia', 'village', 'council_room']
        ditch_these = []
        for card in shittiest_to_best:
            count = hand[card]
            while count > 0 and len(ditch_these) < 2:
                ditch_these.append(card)
        return ditch_these

    # HELPER FUNCTIONS:

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

            
