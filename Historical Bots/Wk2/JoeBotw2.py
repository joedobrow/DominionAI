import BaseBot
import random
import copy

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
			return 'smithy'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard) < 1:
				return 'smithy'
			else:
				return 'silver'
		elif coin == 3:
			return 'estate'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, bonus_coin, player):

		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class CopperBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'CopperBot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		return 'copper'

class CurseBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'CurseBot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		return 'curse'

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

	def action(self, card_map, deck, hand, discard, bonus_coin, player):

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

	def action(self, card_map, deck, hand, discard, bonus_coin, player):

		if hand['remodel'] > 0:
			return 'remodel'
		else:
			return 'noaction'

	def remodel(self, card_map, deck, hand, discard, bonus_coin, player):

		priority_list = {
			'moneylender': 'gold',
			'smithy': 'gold', 
			'copper' : 'estate', 
			'estate': 'remodel', 
			'silver': 'duchy',
			'gold': 'province',
			'remodel' : 'gold', 
		}


		for card in priority_list:
			if hand[card] > 0:
				return [card, priority_list[card]]

		else:
			return ['none', 'none']


class SimulationBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'SimulationBot'
		self.me = AdHocStrat2()

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		#card_map = copy.deepcopy(card_map)
		#deck = copy.deepcopy(deck)
		#hand = copy.deepcopy(hand)
		#discard = copy.deepcopy(discard)
		#player = copy.copy(player)
		#bonus_coin = copy.copy(bonus_coin)

		coin = self.get_coin(card_map, hand, bonus_coin)
		num_actions = self.get_num_actions_in_deck(card_map, deck, hand, discard)
		
		# Obvious ad hoc conditions to reduce searching required
		potential_buys = []
		provinces = card_map['province']['supply']
		if (coin in [0, 1]):
			return 'nobuy'
		elif coin == 2:
			if (provinces < 4) and (card_map['estate']['supply'] > 0):
				return 'estate'
			else:
				return 'nobuy'
		elif coin == 3:
			if (provinces < 3) and (card_map['estate']['supply'] > 0):
				return 'estate'
			else:
				return 'silver'
		elif coin == 4:
			if (provinces < 3) and (card_map['estate']['supply'] > 0):
				return 'estate'
			elif num_actions > 3:
					return 'silver'
			elif num_actions > 1:
				potential_buys = ['silver', 'smithy']
			else:
				if card_map['smithy']['supply'] > 0:
					return 'smithy'
				else:
					return 'silver'
		elif coin == 5:
			if (card_map['province']['supply'] < 4) and (card_map['duchy']['supply'] > 0):
				return 'duchy'
			elif card_map['province']['supply'] < 6:
				if num_actions > 3:
					potential_buys = ['duchy', 'silver']
				elif num_actions > 1:
					potential_buys = ['duchy', 'silver', 'smithy']
				else:
					potential_buys = ['duchy', 'smithy']
			else:
				if num_actions > 3:
					return 'silver'
				elif num_actions > 1:
					potential_buys = ['silver', 'smithy']
				else:
					if card_map['smithy']['supply'] > 0:
						return 'smithy'
					else:
						return 'silver'

		elif coin in [6, 7]:
			if (card_map['province']['supply'] < 4) and (card_map['duchy']['supply'] > 0):
				return 'duchy'
			elif card_map['province']['supply'] < 5:
				potential_buys = ['gold', 'duchy']
			else:
				return 'gold'
		else:
			if provinces < 3:
				potential_buys = ['province', 'duchy']
			num_gold = deck['gold'] + hand['gold'] + discard['gold']
			num_silver = deck['silver'] + hand['silver'] + discard['silver']
			if (5 * num_gold + num_silver) > 5:
				return 'province'
			else:
				return 'gold'

		legal_buys = {}
		opp_vp = self.get_opponents_vp(card_map, deck, hand, discard)
		for card in potential_buys:
			if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
				legal_buys[card] = 0

		for card in legal_buys:

			for i in range(101):
				self.reset_simulation(
						copy.deepcopy(card_map), 
						copy.deepcopy(deck), 
						copy.deepcopy(hand), 
						copy.deepcopy(discard), 
						copy.deepcopy(coin)
				)
				result = self.run_simulation(card, opp_vp, card_map['province']['supply'])
				legal_buys[card] += result

		for card in legal_buys:
			if legal_buys[card] == max(legal_buys.values()):
				return card

		return 'nobuy'

	def action(self, card_map, deck, hand, discard, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'


	def reset_simulation(self, card_map, deck, hand, discard, coin):

		self.hand = hand
		self.discard = discard
		self.deck = deck
		self.coin = 0

		self.card_map = card_map
		self.card_map['province']['supply'] = max(3 - (self.hand['province'] + self.deck['province'] + self.discard['province']), 1)

	def clean_up(self):

		for card in self.card_map:

			card_amount = self.hand[card]
			self.discard[card] += card_amount
			self.hand[card] -= card_amount
		self.draw_card(5)


	def draw_card(self, cards):

		for i in range(cards):

			if sum(self.deck.values()) < 1:
				for card in self.card_map:
					card_amount = self.discard[card]
					self.discard[card] -= card_amount
					self.deck[card] += card_amount
			else:
				draw = random.randint(1, sum(self.deck.values()))
				for card in self.card_map:
					if draw <= self.deck[card]:
						self.deck[card] -= 1
						self.hand[card] += 1
						break
					draw -= self.deck[card]


	def run_simulation(self, card, opp_vp, provinces_left):

		self.discard[card] += 1
		self.clean_up()
		turns = provinces_left * 2 - 1

		for turn in range(turns):
			self.coin = 0
			self.execute_action(self.me.action(0, 0, self.hand, 0, 0))
			buy = self.me.buy(
					copy.deepcopy(self.card_map), 
					copy.deepcopy(self.deck), 
					copy.deepcopy(self.hand), 
					copy.deepcopy(self.discard), 0, 0
			)
			if buy != 'nobuy':
				self.discard[buy] += 1
				self.card_map[buy]['supply'] -= 1
			self.clean_up()
		vp = 0
		for card in self.card_map:
			vp += self.hand[card] * self.card_map[card]['vp']
			vp += self.deck[card] * self.card_map[card]['vp']
			vp += self.discard[card] * self.card_map[card]['vp']
		return vp


	def check_win(self):
		if self.card_map['province']['supply'] == 0:
			return True

	def clean_up(self):
		for card in self.card_map:
			card_amount = self.hand[card]
			self.discard[card] += card_amount
			self.hand[card] -= card_amount
		self.draw_card(5)

	def execute_action(self, action):
		if action == 'smithy':
			self.draw_card(3)

class AdHocStrat(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = hand['smithy'] + deck['smithy'] + discard['smithy']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'smithy', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['smithy'] = provinces_remaining + average_coin * 3 - num_action
		priority_list['province'] = (17 - provinces_remaining) + num_gold
		priority_list['duchy'] = 12 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 1.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, bonus_coin, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class SimpleBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'SimpleBot'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		num_actions = self.get_num_actions_in_deck(card_map, deck, hand, discard)
		if num_actions < 3:
			priority_list = ['province', 'gold', 'smithy', 'silver', 'duchy', 'estate']
		else:
			priority_list = ['province', 'gold', 'silver', 'duchy', 'estate']
		for card in priority_list:
			if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
				return card
		return 'nobuy'

	def action(self, card_map, deck, hand, discard, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class AdHocStrat2(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 2'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = max(card_map['province']['supply'] - 4, 1)
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = hand['smithy'] + deck['smithy'] + discard['smithy']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'smithy', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['smithy'] = provinces_remaining + average_coin * 3 - num_action
		priority_list['province'] = (17 - provinces_remaining) + num_gold
		priority_list['duchy'] = 12 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 1.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class SimulationBot2(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'SimulationBot2'
		self.me = AdHocStrat3()

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		#card_map = copy.deepcopy(card_map)
		#deck = copy.deepcopy(deck)
		#hand = copy.deepcopy(hand)
		#discard = copy.deepcopy(discard)
		#player = copy.copy(player)
		#bonus_coin = copy.copy(bonus_coin)

		coin = self.get_coin(card_map, hand, bonus_coin)
		num_actions = self.get_num_actions_in_deck(card_map, deck, hand, discard)
		
		# Obvious ad hoc conditions to reduce searching required
		potential_buys = []
		provinces = card_map['province']['supply']
		if (coin in [0, 1]):
			return 'nobuy'
		elif coin == 2:
			if (provinces < 4) and (card_map['estate']['supply'] > 0):
				return 'estate'
			else:
				return 'nobuy'
		elif coin == 3:
			if (provinces < 3) and (card_map['estate']['supply'] > 0):
				return 'estate'
			else:
				return 'silver'
		elif coin == 4:
			if (provinces < 3) and (card_map['estate']['supply'] > 0):
				return 'estate'
			elif num_actions > 1:
					return 'silver'
			elif num_actions > 0:
				potential_buys = ['silver', 'moneylender']
			else:
				if card_map['moneylender']['supply'] > 0:
					return 'moneylender'
				else:
					return 'silver'
		elif coin == 5:
			if (card_map['province']['supply'] < 4) and (card_map['duchy']['supply'] > 0):
				return 'duchy'
			elif card_map['province']['supply'] < 6:
				if num_actions > 3:
					potential_buys = ['duchy', 'silver']
				elif num_actions > 1:
					potential_buys = ['duchy', 'silver', 'moneylender']
				else:
					potential_buys = ['duchy', 'moneylender']
			else:
				if num_actions > 1:
					return 'silver'
				elif num_actions > 0:
					potential_buys = ['silver', 'moneylender']
				else:
					if card_map['moneylender']['supply'] > 0:
						return 'moneylender'
					else:
						return 'silver'

		elif coin in [6, 7]:
			if (card_map['province']['supply'] < 4) and (card_map['duchy']['supply'] > 0):
				return 'duchy'
			elif card_map['province']['supply'] < 5:
				potential_buys = ['gold', 'duchy']
			else:
				return 'gold'
		else:
			if provinces < 3:
				potential_buys = ['province', 'duchy']
			num_gold = deck['gold'] + hand['gold'] + discard['gold']
			num_silver = deck['silver'] + hand['silver'] + discard['silver']
			if (5 * num_gold + num_silver) > 5:
				return 'province'
			else:
				return 'gold'

		legal_buys = {}
		opp_vp = self.get_opponents_vp(card_map, deck, hand, discard)
		for card in potential_buys:
			if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
				legal_buys[card] = 0

		for card in legal_buys:

			for i in range(81):
				self.reset_simulation(
						copy.deepcopy(card_map), 
						copy.deepcopy(deck), 
						copy.deepcopy(hand), 
						copy.deepcopy(discard), 
						copy.deepcopy(coin)
				)
				result = self.run_simulation(card, opp_vp, card_map['province']['supply'])
				legal_buys[card] += result

		for card in legal_buys:
			if legal_buys[card] == max(legal_buys.values()):
				return card

		return 'nobuy'

	def action(self, card_map, deck, hand, discard, bonus_coin, player):
		if hand['moneylender'] > 0:
			return 'moneylender'
		else:
			return 'noaction'


	def reset_simulation(self, card_map, deck, hand, discard, coin):

		self.hand = hand
		self.discard = discard
		self.deck = deck
		self.coin = 0

		self.card_map = card_map
		self.card_map['province']['supply'] = max(3 - (self.hand['province'] + self.deck['province'] + self.discard['province']), 1)

	def clean_up(self):

		for card in self.card_map:

			card_amount = self.hand[card]
			self.discard[card] += card_amount
			self.hand[card] -= card_amount
		self.draw_card(5)


	def draw_card(self, cards):

		for i in range(cards):

			if sum(self.deck.values()) < 1:
				for card in self.card_map:
					card_amount = self.discard[card]
					self.discard[card] -= card_amount
					self.deck[card] += card_amount
			else:
				draw = random.randint(1, sum(self.deck.values()))
				for card in self.card_map:
					if draw <= self.deck[card]:
						self.deck[card] -= 1
						self.hand[card] += 1
						break
					draw -= self.deck[card]


	def run_simulation(self, card, opp_vp, provinces_left):

		self.discard[card] += 1
		self.clean_up()
		turns = provinces_left * 2 - 1

		for turn in range(turns):
			self.coin = 0
			self.execute_action(self.me.action(0, 0, self.hand, 0, 0))
			buy = self.me.buy(
					copy.deepcopy(self.card_map), 
					copy.deepcopy(self.deck), 
					copy.deepcopy(self.hand), 
					copy.deepcopy(self.discard), self.coin, 0
			)
			if buy != 'nobuy':
				self.discard[buy] += 1
				self.card_map[buy]['supply'] -= 1
			self.clean_up()
		vp = 0
		for card in self.card_map:
			vp += self.hand[card] * self.card_map[card]['vp']
			vp += self.deck[card] * self.card_map[card]['vp']
			vp += self.discard[card] * self.card_map[card]['vp']
		return vp


	def check_win(self):
		if self.card_map['province']['supply'] == 0:
			return True

	def clean_up(self):
		for card in self.card_map:
			card_amount = self.hand[card]
			self.discard[card] += card_amount
			self.hand[card] -= card_amount
		self.draw_card(5)

	def execute_action(self, action):
		if action == 'moneylender':
			if self.hand['copper'] > 0:
				self.hand['copper'] -= 1
				self.coin += 3

class AdHocStrat3(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 3'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = max(card_map['province']['supply'] - 4, 1)
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = hand['moneylender'] + deck['moneylender'] + discard['moneylender']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'moneylender', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['moneylender'] = provinces_remaining + average_coin * 3 - num_action
		priority_list['province'] = (17 - provinces_remaining) + num_gold
		priority_list['duchy'] = 12 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 1.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, player):
		if hand['moneylender'] > 0:
			return 'moneylender'
		else:
			return 'noaction'

class AdHocStrat4(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 4'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = 0
		for card in card_map:
			if 'action' in card_map[card]['types']:
				num_action += hand[card] + deck[card] + discard[card]
		if num_action == 0:
			action_to_buy = 'moneylender'
		else:
			action_to_buy = 'smithy'

		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', action_to_buy, 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list[action_to_buy] = provinces_remaining + average_coin * 3 - num_action
		priority_list['province'] = (17 - provinces_remaining) + num_gold
		priority_list['duchy'] = 12 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 1.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, player):
		if hand['moneylender'] > 0:
			return 'moneylender'
		else:
			return 'noaction'

class AdHocStrat5(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 5'
		self.data = []

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = 0
		for card in card_map:
			if 'action' in card_map[card]['types']:
				num_action += hand[card] + deck[card] + discard[card]
		action_to_buy = 'remodel'

		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', action_to_buy, 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list[action_to_buy] = provinces_remaining + average_coin * 3 - num_action + 1
		priority_list['province'] = (17 - provinces_remaining) + num_gold
		priority_list['duchy'] = 12 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 1.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, bonus_coin, player):

		if hand['remodel'] > 0:
			return 'remodel'
		else:
			return 'noaction'

	def remodel(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = 0
		for card in card_map:
			if 'action' in card_map[card]['types']:
				num_action += hand[card] + deck[card] + discard[card]
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))

		priority_list = []
		if hand['estate'] > 0:
			priority_list.append(['estate', 'remodel'])
			priority_list.append(['estate', 'silver'])
		if hand['copper'] > 0:
			priority_list.append(['copper', 'estate'])
		if hand['silver'] > 0:
			priority_list.append(['silver', 'duchy'])
		if hand['remodel'] > 0:
			priority_list.append(['remodel', 'gold'])
			priority_list.append(['remodel', 'duchy'])
		if hand['gold'] > 0:
			priority_list.append(['gold', 'province'])
		if len(priority_list) > 0:
			i = random.randint(0, len(priority_list) - 1)
			self.data.append([coin, provinces_remaining, num_action, average_coin, priority_list[i][0], priority_list[i][1]])
			return priority_list[i]
		else:
			return ['none', 'none']

class AdHocStrat6(BaseBot.BaseBot):

	# Assumes other 2 actions are not playable.

	def __init__ (self, parameters):

		# provinces, actions, avg_coin, biases

		self.name = 'Ad hoc strat 6'
		self.parameters = parameters

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces = card_map['province']['supply']
		num_action = 0
		for card in card_map:
			if 'action' in card_map[card]['types']:
				num_action += hand['smithy'] + deck['smithy'] + discard['smithy']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/num_cards


		priority_list = {}

		parameters = self.parameters
		priority_list = []
		# provinces remaining, num_actions, average_coin
		cards = ['silver', 'gold', 'smithy','estate', 'duchy', 'province', 'nobuy']
		for card in range(len(cards)):
			priority_list.append(parameters[2][card] + provinces * parameters[0][card] + average_coin * parameters[1][card])
		new_list = [0] * len(cards)
		for card in range(len(priority_list)):
			if cards[card] != 'nobuy':
				if (coin >= card_map[cards[card]]['cost']) and (card_map[cards[card]]['supply'] > 0):
					new_list[card] = priority_list[card]
				else:
					new_list[card] = -9999
		for card in range(len(new_list)):
			if new_list[card] == max(new_list):
				return cards[card]


		return 'nobuy'

	def action(self, card_map, deck, hand, discard, bonus_coin, player):
		if hand['smithy'] > 0:
			return 'smithy'
		return 'noaction'

class AdHocStrat7(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 7'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_gold = hand['gold'] + deck['gold'] + discard['gold']
		num_action = hand['smithy'] + deck['smithy'] + discard['smithy']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		opp_vp = 6
		my_vp = 0
		for card in card_map:
			opp_vp += (card_map[card]['start_supply'] - card_map[card]['supply'] - discard[card] - deck[card] - hand[card]) * card_map[card]['vp']
			my_vp += (discard[card] + deck[card] + hand[card]) * card_map[card]['vp']
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		if (provinces_remaining == 2) and (average_coin > 1):


			if my_vp > opp_vp:
				priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
			elif my_vp == opp_vp:
				if player == 0:
					priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
				else:
					priority_list = ['duchy', 'estate', 'province', 'gold', 'silver']
			elif (my_vp + 1 == opp_vp):
				if player == 0:
					priority_list = ['duchy', 'estate', 'province', 'gold', 'silver']
				else:
					priority_list = ['duchy', 'province', 'gold', 'estate', 'silver']
			elif (my_vp + 2 <= opp_vp):
				priority_list = ['duchy', 'province', 'gold', 'estate', 'silver']
			elif my_vp + 3 <= opp_vp and player == 0:
				priority_list = ['duchy', 'province', 'gold', 'silver']
			else:
				priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']

			for card in priority_list:
				if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
					#print(provinces_remaining, average_coin, card, my_vp, opp_vp)
					return card
		elif provinces_remaining == 1:

			if my_vp > opp_vp - 6:
				priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
			elif my_vp == opp_vp - 6:
				if player == 0:
					priority_list = ['province', 'duchy', 'estate', 'gold', 'silver']
				else:
					priority_list = ['duchy', 'estate', 'gold', 'silver']
			else:
				priority_list = ['duchy', 'estate', 'gold', 'silver']

			for card in priority_list:
				if (card_map[card]['cost'] <= coin) and (card_map[card]['supply'] > 0):
					return card

		else:

			for card in card_map:
				if (
					card in ['silver', 'gold', 'duchy', 'province', 'smithy', 'estate'] and
					card_map[card]['cost'] <= coin and
					card_map[card]['supply'] > 0
				):
					priority_list[card] = 0

			priority_list['silver'] = provinces_remaining + 2.01
			priority_list['gold'] = provinces_remaining + 3.01
			priority_list['smithy'] = provinces_remaining + average_coin * 3 - num_action*1.1
			priority_list['province'] = (17 - provinces_remaining) + average_coin*2
			priority_list['duchy'] = 13 - provinces_remaining
			priority_list['estate'] = 6.5 - provinces_remaining
			priority_list['nobuy'] = provinces_remaining - 2.02


			for card in priority_list:
				if card != 'nobuy':
					if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
						priority_list[card] = -1
			for card in priority_list:
				if priority_list[card] == max(priority_list.values()):
					return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, bonus_coin, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

class AdHocStrat8(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Ad hoc strat 8'

	def buy (self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_action = hand['smithy'] + deck['smithy'] + discard['smithy']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'smithy', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['smithy'] = provinces_remaining + average_coin * 3 - num_action*1.1
		priority_list['province'] = (17 - provinces_remaining) + average_coin*2
		priority_list['duchy'] = 13 - provinces_remaining
		priority_list['estate'] = 6.5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'
	def action(self, card_map, deck, hand, discard, bonus_coin, player):
		if hand['smithy'] > 0:
			return 'smithy'
		else:
			return 'noaction'

	# joes code
#	for j in bots[1].data:
#		j.append(result[0])
#		this_data.append(j)
#	bots[1].data = []
#
#	for j in bots[0].data:
#		j.append(1 - result[0])
#		this_data.append(j)
#	bots[1].data = []

#df = pd.DataFrame(this_data)
#df.to_csv(
#		'/Users/jdobrow/Code/DominionAI/traindata.py', 
#		index=False,
#		header=['coin', 'provinces', 'num_action', 'average_coin', 'trash', 'gain', 'win'])
