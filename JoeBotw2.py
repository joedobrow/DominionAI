import BaseBot
import random

class JoeBotw2(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'JoeBot'

	# priority list -- each card has a weight, choose the max each turn as output
	# num of provinces remaining : [1, 2, 3, 4, 5 , 6 , 7, 8]
	# num of gold in deck: [0, 1, 2, 3+]
	# num of action cards in deck [0, 1, 2, 3, 4+]
	# num of coin in hand: [0, 1, 2, 3, 4, 5, 6, 7, 8+]
	# vp spread
	# player

	#bot that simulates the rest of the game and makes a move
		self.card_index = {0: 'silver', 1: 'gold', 2: 'duchy', 3:'province', 5:'smithy'}
		self.priorities = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
		card_index_list = [3, 1, 5, 0, 2]


		for amount in self.priorities:
			self.priorities[amount] = card_index_list

		self.permuted = self.permutation(card_index_list)



	# have a priority list for each permutation, then run each 

	def get_permuted_list(self, n):
		return self.permuted[n]

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		actions = self.get_num_actions_in_deck(card_map, deck, hand, discard)

		for card_i in self.priorities[card_map['province']['supply']]:
			card = self.card_index[card_i]
			if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
				if 'action' in card_map[card]['types']:
					if actions < 2:
						return card
				else:
					return card


	def permutation(self, lst): 
	  
	    # If lst is empty then there are no permutations 
	    if len(lst) == 0: 
	        return [] 
	  
	    # If there is only one element in lst then, only 
	    # one permuatation is possible 
	    if len(lst) == 1: 
	        return [lst] 
	  
	    # Find the permutations for lst if there are 
	    # more than 1 characters 
	  
	    l = [] # empty list that will store current permutation 
	  
	    # Iterate the input(lst) and calculate the permutation 
	    for i in range(len(lst)): 
	       m = lst[i] 
	  
	       # Extract lst[i] or m from the list.  remLst is 
	       # remaining list 
	       remLst = lst[:i] + lst[i+1:] 
	  
	       # Generating all permutations where m is first 
	       # element 
	       for p in self.permutation(remLst): 
	           l.append([m] + p) 
	    return l 
	          
	  
	def action(self, card_map, deck, hand, discard, player):

		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'


class SmithyBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'SmithyBot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)

		if coin >= 8:
			return 'province'
		elif coin in [6, 7]:
			return 'gold'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard) < 1:
				return 'smithy'
			else:
				return 'silver'
		elif coin == 3:
			return 'silver'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, player):

		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class MoneylenderBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'MoneylenderBot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)

		if coin >= 8:
			if (hand['gold'] + deck['gold'] + discard['gold']) > 2:
				return 'province'
			else:
				return 'gold'
		elif coin in [6, 7]:
			return 'gold'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard) < 1:
				return 'moneylender'
			else:
				return 'silver'
		elif coin == 3:
			return 'silver'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, player):

		if hand['moneylender'] > 0:
			return 'moneylender'
		else:
			return 'noaction'

class RemodelBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'RemodelBot'


	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)

		if coin >= 8:
			if (hand['gold'] + deck['gold'] + discard['gold']) > 2:
				return 'province'
			else:
				return 'gold'
		elif coin in [6, 7]:
			return 'gold'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard) < 4:
				return 'remodel'
			else:
				return 'silver'
		elif coin == 3:
			return 'silver'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, player):

		if hand['remodel'] > 0:
			return 'remodel'
		else:
			return 'noaction'

	def remodel(self, card_map, deck, hand, discard, player):

		priority_list = {
			'remodel' : 'gold', 
			'moneylender': 'gold',
			'smithy': 'gold', 
			'copper' : 'estate', 
			'estate': 'remodel', 
			'silver': 'duchy',
			'gold': 'province'
		}
		for card in priority_list:
			if hand[card] > 0:
				return [card, priority_list[card]]


class SimulationBot:

	def __init__ (self):

		self.name = 'SimulationBot'

		self.opp_cards = {
				'copper': 0,
				'silver': 0,
				'gold': 0,
				'estate': 0,
				'duchy': 0,
				'province': 0,
				'curse': 0,
				'moneylender': 0,
				'remodel': 0,
				'smithy': 0
		}

		self.hand = [self.opp_cards.copy(), self.opp_cards.copy()]
		self.deck = [self.opp_cards.copy(), self.opp_cards.copy()]
		self.discard = [self.opp_cards.copy(), self.opp_cards.copy()]
		self.enemy = AdHocStrat()
		self.coin = 0

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		self.card_map = card_map
		self.deck[player] = deck
		self.hand[player] = hand
		self.discard[player] = discard
		self.player = player
		for card in card_map:
			self.opp_cards[card] = (
					card_map[card]['start_supply'] - 
					self.deck[card] - self.hand[card] - 
					self.discard[card]
			)

		coin = self.get_coin(card_map, hand, bonus_coin)
		legal_buys = []
		for card in card_map:
			if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0)

		for card in legal_buys:

			for i in range(100):

				self.reset_simulation(card_map, deck, hand, discard, coin, player)
				self.run_simulation

	def reset_simulation(self, card_map, deck, hand, discard, coin, player):

		self.card_map = card_map
		self.deck[player] = deck
		self.hand[player] = hand
		self.discard[player] = discard
		self.player = player
		for card in card_map:
			self.opp_cards[card] = (
					card_map[card]['start_supply'] - 
					self.deck[card] - self.hand[card] - 
					self.discard[card]
			)

	def clean_up(self, player):
            
        for card in self.card_map:
            card_amount = self.hand[player][card]
            self.discard[player][card] += card_amount
            self.hand[player][card] -= card_amount
            
        self.draw_card(5, player)


	def draw_card(self, cards, player):

		for i in range(cards):
            if sum(self.deck[player].values()) < 1:
                for card in self.card_map:
                    card_amount = self.discard[player][card]
                    self.discard[player][card] -= card_amount
                    self.deck[player][card] += card_amount
            else:
                draw = random.randint(1, sum(self.deck[player].values()))
                for card in self.card_map:
                    if draw <= self.deck[player][card]:
                        self.deck[player][card] -= 1
                        self.hand[player][card] += 1
                        break
                    draw -= self.deck[player][card]


	def run_simulation(self, card):

		self.discard[card] += 1
		self.clean_up(self.player)

		for i in range(5):
			self.draw_card(5, 1 - self.player)

		for turn in range(60):
			self.coin = 0
			action = self.enemy.action(self.card_map, self.deck[1 - player], self.hand[1 - player], self.discard[1 - player], 1 - player)
			self.execute_action(action)


	def clean_up(self, player):
            
        for card in self.card_map:
            card_amount = self.hand[player][card]
            self.discard[player][card] += card_amount
            self.hand[player][card] -= card_amount
            
        self.draw_card(5, player)

    def execute_action(self, action, player):

        if action == 'smithy':
            self.draw_card(3, player)

class AdHocStrat:

	def __init__ (self):

		self.name = 'Ad hoc strat'

    def buy (self, card_map, deck, hand, discard, bonus_coin, player):

    	provinces_remaining = card_map['province']['supply']
    	num_gold = hand['gold'] + deck['gold'] + discard['gold']
    	num_action = hand['smithy'] + deck['smithy'] + discard['smithy']
    	num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
    	average_coin = num_gold/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))

    	priority_list = {
    			'silver': 0,
    			'gold' : 0,
    			'estate' : 0,
    			'duchy' : 0,
    			'province' : 0,
    			'smithy' : 0
    	}
    	priority_list['silver'] = provinces_remaining + 2.01
    	priority_list['gold'] = provinces_remaining + 3.01
    	priority_list['smithy'] = provinces_remaining + average_coin * 3 - num_action
    	priority_list['province'] = (17 - provinces_remaining) + num_gold
    	priority_list['duchy'] = 12 - provinces_remaining

    	for card in priority_list:
    		if priority_list[card] == max(priority_list.values()):
    			return card

    def action(self, card_map, deck, hand, discard, player):

		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'


