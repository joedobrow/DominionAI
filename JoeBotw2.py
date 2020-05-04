import BaseBot

class JoeBotw2(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'JoeBot'

	# compare multiple strategies with a grid search?
	# How many action cards to buy? 0, 1, 2, 3?
	# Which action cards?
	# Threshold for switching from money to VP

	def set_strat(num_smithy, num_moneylender, num_):
		None


	def buy(self, game, player):
		return 2

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
