import BaseBot
import copy

class GeneralBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Generalized Bot'
		self.no_buy_val = 1.5
		self.phase = None

	def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		self.phase = 'buy'
		self.card_map = card_map
		self.deck = deck
		self.hand = hand
		self.discard = discard
		self.coin = coin
		self.actions = actions
		self.buys = buys
		self.in_play = in_play
		self.trash = trash
		self.attack_immune = attack_immune
		self.player = player


		values = {}
		for card in card_map:
			if card_map[card]['cost'] <= self.coin:
				values[card] = self.getVal(card)
		values['nobuy'] = self.no_buy_val
		#print(values)
		for card in values:
			if values[card] == max(values.values()):
				return card

	def coinVal(self, n):
		return n

	def actionVal(self, n):
 		total_cards = sum(self.hand.values()) + sum(self.deck.values()) + sum(self.discard.values()) + sum(self.in_play.values())
 		if n == 1:
 			return 0
 		else:
 			net_actions = 0
 			for card in self.card_map:
 				if 'action' in self.card_map[card]['types']:
 					net_actions -= (self.hand[card] + self.deck[card] + self.discard[card] + self.in_play[card])
 				if card == 'village':
 					net_actions += 2 * (self.hand[card] + self.deck[card] + self.discard[card] + self.in_play[card])
 			if n == 0:
 				return min(net_actions * 6/(total_cards - 3.9) - .25, 0)
 			else:
 				if net_actions >= 0:
 					return .1 * n
 				else:
 					return .3 * n - (net_actions * .3) * 4 / (total_cards - 3.9)


	def vpVal(self, n):

		return (n**2) / 8 + (9 - self.card_map['province']['supply']) / 3

	def cardVal(self, n):

		return n * 1.1

		# if village in hand its avg value of deck * n
		# otherwise, other actions drawn are dead, including future bought ones
		# have to consider maxing out gold and such as well

	def buyVal(self, n):

		return 0.1

		#function of how much gold will get

	def trashVal(self, n):
		return 1.4 + n/3

	def getVal(self, card):

		if card == 'copper':
			return self.coinVal(1)

		elif card == 'silver':
			return self.coinVal(2)

		elif card == 'gold':
			return self.coinVal(3)

		elif card == 'estate':
			if self.phase == 'militia':
				return 0
			return self.vpVal(1)

		elif card == 'duchy':
			if self.phase == 'militia':
				return 0
			return self.vpVal(3)

		elif card == 'province':
			if self.phase == 'militia':
				return 0
			return self.vpVal(6)

		elif card == 'curse':
			return -10

		elif card == 'chapel':
		# if more trash is added in need to factor in chance to trash this later
			if self.phase != 'buy':
				return self.trashVal(4)

			num_chapels = self.hand['chapel'] + self.deck['chapel'] + self.discard['chapel'] + self.in_play['chapel']
			if self.hand['copper'] < 5:
				return self.trashVal(4) - num_chapels * 3
			else:
				return 0

		elif card == 'council_room':
			# add in value of chances of drawing a militia AND having an extra action
			return self.cardVal(4) + self.buyVal(1) - self.cardVal(1) * 1.2 + self.actionVal(0)

		elif card == 'gardens':
			est = 25
			#estimate cards at end of game
			return self.vpVal(est // 10)

		elif card == 'militia':
			num_militia = self.hand['militia'] + self.discard['militia'] + self.deck['militia'] + self.in_play['militia']
			return self.coinVal(2) + self.actionVal(0) + (1 - num_militia/2)

		elif card == 'moat':
			#Number of attacks opponent has
			num_opp_attacks = 0
			for card in self.card_map:
				if 'attack' in self.card_map[card]['types']:
					num_opp_attacks -= (self.hand[card] + self.discard[card] + self.deck[card] + self.in_play[card])
					num_opp_attacks += self.card_map[card]['start_supply'] - self.card_map[card]['supply']
				
			return self.cardVal(2) + self.actionVal(0) + num_opp_attacks * .25

		elif card == 'moneylender':
			#minus chance of no copper
			#affected by other trash
			#return self.coinVal(3) + self.actionVal(0)
			return 0

		elif card == 'remodel':
			return 0
			# this is hard

		elif card == 'village':
			return self.cardVal(1) + self.actionVal(2)

		elif card == 'witch':
			#value changes if action or buy
			num_curses = self.card_map['curse']['supply']
			return self.cardVal(2) + self.actionVal(0) + num_curses * .25

		elif card == 'workshop':
			return 0
			# manual
			# this might be a base comparison for future workshops

	def action(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		for card in hand:
			if 'action' in card_map[card]['types']:

				self.phase = 'action'
				self.card_map = card_map
				self.deck = deck
				self.hand = hand
				self.discard = discard
				self.coin = coin
				self.actions = actions
				self.buys = buys
				self.in_play = in_play
				self.trash = trash
				self.attack_immune = attack_immune
				self.player = player

				if hand['village'] > 0:
					return 'village'
				legal_actions = {}
				for card in card_map:
					if 'action' in card_map[card]['types']:
						if hand[card] > 0:
							legal_actions[card] = self.getVal(card)
				if 'chapel' in legal_actions:
					good_trashes = 0
					for card in ['copper', 'curse', 'estate']:
						good_trashes += hand[card] + deck[card] + discard[card] + in_play[card]
					legal_actions['chapel'] = good_trashes * 2

				for card in legal_actions:
					if legal_actions[card] == max(legal_actions.values()):
						return card

	def chapel(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		self.phase = 'chapel'
		total_coin = 0
		total_coin += hand['copper'] + discard['copper'] + deck['copper'] + in_play['copper']
		total_coin += (hand['silver'] + discard['silver'] + deck['silver'] + in_play['silver']) * 2
		total_coin += (hand['gold'] + discard['gold'] + deck['gold'] + in_play['gold']) * 3
		total_coin += (hand['militia'] + discard['militia'] + deck['militia'] + in_play['militia']) * 2

		to_trash = []
		legal_trash = {}
		for card in card_map:
			if hand[card] > 0:
				legal_trash[card] = self.getVal(card)
		for card in legal_trash:
			if card in ['copper', 'estate', 'curse']:
				for i in range(hand[card]):
					if card == 'copper':
						if total_coin > 3:
							to_trash.append(card)
							total_coin -= 1
					else:
						to_trash.append(card)		
		return to_trash

	def militia(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		self.phase = 'militia'
		self.card_map = card_map
		self.deck = deck
		self.hand = copy.deepcopy(hand)
		self.discard = discard
		self.coin = coin
		self.actions = actions
		self.buys = buys
		self.in_play = in_play
		self.trash = trash
		self.attack_immune = attack_immune
		self.player = player
		to_disc = []
		legal_disc = {}
		for card in card_map:
			if hand[card] > 0:
				legal_disc[card] = self.getVal(card)
		while len(to_disc) < sum(self.hand.values()) - 3:
			for card in legal_disc:
				if legal_disc[card] == min(legal_disc.values()):
					if hand[card] > 0:
						to_disc.append(card)
						hand[card] -= 1
					else:
						legal_disc[card] = 10000
		return to_disc

	def remodel(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
		return none

	def workshop(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
		return 'gardens'



class BigMoney(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Big Money with Witch'

	def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):


		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['province'] = 17 - provinces_remaining + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02
		priority_list['witch'] = provinces_remaining + 4 - (hand['witch'] + discard['witch'] + deck['witch'] + in_play['witch'])


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card


		return 'nobuy'

class MilitiaBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Militia Bot'

	def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		num_actions = 0 
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
			if 'action' in card_map[card]['types']:
				num_actions += hand[card] + discard[card] + deck[card] + in_play[card]
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['province'] = 17 - provinces_remaining + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02
		priority_list['militia'] = provinces_remaining + 3 - .5 * num_actions


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		return 'militia'

class MoatBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Moat Bot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		num_actions = 0 
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
			if 'action' in card_map[card]['types']:
				num_actions += hand[card] + discard[card] + deck[card] + in_play[card]
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['province'] = 17 - provinces_remaining + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02
		priority_list['moat'] = provinces_remaining - num_actions


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		return 'moat'

class CouncilBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Council Bot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		num_actions = 0 
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
			if 'action' in card_map[card]['types']:
				num_actions += hand[card] + discard[card] + deck[card] + in_play[card]
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['province'] = 17 - provinces_remaining + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02
		priority_list['council_room'] = provinces_remaining + 4 - num_actions


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		return 'council_room'

class WorkshopBot(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Workshop Bot'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		provinces_remaining = card_map['province']['supply']
		num_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values())
		num_actions = 0 
		total_coin = 0

		for card in card_map:
			total_coin += (hand[card] + discard[card] + deck[card] + in_play[card]) * card_map[card]['coin']
			if 'action' in card_map[card]['types']:
				num_actions += hand[card] + discard[card] + deck[card] + in_play[card]
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()))
		priority_list = {}

		priority_list['silver'] = provinces_remaining + 2.01
		priority_list['gold'] = provinces_remaining + 3.01
		priority_list['province'] = 17 - provinces_remaining + average_coin * 1.4
		priority_list['duchy'] = 11 - provinces_remaining
		priority_list['estate'] = 5 - provinces_remaining
		priority_list['nobuy'] = provinces_remaining - 2.02
		priority_list['workshop'] = provinces_remaining + 3 - num_actions * .5


		for card in priority_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		return 'workshop'

	def workshop(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		num_actions = 0
		for card in card_map:
			if 'action' in card_map[card]['types']:
				num_actions += hand[card] + discard[card] + deck[card] + in_play[card]
		if num_actions < 2:
			return 'workshop'
		else:
			return 'silver'

class WorkshopAggro(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Workshop AggroBot'

	def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		num_workshops = hand['workshop'] + deck['workshop'] + discard['workshop'] + in_play['workshop']
		num_villages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		priority_list = {}

		priority_list['province'] = 18
		priority_list['workshop'] = 11.1 - num_workshops + num_villages 
		priority_list['village'] = 10
		priority_list['duchy'] = 8
		priority_list['gardens'] = 9
		priority_list['estate'] = 7
		priority_list['gold'] = 6
		priority_list['silver'] = 5


		for card in priority_list:
			if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
				priority_list[card] = -999
		for card in priority_list:
			if priority_list[card] == max(list(priority_list.values())):
				return card

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		if hand['village'] > 0:
			return 'village'
		else:
			return 'workshop'

	def workshop(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, attack_immune, player):
		if card_map['village']['supply'] > 0:
			return 'village'
		elif card_map['workshop']['supply'] > 0:
			return 'workshop'
		else:
			return 'gardens'

class HolyWitch(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Holy Witch w3'

	def action(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):
		if hand['village'] > 0:
			return 'village'
			
		if hand['witch'] > 0:
			return 'witch'

		if hand['chapel'] > 0:
			return 'chapel'

	def buy(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

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

	def chapel(self, card_map, deck, hand, discard, coin, actions, buys, in_play, trash, attack_immune, player):

		self.phase = 'chapel'
		total_coin = 0
		total_coin += hand['copper'] + discard['copper'] + deck['copper'] + in_play['copper']
		total_coin += (hand['silver'] + discard['silver'] + deck['silver'] + in_play['silver']) * 2
		total_coin += (hand['gold'] + discard['gold'] + deck['gold'] + in_play['gold']) * 3
		total_coin += (hand['militia'] + discard['militia'] + deck['militia'] + in_play['militia']) * 2

		to_trash = []
		for card in card_map:
			if card in ['copper', 'estate', 'curse']:
				for i in range(hand[card]):
					if card == 'copper':
						if total_coin > 3:
							to_trash.append(card)
							total_coin -= 1
					else:
						to_trash.append(card)		
		return to_trash