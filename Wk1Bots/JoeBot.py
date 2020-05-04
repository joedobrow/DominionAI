class JoeBot:

    def __init__(self):

        self.name = "JoeBot"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']
        
        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining > 3:
            priority_list = ['province', 'gold', 'silver', 'duchy']
        elif provinces_remaining == 3:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot2:

    def __init__(self):

        self.name = "JoeBot2"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']
        
        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining == 5:
            priority_list = ['province', 'gold', 'silver', 'duchy']
        elif provinces_remaining == 4:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot25:

    def __init__(self):

        self.name = "JoeBot25"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        num_gold = hand['gold'] + discard['gold'] + deck['gold']
        num_silver = hand['silver'] + discard['silver'] + deck['silver']

        vp = 0
        for card in env.card_map.keys():
            vp += deck[card]*env.card_map[card]['vp']
            vp += hand[card]*env.card_map[card]['vp']
            vp += discard[card]*env.card_map[card]['vp']
        opp_vp = 0
        for card in env.card_map.keys():
            opp_vp += env.card_map[card]['vp'] * 8
            opp_vp -= env.card_map[card]['supply'] * env.card_map[card]['vp']
            opp_vp -= deck[card]*env.card_map[card]['vp']
            opp_vp -= hand[card]*env.card_map[card]['vp']
            opp_vp -= discard[card]*env.card_map[card]['vp']
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']

        if provinces_remaining > 7:
            if (num_gold < 1) and (num_silver < 6):
                priority_list = ['gold', 'silver']
            else:
                priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining == 5:
            priority_list = ['province', 'gold', 'duchy', 'silver']
        elif provinces_remaining in [4, 3]:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        elif provinces_remaining == 2:
            if vp < opp_vp:
                if (opp_vp - vp) == 1:
                    priority_list = ['duchy', 'estate', 'province', 'gold', 'silver']
                else:
                    priority_list = ['duchy', 'province' 'gold', 'silver', 'estate']
            elif vp == opp_vp:
                priority_list = ['duchy', 'estate', 'province', 'gold', 'silver']
            else:
               priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        elif provinces_remaining == 1:
            if opp_vp - vp > 6:
                priority_list = ['duchy', 'estate', 'gold', 'silver']
            else:
                priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot3:

    def __init__(self):

        self.name = "JoeBot3"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']
        
        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining > 4:
            priority_list = ['province', 'gold', 'silver', 'duchy']
        elif provinces_remaining == 4:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        elif provinces_remaining == 3:
            priority_list = ['province', 'duchy', 'gold', 'silver', 'estate']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot4:

    def __init__(self):

        self.name = "JoeBot4"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']
        
        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining > 4:
            priority_list = ['province', 'gold', 'silver', 'duchy']
        elif provinces_remaining == 4:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        elif provinces_remaining == 3:
            priority_list = ['province', 'duchy', 'gold', 'silver', 'estate']
        elif provinces_remaining == 2:
            priority_list = ['duchy', 'estate', 'province', 'gold', 'silver']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot5:

    def __init__(self):

        self.name = "JoeBot5"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']
        
        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining > 4:
            priority_list = ['province', 'gold', 'silver', 'duchy']
        elif provinces_remaining == 4:
            priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        elif provinces_remaining == 3:
            priority_list = ['province', 'duchy', 'gold', 'silver', 'estate']
        else:
            priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot6:

    def __init__(self):

        self.name = "JoeBot6"

    def get_moves(self, env, deck, hand, discard):
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']

        vp = 0
        for card in env.card_map.keys():
            vp += deck[card]*env.card_map[card]['vp']
            vp += hand[card]*env.card_map[card]['vp']
            vp += discard[card]*env.card_map[card]['vp']
        opp_vp = 0

        for card in env.card_map.keys():
            opp_vp += env.card_map[card]['vp'] * 8
            opp_vp -= env.card_map[card]['supply'] * env.card_map[card]['vp']
            opp_vp -= deck[card]*env.card_map[card]['vp']
            opp_vp -= hand[card]*env.card_map[card]['vp']
            opp_vp -= discard[card]*env.card_map[card]['vp']
        
        if provinces_remaining > 6:
            priority_list = ['gold', 'silver']

        if provinces_remaining > 5:
            priority_list = ['province', 'gold', 'silver']
        elif provinces_remaining == 5:
            if vp == opp_vp:
                priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
            else:
                priority_list = ['province', 'gold', 'duchy', 'silver']
        elif provinces_remaining == 4:
            if vp == opp_vp:
                priority_list = ['province', 'duchy' 'gold', 'silver']
            else:
                priority_list = ['province', 'duchy', 'gold', 'silver']
        elif provinces_remaining == 3:
            priority_list = ['province', 'duchy', 'gold', 'silver', 'estate']
        else:
            if vp == opp_vp:
                priority_list = ['province', 'duchy', 'gold', 'silver', 'estate']
            else:
                priority_list = ['province', 'duchy', 'gold', 'estate', 'silver']
        
        for card in priority_list:
            if card in legal_moves:
                return card
        return []

class JoeBot7:

    def __init__(self):

        self.name = "JoeBot7"

    def get_moves(self, env, deck, hand, discard):

        purchased_cards = 0
        purchased_cards += 45 - env.card_map['copper']['supply']
        purchased_cards += 30 - env.card_map['silver']['supply']
        purchased_cards += 30 - env.card_map['gold']['supply']
        purchased_cards += 8 - env.card_map['estate']['supply']
        purchased_cards += 8 - env.card_map['duchy']['supply']
        purchased_cards += 8 - env.card_map['province']['supply']
        purchased_cards += 8 - env.card_map['curse']['supply']
        if purchased_cards % 2 == 0:
            probable_player = 1
        else:
            probable_player = -1
        
        coin = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        
        legal_moves = []
        for card in env.card_map.keys():
            if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                legal_moves.append(card)
                
        provinces_remaining = env.card_map['province']['supply']

        vp = 0
        for card in env.card_map.keys():
            vp += deck[card]*env.card_map[card]['vp']
            vp += hand[card]*env.card_map[card]['vp']
            vp += discard[card]*env.card_map[card]['vp']
        opp_vp = 0

        for card in env.card_map.keys():
            opp_vp += env.card_map[card]['vp'] * 8
            opp_vp -= env.card_map[card]['supply'] * env.card_map[card]['vp']
            opp_vp -= deck[card]*env.card_map[card]['vp']
            opp_vp -= hand[card]*env.card_map[card]['vp']
            opp_vp -= discard[card]*env.card_map[card]['vp']

        num_gold = hand['gold'] + discard['gold'] + deck['gold']
        num_silver = hand['silver'] + discard['silver'] + deck['silver']
        priority_list = []

        if coin >= 8:
            if (num_gold == 0) and (num_silver <= 5):
                priority_list = ['gold', 'province', 'silver', 'duchy']
            else:
                if provinces_remaining == 2:
                    if opp_vp > vp:
                        if opp_vp - vp == 1:
                            priority_list = ['duchy', 'estate', 'province']
                        else:
                            priority_list = ['duchy', 'province']
                    else:
                        return 'province'

                else:
                    return 'province'
        elif coin >= 6:
            if provinces_remaining <= 4:
                priority_list = ['duchy', 'gold', 'estate', 'silver']
            else:
                priority_list = ['gold', 'duchy', 'silver', 'estate']
        elif coin == 5:
            if provinces_remaining <= 5:
                priority_list = ['duchy', 'silver', 'estate']
            else:
                priority_list = ['silver', 'duchy', 'estate']
        elif coin >= 3:
            if provinces_remaining <= 3:
                priority_list = ['estate', 'silver']
            else:
                priority_list = ['silver']
        else:
            if provinces_remaining <= 3:
                priority_list = ['estate']
            else:
                return None

        for card in priority_list:
            if card in legal_moves:
                return card
        return []

# duchy dancing is bad

# duchy dancing is bad