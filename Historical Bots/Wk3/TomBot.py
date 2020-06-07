import BaseBot
import math

class TomBot2PointOh(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Celi-BOT'

	def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		EmptyPiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				EmptyPiles += 1

		if (hand['village'] > 0):
			return 'village'
		if (actions > 1):
			if (hand['witch'] > 0):
				return 'witch'
		if (hand['witch'] > 0 and hand['chapel'] == 0):
			return 'witch'
		if (hand['chapel'] > 0 and hand['witch'] == 0):
			return 'chapel'


		if (hand['chapel'] > 0 and hand['witch'] > 0):
			if hand['curse'] == 0 and (EmptyPiles == 2 or card_map['province']['supply'] <=2):
				return 'witch'

			extraMoney = 0
			choice = self.buy(card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player)
			choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, in_play, trash, player)
			while extraMoney < 3:
				if (choice == choice1):
					extraMoney += 1
					choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, in_play, trash, player)
				else:
					break
			chapelValue = hand['curse'] + min(extraMoney, hand['copper'])
			
			if EmptyPiles < 2 and card_map['province']['supply'] > 4:
				chapelValue += hand['estate']
			
			sameBuy = self.buy(card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player) == self.buy(card_map, deck, hand, discard, bonus_coin+2, actions, in_play, trash, player)
			if (chapelValue > 1 or hand['curse'] > 0 or sameBuy):
				return 'chapel'
			else:
				return 'witch'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):
		# If cards are erroneously returned, nothing will be trashed. If some of the cards are
		# erroneous but some are correct, the correct returns will still be trashed.
		EmptyPiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				EmptyPiles += 1
		trashes = []
		for i in range(hand['curse']):
			trashes.append('curse')
		if EmptyPiles == 2 or card_map['province']['supply'] <=2:
			return trashes

		if EmptyPiles < 2 and card_map['province']['supply'] > 4:
			for i in range(hand['estate']):
				trashes.append('estate')

		extraMoney = 0
		choice = self.buy(card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player)
		choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, in_play, trash, player)
		while extraMoney<3:
			if (choice == choice1):
				extraMoney += 1
				choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, in_play, trash, player)
			else:
				break
		for i in range(min(extraMoney, hand['copper'])):
			trashes.append('copper')

		return trashes


	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

		coin = self.get_coin(card_map, hand, bonus_coin)
		

		buys = []
		for card in card_map:
			if (coin >= card_map[card]['cost']) and card_map[card]['supply'] > 0:
				buys.append(card)

		
		provinces = card_map['province']['supply']
		duchies = card_map['duchy']['supply']
		estates = card_map['estate']['supply']
		curses = card_map['curse']['supply']
		gardens = card_map['gardens']['supply']

		myProvinces = hand['province'] + deck['province'] + discard['province']
		myDuchies = hand['duchy'] + deck['duchy'] + discard['duchy']
		myEstates = hand['estate'] + deck['estate'] + discard['estate']
		myCurses = hand['curse'] + deck['curse'] + discard['curse']
		myGardens = hand['gardens'] + deck['gardens'] + discard['gardens']
		myVPs = (myProvinces*6) + (myDuchies*3) + myEstates - myCurses

		oppProvinces = 8 - provinces - myProvinces
		oppDuchies = 8 - duchies - myDuchies
		oppEstates = 8 - estates - myEstates
		oppCurses = 10 - curses - myCurses
		oppGardens = 8 - gardens - myGardens
		oppVPs = (oppProvinces*6) + (oppDuchies*3) + oppEstates - oppCurses + oppGardens*3

		VPs = myVPs - oppVPs

		myGold = hand['gold'] + deck['gold'] + discard['gold']
		mySilver = hand['silver'] + deck['silver'] + discard['silver']
		myCopper = hand['copper'] + deck['copper'] + discard['copper']

		myWitches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']
		myVillages = hand['village'] + deck['village'] + discard['village'] + in_play['village']
		myChapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']


		myActionCards = myWitches + myVillages + myChapels
		totalCards = myProvinces + myDuchies + myEstates + myCurses + myGold + mySilver + myCopper + myWitches + myVillages + myChapels + myGardens

		myVPs = (myProvinces*6) + (myDuchies*3) + myEstates - myCurses + math.floor(totalCards/10)*myGardens


		EmptyPiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				EmptyPiles += 1

		OnePiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 1:
				OnePiles += 1

		# if 5-2 buy witch, chapel
		if (totalCards < 12 and coin == 5 and ('witch' in buys)):
			return 'witch'
		if (totalCards < 12 and coin == 2 and myChapels < 1 and ('chapel' in buys)):
			return 'chapel'
		# if 4-3 buy silver, chapel
		if (totalCards < 12 and coin == 4 and ('silver' in buys)):
			return 'silver'
		if (totalCards < 12 and coin == 3 and myChapels < 1 and ('chapel' in buys)):
			return 'chapel'

		if card_map['witch']['supply'] >= 6 and coin in [5,6,7] and myWitches == 0:
			return 'witch' 
		if card_map['witch']['supply'] >= 6 and coin == 5 and myWitches <= 1:
			return 'witch'


		if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 0) and (VPs > -3):
			return 'duchy'
		if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 1) and (VPs >= -3):
			return 'duchy'
		if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 0) and (VPs > -1):
			return 'estate'
		if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 1) and (VPs >= -1):
			return 'estate'

		if (provinces > 4) and (myGold > 1) and ('province' in buys):
			return 'province'
		if (provinces == 5) and ('duchy' in buys):
			return 'duchy'
		if (provinces > 4) and ('gold' in buys):
			return 'gold'
		if (provinces > 4) and ('silver' in buys):
			return 'silver'
		if (provinces in [4,3]) and ('province' in buys):
			return 'province'
		if (provinces in [4,3]) and ('duchy' in buys):
			return 'duchy'
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
		if (provinces == 1) and ('silver' in buys):
			return 'silver'

		else:
			return 'nobuy'


