import BaseBot

class BigMoney(BaseBot.BaseBot):

	def __init__ (self, parameters):

		self.name = 'Big Money'
		self.parameters = parameters

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		cards = ['silver', 'gold', 'estate', 'duchy', 'province', 'nobuy']

		for card in range(len(cards)):
			priority_list[cards[card]] = provinces_remaining * self.parameters[0][card] + self.parameters[1][card]


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card


		return 'nobuy'

class ChapelBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Chapel Bot'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):
		if hand['chapel'] > 0:
			return 'chapel'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_action = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))
		curve_ball = 0
		if hand['copper'] == 5:
			curve_ball = 100
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'chapel', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['chapel'] = provinces_remaining + 4 - num_action * 100 - curve_ball
		priority_list['province'] = (17 - provinces_remaining) + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cops_to_trash = 0
		to_chapel = []

		if provinces_remaining >= 3:
			for i in range(3):
				to_chapel.append('estate')

		if coin >= 8:
			num_cops_to_trash = coin - 8
		elif coin == 7:
			num_cops_to_trash = 1
		elif coin == 6:
			num_cops_to_trash = 3
		elif coin == 5:
			num_cops_to_trash = 2
		elif coin == 4:
			num_cops_to_trash = 1
		else:
			num_cops_to_trash = 4
		for i in range(num_cops_to_trash):
			to_chapel.append('copper')
		for i in range(4):
			to_chapel.append('curse')

		return to_chapel

class WitchBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Witch Bot'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['witch'] > 0:
			return 'witch'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_action = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'witch', 'estate'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['witch'] = provinces_remaining + 4.1 - num_action
		priority_list['province'] = (17 - provinces_remaining) + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card

class MoneylenderBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'MoneylenderBot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)

		if coin >= 8:
			if (hand['gold'] + deck['gold'] + discard['gold']) > 2:
				return 'province'
			else:
				return 'gold'
		elif coin in [6, 7]:
			return 'gold'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard, in_play) < 1:
				return 'moneylender'
			else:
				return 'silver'
		elif coin == 3:
			return 'silver'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['moneylender'] > 0:
			return 'moneylender'
		else:
			return 'noaction'

class RemodelBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'RemodelBot'


	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)

		if coin >= 8:
			if (hand['gold'] + deck['gold'] + discard['gold']) > 2:
				return 'province'
			else:
				return 'gold'
		elif coin in [6, 7]:
			return 'gold'
		elif coin in  [5, 4]:
			if self.get_num_actions_in_deck(card_map, deck, hand, discard, in_play) < 4:
				return 'remodel'
			else:
				return 'silver'
		elif coin == 3:
			return 'silver'
		else:
			return 'nobuy'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['remodel'] > 0:
			return 'remodel'
		else:
			return 'noaction'

	def remodel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		priority_list = {
			'curse': 'estate',
			'moneylender': 'gold',
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

class GardenBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'GardenBot'


	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_action = hand['remodel'] + deck['remodel'] + discard['remodel'] + in_play['remodel']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))
		priority_list = {}

		for card in card_map:
			if (
				card in ['silver', 'gold', 'duchy', 'province', 'remodel', 'estate', 'gardens'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				priority_list[card] = 0

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['gardens'] = 20 - provinces_remaining * 1.5
		priority_list['remodel'] = provinces_remaining + 3 - num_action*.4
		priority_list['province'] = (16 - provinces_remaining) + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['copper'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['remodel'] > 0:
			return 'remodel'
		else:
			return 'noaction'

	def remodel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		priority_list = {
			'curse': 'estate',
			'remodel' : 'gold',  
			'estate': 'gardens',
			'copper' : 'estate',
			'silver': 'duchy',
			'gold': 'province',
		}


		for card in priority_list:
			if (hand[card] > 0) and (card_map[priority_list[card]]['supply'] > 0):
				return [card, priority_list[card]]

		else:
			return ['none', 'none']

class HolyWitch(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Holy Witch'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):
		return 'village'
		if hand['witch'] > 0:
			return 'witch'

		if hand['chapel'] > 0:
			return 'chapel'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_chapel = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		num_action = self.get_num_actions_in_deck(card_map, deck, hand, discard, in_play)
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))
		curve_ball = 0
		if hand['copper'] == 5:
			curve_ball = 100
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['chapel'] = provinces_remaining + 4 - num_chapel * 100 - curve_ball
		priority_list['witch'] = provinces_remaining + 5 - num_action + card_map['curse']['supply'] - 9
		priority_list['province'] = (17 - provinces_remaining) + average_coin * 1.4
		priority_list['village'] = 100
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cops_to_trash = 0
		to_chapel = []

		if provinces_remaining >= 4:
			for i in range(3):
				to_chapel.append('estate')

		num_cops_to_trash = 10

		coin_in_deck = 0
		for card in card_map:
			coin_in_deck += (deck[card] + hand[card] + discard[card] + in_play[card]) * card_map[card]['coin']

		num_cops_to_trash = coin_in_deck - 3

		for i in range(num_cops_to_trash):
			to_chapel.append('copper')

		for i in range(5):
			to_chapel.append('curse')

		return to_chapel

class HolyWitchTest(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Holy Witch Test'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['witch'] > 0:
			return 'witch'

		if hand['chapel'] > 0:
			return 'chapel'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_chapel = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		num_action = self.get_num_actions_in_deck(card_map, deck, hand, discard, in_play)
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())
		total_coin = 0
		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))
		curve_ball = 0
		if hand['copper'] == 5:
			curve_ball = 100
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['chapel'] = provinces_remaining + 4 - num_chapel * 100 - curve_ball
		priority_list['witch'] = provinces_remaining + 5 - num_action + card_map['curse']['supply'] - 9
		priority_list['province'] = (17 - provinces_remaining) + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cops_to_trash = 0
		to_chapel = []

		if provinces_remaining >= 4:
			for i in range(3):
				to_chapel.append('estate')

		num_cops_to_trash = 10

		coin_in_deck = 0
		for card in card_map:
			coin_in_deck += (deck[card] + hand[card] + discard[card] + in_play[card]) * card_map[card]['coin']

		num_cops_to_trash = coin_in_deck - 3

		for i in range(num_cops_to_trash):
			to_chapel.append('copper')

		for i in range(5):
			to_chapel.append('curse')

		return to_chapel

class HolyWitch3(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Holy Witch 3 '

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		if hand['village'] > 0:
			return 'village'

		if hand['witch'] > 0:
			return 'witch'

		if hand['chapel'] > 0:
			return 'chapel'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):


		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_chapel = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		num_action = self.get_num_actions_in_deck(card_map, deck, hand, discard, in_play)
		curve_ball = 0
		if hand['copper'] == 5:
			curve_ball = 100
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['chapel'] = provinces_remaining + 4 - num_chapel * 100 - curve_ball
		priority_list['witch'] = provinces_remaining + 5 - num_action + card_map['curse']['supply'] - 9
		priority_list['province'] = 19 - provinces_remaining
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -1
		for card in priority_list:
			if priority_list[card] == max(priority_list.values()):
				return card


		return 'nobuy'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cops_to_trash = 0
		to_chapel = []

		if provinces_remaining >= 4:
			for i in range(3):
				to_chapel.append('estate')

		num_cops_to_trash = 10

		coin_in_deck = 0
		for card in card_map:
			coin_in_deck += (deck[card] + hand[card] + discard[card] + in_play[card]) * card_map[card]['coin']

		num_cops_to_trash = coin_in_deck - 3

		for i in range(num_cops_to_trash):
			to_chapel.append('copper')

		for i in range(5):
			to_chapel.append('curse')

		return to_chapel