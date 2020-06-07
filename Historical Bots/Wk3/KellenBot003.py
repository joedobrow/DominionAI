import BaseBot

class KellenBot003(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'KellenBot003'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		my_copper = hand['copper'] + deck['copper'] + discard['copper'] + in_play['copper']
		my_silver = hand['silver'] + deck['silver'] + discard['silver'] + in_play['silver']
		my_gold = hand['gold'] + deck['gold'] + discard['gold'] + in_play['gold']
		my_curses = hand['curse'] + deck['curse'] + discard['curse'] + in_play['curse']
		my_estates = hand['estate'] + deck['estate'] + discard['estate'] + in_play['estate']
		my_duchies = hand['duchy'] + deck['duchy'] + discard['duchy'] + in_play['duchy']
		my_provinces = hand['province'] + deck['province'] + discard['province'] + in_play['province']
		my_gardens = hand['gardens'] + deck['gardens'] + discard['gardens'] + in_play['gardens']
		my_chapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		my_villages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		my_moneylenders = hand['moneylender'] + deck['moneylender'] + discard['moneylender'] + in_play['moneylender']
		my_remodels = hand['remodel'] + deck['remodel'] + discard['remodel'] + in_play['remodel']
		my_witches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']

		copper_remaining = card_map['copper']['supply']
		silver_remaining = card_map['silver']['supply']
		gold_remaining = card_map['gold']['supply']
		curses_remaining = card_map['curse']['supply']
		estates_remaining = card_map['estate']['supply']
		duchies_remaining = card_map['duchy']['supply']
		provinces_remaining = card_map['province']['supply']
		gardens_remaining = card_map['gardens']['supply']
		chapels_remaining = card_map['chapel']['supply']
		villages_remaining = card_map['village']['supply']
		moneylenders_remaining = card_map['moneylender']['supply']
		remodels_remaining = card_map['remodel']['supply']
		witches_remaining = card_map['witch']['supply']

		opp_copper = 46 - copper_remaining - my_copper - trash['copper'] + 14
		opp_silver = 40 - silver_remaining - my_silver - trash['silver']
		opp_gold = 30 - gold_remaining - my_gold - trash['gold']
		opp_curses = 10 - curses_remaining - my_curses - trash['curse']
		opp_estates = 8 - estates_remaining - my_estates - trash['estate'] + 6
		opp_duchies = 8 - duchies_remaining - my_duchies - trash['duchy']
		opp_provinces = 8 - provinces_remaining - my_provinces - trash['province']
		opp_gardens = 8 - gardens_remaining - my_gardens - trash['gardens']
		opp_chapels = 10 - chapels_remaining - my_chapels - trash['chapel']
		opp_villages = 10 - villages_remaining - my_villages - trash['village']
		opp_moneylenders = 10 - moneylenders_remaining - my_moneylenders - trash['moneylender']
		opp_remodels = 10 - remodels_remaining - my_remodels - trash['remodel']
		opp_witches = 10 - witches_remaining - my_witches - trash['witch']

		empty_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				empty_piles += 1

		one_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				one_piles += 1

		my_treasure_cards = my_copper + my_silver + my_gold
		my_vp_cards = my_curses + my_estates + my_duchies + my_provinces + my_gardens
		my_action_cards = my_chapels + my_villages + my_moneylenders + my_remodels + my_witches
		my_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())

		my_treasure_card_ratio = my_treasure_cards/my_cards
		my_vp_card_ratio = my_vp_cards/my_cards
		my_action_card_ratio = my_action_cards/my_cards

		opp_treasure_cards = opp_copper + opp_silver + opp_gold
		opp_vp_cards = opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens
		opp_action_cards = opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches
		opp_cards = opp_copper + opp_silver + opp_gold + opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens + opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches


		my_vps = (my_provinces*6) + (my_duchies*3) + (my_estates) + (my_gardens*(int(my_cards/10))) - (my_curses)
		opp_vps = (opp_provinces*6) + (opp_duchies*3) + (opp_estates) + (opp_gardens*(int(opp_cards/10))) - (opp_curses)
		vp_diff = my_vps - opp_vps

		coin = self.get_coin(card_map, hand, bonus_coin)

		hand_coin = (hand['gold']*3) + hand['silver']*2 + hand['copper']
		total_coin = 0
		for card in card_map:
			total_coin += ((hand[card] + discard[card] + deck[card])) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))

		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		
		deck_cards = 0
		for card in card_map:
			deck_cards += (deck[card] + discard[card])

		no_curses = 0
		if card_map['curse']['supply'] == 0:
			no_curses = 1
		# --------------------------------- ACTIONS -----------------------------------------------------------------

		action_list = {}
		for card in card_map:
			if (
				card in ['chapel', 'witch', 'remodel']
			):
				action_list[card] = 0

		action_list['chapel'] = provinces_remaining + (hand['curse']*2) + (hand['copper']*2) + (hand['estate']*2)
		action_list['witch'] = provinces_remaining + 3.5 - no_curses
		action_list['remodel'] = provinces_remaining + 3
		action_list['noaction'] = 1

		if provinces_remaining <= 4:
			action_list['chapel'] = provinces_remaining + (hand['curse']*2) + (hand['copper']*2)

		if (coin >= 8):
			action_list['witch'] = provinces_remaining + 2.5

		if deck_cards <2:
			action_list['witch'] = provinces_remaining + 1.5

		if (provinces_remaining == 1) and (hand['gold'] > 0):
			action_list['remodel'] = 90

		for card in action_list:
			if card != 'noaction':
				if (hand[card] == 0):
					action_list[card] = -1

		for card in action_list:
			if action_list[card] == max(list(action_list.values())):
				return card

		return 'noaction'

	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		my_copper = hand['copper'] + deck['copper'] + discard['copper'] + in_play['copper']
		my_silver = hand['silver'] + deck['silver'] + discard['silver'] + in_play['silver']
		my_gold = hand['gold'] + deck['gold'] + discard['gold'] + in_play['gold']
		my_curses = hand['curse'] + deck['curse'] + discard['curse'] + in_play['curse']
		my_estates = hand['estate'] + deck['estate'] + discard['estate'] + in_play['estate']
		my_duchies = hand['duchy'] + deck['duchy'] + discard['duchy'] + in_play['duchy']
		my_provinces = hand['province'] + deck['province'] + discard['province'] + in_play['province']
		my_gardens = hand['gardens'] + deck['gardens'] + discard['gardens'] + in_play['gardens']
		my_chapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		my_villages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		my_moneylenders = hand['moneylender'] + deck['moneylender'] + discard['moneylender'] + in_play['moneylender']
		my_remodels = hand['remodel'] + deck['remodel'] + discard['remodel'] + in_play['remodel']
		my_witches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']

		copper_remaining = card_map['copper']['supply']
		silver_remaining = card_map['silver']['supply']
		gold_remaining = card_map['gold']['supply']
		curses_remaining = card_map['curse']['supply']
		estates_remaining = card_map['estate']['supply']
		duchies_remaining = card_map['duchy']['supply']
		provinces_remaining = card_map['province']['supply']
		gardens_remaining = card_map['gardens']['supply']
		chapels_remaining = card_map['chapel']['supply']
		villages_remaining = card_map['village']['supply']
		moneylenders_remaining = card_map['moneylender']['supply']
		remodels_remaining = card_map['remodel']['supply']
		witches_remaining = card_map['witch']['supply']

		opp_copper = 46 - copper_remaining - my_copper - trash['copper'] + 14
		opp_silver = 40 - silver_remaining - my_silver - trash['silver']
		opp_gold = 30 - gold_remaining - my_gold - trash['gold']
		opp_curses = 10 - curses_remaining - my_curses - trash['curse']
		opp_estates = 8 - estates_remaining - my_estates - trash['estate'] + 6
		opp_duchies = 8 - duchies_remaining - my_duchies - trash['duchy']
		opp_provinces = 8 - provinces_remaining - my_provinces - trash['province']
		opp_gardens = 8 - gardens_remaining - my_gardens - trash['gardens']
		opp_chapels = 10 - chapels_remaining - my_chapels - trash['chapel']
		opp_villages = 10 - villages_remaining - my_villages - trash['village']
		opp_moneylenders = 10 - moneylenders_remaining - my_moneylenders - trash['moneylender']
		opp_remodels = 10 - remodels_remaining - my_remodels - trash['remodel']
		opp_witches = 10 - witches_remaining - my_witches - trash['witch']

		empty_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				empty_piles += 1

		one_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				one_piles += 1

		my_treasure_cards = my_copper + my_silver + my_gold
		my_vp_cards = my_curses + my_estates + my_duchies + my_provinces + my_gardens
		my_action_cards = my_chapels + my_villages + my_moneylenders + my_remodels + my_witches
		my_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())

		my_treasure_card_ratio = my_treasure_cards/my_cards
		my_vp_card_ratio = my_vp_cards/my_cards
		my_action_card_ratio = my_action_cards/my_cards

		opp_treasure_cards = opp_copper + opp_silver + opp_gold
		opp_vp_cards = opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens
		opp_action_cards = opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches
		opp_cards = opp_copper + opp_silver + opp_gold + opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens + opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches


		my_vps = (my_provinces*6) + (my_duchies*3) + (my_estates) + (my_gardens*(int(my_cards/10))) - (my_curses)
		opp_vps = (opp_provinces*6) + (opp_duchies*3) + (opp_estates) + (opp_gardens*(int(opp_cards/10))) - (opp_curses)
		vp_diff = my_vps - opp_vps

		coin = self.get_coin(card_map, hand, bonus_coin)

		hand_coin = (hand['gold']*3) + hand['silver']*2 + hand['copper']
		total_coin = 0
		for card in card_map:
			total_coin += ((hand[card] + discard[card] + deck[card])) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))

		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		# --------------------------------------------------------------------------------------------------

		if player == 0:
			if (empty_piles == 2) and (card_map['province']['supply'] == 1) and ('province' in buys) and (vp_diff >= -5):
				return 'province'
			if (empty_piles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (vp_diff >= -2):
				return 'duchy'
			if (empty_piles == 2) and (card_map['gardens']['supply'] == 1) and ('gardens' in buys) and (vp_diff >= -(int(my_cards/10)) + 1):
				return 'gardens'
			if (empty_piles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (vp_diff >= 0):
				return 'estate'
			if (empty_piles == 2) and (card_map['curse']['supply'] == 1) and ('curse' in buys) and (vp_diff >= 2):
				return 'curse'
			if (empty_piles == 2) and (card_map['copper']['supply'] == 1) and ('copper' in buys) and (vp_diff >= 1):
				return 'copper'
			if (empty_piles == 2) and (card_map['silver']['supply'] == 1) and ('silver' in buys) and (vp_diff >= 1):
				return 'silver'
			if (empty_piles == 2) and (card_map['gold']['supply'] == 1) and ('gold' in buys) and (vp_diff >= 1):
				return 'gold'
			if (empty_piles == 2) and (card_map['chapel']['supply'] == 1) and ('chapel' in buys) and (vp_diff >= 1):
				return 'chapel'
			if (empty_piles == 2) and (card_map['village']['supply'] == 1) and ('village' in buys) and (vp_diff >= 1):
				return 'village'
			if (empty_piles == 2) and (card_map['moneylender']['supply'] == 1) and ('moneylender' in buys) and (vp_diff >= 1):
				return 'moneylender'
			if (empty_piles == 2) and (card_map['remodel']['supply'] == 1) and ('remodel' in buys) and (vp_diff >= 1):
				return 'remodel'
			if (empty_piles == 2) and (card_map['witch']['supply'] == 1) and ('witch' in buys) and (vp_diff >= 1):
				return 'witch'


		if player == 1:	
			if (empty_piles == 2) and (card_map['province']['supply'] == 1) and ('province' in buys) and (vp_diff >= -6):
				return 'province'
			if (empty_piles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (vp_diff >= -3):
				return 'duchy'
			if (empty_piles == 2) and (card_map['gardens']['supply'] == 1) and ('gardens' in buys) and (vp_diff >= -(int(my_cards/10))):
				return 'gardens'
			if (empty_piles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (vp_diff >= -1):
				return 'estate'
			if (empty_piles == 2) and (card_map['curse']['supply'] == 1) and ('curse' in buys) and (vp_diff >= 1):
				return 'curse'
			if (empty_piles == 2) and (card_map['copper']['supply'] == 1) and ('copper' in buys) and (vp_diff >= 0):
				return 'copper'
			if (empty_piles == 2) and (card_map['silver']['supply'] == 1) and ('silver' in buys) and (vp_diff >= 0):
				return 'silver'
			if (empty_piles == 2) and (card_map['gold']['supply'] == 1) and ('gold' in buys) and (vp_diff >= 0):
				return 'gold'
			if (empty_piles == 2) and (card_map['chapel']['supply'] == 1) and ('chapel' in buys) and (vp_diff >= 0):
				return 'chapel'
			if (empty_piles == 2) and (card_map['village']['supply'] == 1) and ('village' in buys) and (vp_diff >= 0):
				return 'village'
			if (empty_piles == 2) and (card_map['moneylender']['supply'] == 1) and ('moneylender' in buys) and (vp_diff >= 0):
				return 'moneylender'
			if (empty_piles == 2) and (card_map['remodel']['supply'] == 1) and ('remodel' in buys) and (vp_diff >= 0):
				return 'remodel'
			if (empty_piles == 2) and (card_map['witch']['supply'] == 1) and ('witch' in buys) and (vp_diff >= 0):
				return 'witch'

		#first buy
		if (my_estates == 3) and (my_copper == 7) and (my_cards == 10):
			if (hand_coin == 2) and ('chapel' in buys):
				return 'chapel'
			if (hand_coin == 3) and ('chapel' in buys):
				return 'chapel'
			if (hand_coin == 4) and ('silver' in buys):
				return 'silver'
			if (hand_coin == 5) and ('witch' in buys):
				return 'witch'
			else:
				return 'nobuy'

		#second buy
		if (my_estates == 3) and (my_copper == 7) and (my_cards == 11):
			if (my_chapels == 1):
				if ('witch' in buys):
					return 'witch'
				elif ('silver' in buys):
					return 'silver'
			if (my_silver == 1): 
				if ('chapel' in buys):
					return 'chapel'
			if (my_witches == 1):
				if ('chapel' in buys):
					return 'chapel'
			else:
				return 'nobuy'


		buy_list = {}
		for card in card_map:
			if (
				card in ['copper', 'silver', 'gold', 'curse', 'estate', 'gardens', 'duchy', 'province', 'moneylender', 'village', 'remodel', 'witch'] and
				card_map[card]['cost'] <= coin and
				card_map[card]['supply'] > 0
			):
				buy_list[card] = 0

		buy_list['silver'] = provinces_remaining + 2.01
		buy_list['gold'] = provinces_remaining + 3.01
		buy_list['province'] = (18 - provinces_remaining) + my_gold
		buy_list['duchy'] = 11 - provinces_remaining
		buy_list['estate'] = 4 - provinces_remaining
		buy_list['witch'] = provinces_remaining + 3.5
		buy_list['remodel'] = 10.5 - provinces_remaining
		buy_list['nobuy'] = provinces_remaining - 1.02
		buy_list['copper'] = -2
		buy_list['curse'] = -2
		buy_list['chapel'] = -2
		buy_list['estate'] = -2
		buy_list['moneylender'] = -2
		buy_list['village'] = -2


		if my_witches >= 1:
			buy_list['witch'] = -2

		if my_gold == 0 or my_remodels >= 2:
			buy_list['remodel'] = -2

		if my_gold == 0:
			buy_list['duchy'] = -2
			buy_list['estate'] = -2

		if provinces_remaining <= 1:
			buy_list['province'] = 99
			buy_list['duchy'] = 98
			buy_list['gardens'] = 97
			buy_list['estate'] = 96
			buy_list['gold'] = 95
			buy_list['remodel'] = 94

		for card in buy_list:
			if card != 'nobuy':
				if (card_map[card]['cost'] > coin) or (card_map[card]['supply'] == 0):
					buy_list[card] = -2


		for card in buy_list:
			if buy_list[card] == max(buy_list.values()):
				return card

		return 'nobuy'

	def remodel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		my_copper = hand['copper'] + deck['copper'] + discard['copper'] + in_play['copper']
		my_silver = hand['silver'] + deck['silver'] + discard['silver'] + in_play['silver']
		my_gold = hand['gold'] + deck['gold'] + discard['gold'] + in_play['gold']
		my_curses = hand['curse'] + deck['curse'] + discard['curse'] + in_play['curse']
		my_estates = hand['estate'] + deck['estate'] + discard['estate'] + in_play['estate']
		my_duchies = hand['duchy'] + deck['duchy'] + discard['duchy'] + in_play['duchy']
		my_provinces = hand['province'] + deck['province'] + discard['province'] + in_play['province']
		my_gardens = hand['gardens'] + deck['gardens'] + discard['gardens'] + in_play['gardens']
		my_chapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		my_villages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		my_moneylenders = hand['moneylender'] + deck['moneylender'] + discard['moneylender'] + in_play['moneylender']
		my_remodels = hand['remodel'] + deck['remodel'] + discard['remodel'] + in_play['remodel']
		my_witches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']

		copper_remaining = card_map['copper']['supply']
		silver_remaining = card_map['silver']['supply']
		gold_remaining = card_map['gold']['supply']
		curses_remaining = card_map['curse']['supply']
		estates_remaining = card_map['estate']['supply']
		duchies_remaining = card_map['duchy']['supply']
		provinces_remaining = card_map['province']['supply']
		gardens_remaining = card_map['gardens']['supply']
		chapels_remaining = card_map['chapel']['supply']
		villages_remaining = card_map['village']['supply']
		moneylenders_remaining = card_map['moneylender']['supply']
		remodels_remaining = card_map['remodel']['supply']
		witches_remaining = card_map['witch']['supply']

		opp_copper = 46 - copper_remaining - my_copper - trash['copper'] + 14
		opp_silver = 40 - silver_remaining - my_silver - trash['silver']
		opp_gold = 30 - gold_remaining - my_gold - trash['gold']
		opp_curses = 10 - curses_remaining - my_curses - trash['curse']
		opp_estates = 8 - estates_remaining - my_estates - trash['estate'] + 6
		opp_duchies = 8 - duchies_remaining - my_duchies - trash['duchy']
		opp_provinces = 8 - provinces_remaining - my_provinces - trash['province']
		opp_gardens = 8 - gardens_remaining - my_gardens - trash['gardens']
		opp_chapels = 10 - chapels_remaining - my_chapels - trash['chapel']
		opp_villages = 10 - villages_remaining - my_villages - trash['village']
		opp_moneylenders = 10 - moneylenders_remaining - my_moneylenders - trash['moneylender']
		opp_remodels = 10 - remodels_remaining - my_remodels - trash['remodel']
		opp_witches = 10 - witches_remaining - my_witches - trash['witch']

		empty_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				empty_piles += 1

		one_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				one_piles += 1

		my_treasure_cards = my_copper + my_silver + my_gold
		my_vp_cards = my_curses + my_estates + my_duchies + my_provinces + my_gardens
		my_action_cards = my_chapels + my_villages + my_moneylenders + my_remodels + my_witches
		my_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())

		my_treasure_card_ratio = my_treasure_cards/my_cards
		my_vp_card_ratio = my_vp_cards/my_cards
		my_action_card_ratio = my_action_cards/my_cards

		opp_treasure_cards = opp_copper + opp_silver + opp_gold
		opp_vp_cards = opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens
		opp_action_cards = opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches
		opp_cards = opp_copper + opp_silver + opp_gold + opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens + opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches



		my_vps = (my_provinces*6) + (my_duchies*3) + (my_estates) + (my_gardens*(int(my_cards/10))) - (my_curses)
		opp_vps = (opp_provinces*6) + (opp_duchies*3) + (opp_estates) + (opp_gardens*(int(opp_cards/10))) - (opp_curses)
		vp_diff = my_vps - opp_vps

		coin = self.get_coin(card_map, hand, bonus_coin)

		hand_coin = (hand['gold']*3) + hand['silver']*2 + hand['copper']
		total_coin = 0
		for card in card_map:
			total_coin += ((hand[card] + discard[card] + deck[card])) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))

		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		# --------------------------------------------------------------------------------------------------

		if (provinces_remaining > 4):
			remodel_priorities = {
				'curse' : 'chapel',
				'remodel' : 'gold',
				'estate' : 'remodel',
				'copper' : 'chapel',
				'chapel' : 'remodel',
				'witch' : 'gold',
				'gold' : 'province',
			}
			for card in remodel_priorities:
				if hand[card] > 0 and card_map[remodel_priorities[card]]['supply'] > 0:
					return [card, remodel_priorities[card]]

		if provinces_remaining <=4:
			high_remodel_priorities = {
				'curse' : 'estate',
				'remodel' : 'duchy',
				'remodel' : 'gold',
				'gardens' : 'duchy',
				'gardens' : 'gold',
				'estate' : 'gardens',
				'chapel' : 'gardens',
			}
			low_remodel_priorities = {
				'province' : 'province',
				'duchy' : 'duchy',
			}
			if provinces_remaining ==1:
				high_remodel_priorities = {
					'remodel' : 'duchy',
					'witch' : 'duchy',
					'curse' : 'estate',
					'gardens' : 'duchy',
					'estate' : 'gardens',
					'chapel' : 'gardens',	
					'remodel' : 'gold',
				}

			if coin >= 11:
				if (hand['gold'] > 0):
					return ['gold', 'province']
			if coin == 10:
				if (hand['silver'] > 0):
					if (card_map['duchy']['supply'] >= 1):
						return ['silver', 'duchy']
				if (hand['gold'] > 0):
					if (card_map['duchy']['supply'] >= 1):
						return ['gold', 'province']
				if (hand['copper'] > 0):
					if (card_map['estate']['supply'] >= 1):
						return ['copper', 'estate']
			if coin == 9:
				if (hand['copper'] > 0):
					if (card_map['estate']['supply'] >= 1):
						return ['copper', 'estate']
				
				if (hand['silver'] == 3) and (hand['gold'] > 0):
					if (card_map['duchy']['supply'] >= 1):
						return ['gold', 'province']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]
			if coin == 8:
				
				if (hand['gold'] == 1) and (hand['silver'] == 2) and (hand['copper'] == 1):
					if (card_map['duchy']['supply'] >= 1):
						return ['gold', 'province']
				if (hand['gold'] == 2) and (hand['copper'] == 2):
					if (card_map['duchy']['supply'] >= 1):
						return ['gold', 'province']
				if (hand['gold'] == 2) and (hand['silver'] == 1):
					if (card_map['duchy']['supply'] >= 1):
						return ['gold', 'province']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]
			if coin == 7:
				
				if (hand['gold'] > 0):
					return ['gold', 'province']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				if (hand['silver'] == 3) and (hand['copper'] == 1):
					if (card_map['duchy']['supply'] >= 2):
						return ['silver', 'duchy']
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]
			if coin == 6:
				
				if (hand['gold'] > 0):
					return ['gold', 'province']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				if (hand['copper'] > 0):
					if (card_map['estate']['supply'] >= 1):
						return ['copper', 'estate']
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]
			if coin == 5:
				
				if (hand['gold'] > 0):
					return ['gold', 'province']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				if (hand['copper'] > 0):
					if (card_map['estate']['supply'] >= 1):
						return ['copper', 'estate']
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]
			if coin <= 4:
				
				if (hand['gold'] > 0):
					return ['gold', 'province']
				if (hand['silver'] > 0):
					if (card_map['duchy']['supply'] >= 1):
						return ['silver', 'duchy']
				for card in high_remodel_priorities:
					if hand[card] > 0 and card_map[high_remodel_priorities[card]]['supply'] > 0:
						return [card, high_remodel_priorities[card]]
				if (hand['copper'] > 0):
					if (card_map['estate']['supply'] >= 1):
						return ['copper', 'estate']
				for card in low_remodel_priorities:
					if hand[card] > 0 and card_map[low_remodel_priorities[card]]['supply'] > 0:
						return [card, low_remodel_priorities[card]]



	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		my_copper = hand['copper'] + deck['copper'] + discard['copper'] + in_play['copper']
		my_silver = hand['silver'] + deck['silver'] + discard['silver'] + in_play['silver']
		my_gold = hand['gold'] + deck['gold'] + discard['gold'] + in_play['gold']
		my_curses = hand['curse'] + deck['curse'] + discard['curse'] + in_play['curse']
		my_estates = hand['estate'] + deck['estate'] + discard['estate'] + in_play['estate']
		my_duchies = hand['duchy'] + deck['duchy'] + discard['duchy'] + in_play['duchy']
		my_provinces = hand['province'] + deck['province'] + discard['province'] + in_play['province']
		my_gardens = hand['gardens'] + deck['gardens'] + discard['gardens'] + in_play['gardens']
		my_chapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		my_villages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		my_moneylenders = hand['moneylender'] + deck['moneylender'] + discard['moneylender'] + in_play['moneylender']
		my_remodels = hand['remodel'] + deck['remodel'] + discard['remodel'] + in_play['remodel']
		my_witches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']

		copper_remaining = card_map['copper']['supply']
		silver_remaining = card_map['silver']['supply']
		gold_remaining = card_map['gold']['supply']
		curses_remaining = card_map['curse']['supply']
		estates_remaining = card_map['estate']['supply']
		duchies_remaining = card_map['duchy']['supply']
		provinces_remaining = card_map['province']['supply']
		gardens_remaining = card_map['gardens']['supply']
		chapels_remaining = card_map['chapel']['supply']
		villages_remaining = card_map['village']['supply']
		moneylenders_remaining = card_map['moneylender']['supply']
		remodels_remaining = card_map['remodel']['supply']
		witches_remaining = card_map['witch']['supply']

		opp_copper = 46 - copper_remaining - my_copper - trash['copper'] + 14
		opp_silver = 40 - silver_remaining - my_silver - trash['silver']
		opp_gold = 30 - gold_remaining - my_gold - trash['gold']
		opp_curses = 10 - curses_remaining - my_curses - trash['curse']
		opp_estates = 8 - estates_remaining - my_estates - trash['estate'] + 6
		opp_duchies = 8 - duchies_remaining - my_duchies - trash['duchy']
		opp_provinces = 8 - provinces_remaining - my_provinces - trash['province']
		opp_gardens = 8 - gardens_remaining - my_gardens - trash['gardens']
		opp_chapels = 10 - chapels_remaining - my_chapels - trash['chapel']
		opp_villages = 10 - villages_remaining - my_villages - trash['village']
		opp_moneylenders = 10 - moneylenders_remaining - my_moneylenders - trash['moneylender']
		opp_remodels = 10 - remodels_remaining - my_remodels - trash['remodel']
		opp_witches = 10 - witches_remaining - my_witches - trash['witch']

		empty_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				empty_piles += 1

		one_piles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				one_piles += 1

		my_treasure_cards = my_copper + my_silver + my_gold
		my_vp_cards = my_curses + my_estates + my_duchies + my_provinces + my_gardens
		my_action_cards = my_chapels + my_villages + my_moneylenders + my_remodels + my_witches
		my_cards = sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values())

		my_treasure_card_ratio = my_treasure_cards/my_cards
		my_vp_card_ratio = my_vp_cards/my_cards
		my_action_card_ratio = my_action_cards/my_cards

		opp_treasure_cards = opp_copper + opp_silver + opp_gold
		opp_vp_cards = opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens
		opp_action_cards = opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches
		opp_cards = opp_copper + opp_silver + opp_gold + opp_curses + opp_estates + opp_duchies + opp_provinces + opp_gardens + opp_chapels + opp_villages + opp_moneylenders + opp_remodels + opp_witches



		my_vps = (my_provinces*6) + (my_duchies*3) + (my_estates) + (my_gardens*(int(my_cards/10))) - (my_curses)
		opp_vps = (opp_provinces*6) + (opp_duchies*3) + (opp_estates) + (opp_gardens*(int(opp_cards/10))) - (opp_curses)
		vp_diff = my_vps - opp_vps

		coin = self.get_coin(card_map, hand, bonus_coin)

		hand_coin = (hand['gold']*3) + hand['silver']*2 + hand['copper']
		total_coin = 0
		for card in card_map:
			total_coin += ((hand[card] + discard[card] + deck[card])) * card_map[card]['coin']
		average_coin = total_coin/(sum(hand.values()) + sum(deck.values()) + sum(discard.values()) + sum(in_play.values()))

		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		# --------------------------------------------------------------------------------------------------

		chapel_map = {} 

		chapel_map['curse'] = 5 
		chapel_map['copper'] = -3 + total_coin 
		chapel_map['estate'] = -4 + provinces_remaining

		
		if coin >= 8 and provinces_remaining < 8:
			chapel_map['copper'] = coin - 8 

		chapel_list = []
		for card in chapel_map:
			for i in range(int(chapel_map[card])):
				chapel_list.append(card)
		return chapel_list
