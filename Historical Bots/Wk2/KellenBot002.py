import BaseBot

class KellenBot002(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'KellenBot002'

	def action(self, card_map, deck, hand, discard, bonus_coin, player):

		if (hand['smithy'] > 0):
			return 'smithy'
		else:
			return 'noaction'

	def buy(self, card_map, deck, hand, discard, bonus_coin, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		HandCoin = (hand['gold']*3) + (hand['silver']*2) + hand['copper']


		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		CardsInDeck = deck['gold'] + deck['silver'] + deck['copper'] + deck['province'] + deck['duchy'] + deck['estate'] + deck['curse'] + deck['moneylender'] + deck['smithy'] + deck['remodel']
		AvgCoinDraw = ((deck['gold']*3) + (deck['silver']*2) + deck['copper'])/(CardsInDeck + .001)

		provinces = card_map['province']['supply']
		duchies = card_map['duchy']['supply']
		estates = card_map['estate']['supply']

		MyProvinces = hand['province'] + deck['province'] + discard['province']
		MyDuchies = hand['duchy'] + deck['duchy'] + discard['duchy']
		MyEstates = hand['estate'] + deck['estate'] + discard['estate']
		MyVPs = (MyProvinces*6) + (MyDuchies*3) + MyEstates

		OppProvinces = provinces - MyProvinces
		OppDuchies = duchies - MyDuchies
		OppEstates = estates - MyEstates
		OppVPs = (OppProvinces*6) + (OppDuchies*3) + OppEstates

		VPs = MyVPs - OppVPs

		MyGold = hand['gold'] + deck['gold'] + discard['gold']
		MySilver = hand['silver'] + deck['silver'] + discard['silver']
		MyCopper = hand['copper'] + deck['copper'] + discard['copper']

		MyMoneylenders = hand['moneylender'] + deck['moneylender'] + discard['moneylender']
		MySmithies = hand['smithy'] + deck['smithy'] + discard['smithy']
		MyRemodels = hand['remodel'] + deck['remodel'] + discard['remodel']

		MyActionCards = MyMoneylenders + MySmithies + MyRemodels
		TotalCards = MyProvinces + MyDuchies + MyEstates + MyGold + MySilver + MyCopper + MyMoneylenders + MySmithies + MyRemodels
		ActionRatio = MyActionCards/TotalCards

		EmptyPiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				EmptyPiles += 1

		OnePiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				OnePiles += 1

		if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 0) and (VPs > -3):
			return 'duchy'
		if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 1) and (VPs >= -3):
			return 'duchy'
		if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 0) and (VPs > -1):
			return 'estate'
		if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 1) and (VPs >= -1):
			return 'estate'

		if (provinces > 4) and (MyGold > 1) and ('province' in buys):
			return 'province'
		if (provinces == 5) and ('duchy' in buys):
			return 'duchy'
		if (provinces > 4) and ('gold' in buys):
			return 'gold'
		if (provinces > 4) and (MySmithies == 0) and ('smithy' in buys):
			return 'smithy'
		if (provinces > 4) and (ActionRatio <=.052) and (MySmithies <= 1) and ('smithy' in buys):
			return 'smithy'
		if (provinces > 4) and ('silver' in buys):
			return 'silver'
		if (provinces in [4,3]) and ('province' in buys):
			return 'province'
		if (provinces == 4) and (CardsInDeck <= 3) and ('gold' in buys):
			return 'gold'
		if (provinces in [4,3]) and ('duchy' in buys):
			return 'duchy'
		if (provinces in [4,3]) and (ActionRatio <=.052) and (MySmithies <= 1) and ('smithy' in buys):
			return 'smithy'
		if (provinces in [4,3]) and ('gold' in buys):
			return 'gold'
		if (provinces in [4,3]) and ('silver' in buys):
			return 'silver'

		if (provinces == 2) and (VPs < -3 or VPs > 0) and (player == 0) and ('province' in buys):
			return 'province'
		if (provinces == 2) and (VPs <= -3 or VPs >= 0) and (player == 1) and ('province' in buys):
			return 'province'
		if (provinces == 2) and ('duchy' in buys):
			return 'duchy'
		if (provinces == 2) and ('province' in buys):
			return 'province'
		if (provinces == 2) and ('estate' in buys):
			return 'estate'
		if (provinces == 2) and ('gold' in buys):
			return 'gold'
		if (provinces == 2) and (ActionRatio <=.052) and (MySmithies <= 1) and ('smithy' in buys):
			return 'smithy'
		if (provinces == 2) and ('silver' in buys):
			return 'silver'

		if (provinces == 1) and (VPs > -6) and (player == 0) and ('province' in buys):
			return 'province'
		if (provinces == 1) and (VPs >= -6) and (player == 1) and ('province' in buys):
			return 'province'
		if (provinces == 1) and ('duchy' in buys):
			return 'duchy'
		if (provinces == 1) and ('estate' in buys):
			return 'estate'
		if (provinces == 1) and ('province' in buys):
			return 'province'
		if (provinces == 1) and ('gold' in buys):
			return 'gold'
		if (provinces == 1) and (ActionRatio <=.052) and (MySmithies <= 2) and ('smithy' in buys):
			return 'smithy'
		if (provinces == 1) and ('silver' in buys):
			return 'silver'

		else:
			return 'nobuy'

