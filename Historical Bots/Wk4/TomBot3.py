import BaseBot
import math

class TomBot3(BaseBot.BaseBot):

	def __init__ (self):

		self.name = 'Pun BOT 420'
		self.mode = 0 # 0 is chapel, witch, money
									# 1 is gardens militia, workshop

	def workshop(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player):
		myProvinces = hand['province'] + deck['province'] + discard['province']
		myDuchies = hand['duchy'] + deck['duchy'] + discard['duchy']
		myEstates = hand['estate'] + deck['estate'] + discard['estate']
		myCurses = hand['curse'] + deck['curse'] + discard['curse']
		myGardens = hand['gardens'] + deck['gardens'] + discard['gardens']

		myGold = hand['gold'] + deck['gold'] + discard['gold']
		mySilver = hand['silver'] + deck['silver'] + discard['silver']
		myCopper = hand['copper'] + deck['copper'] + discard['copper']

		myWitches = hand['witch'] + deck['witch'] + discard['witch'] + in_play['witch']
		myChapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		myMilitia = hand['militia'] + deck['militia'] + discard['militia'] + in_play['militia']
		myWorkshop = hand['workshop'] + deck['workshop'] + discard['workshop'] + in_play['workshop']
		myWorkshop = hand['workshop'] + deck['workshop'] + discard['workshop'] + in_play['workshop']

		totalCards = myProvinces + myDuchies + myEstates + myCurses + myGold + mySilver + myCopper + myWitches + myMilitia + myWorkshop + myChapels + myGardens

		if myWorkshop <= (totalCards/10) and myWorkshop < 3:
			return 'workshop'
		if card_map['gardens']['supply'] > 0:
			return 'gardens'
		return 'estate'

	def militia(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player):

		actionNames = []
		for i in range(hand['witch']):
			actionNames.append('witch')
		for i in range(hand['chapel']):
			actionNames.append('chapel')
		for i in range((hand['militia'])):
			actionNames.append('militia')
		for i in range((hand['workshop'])):
			actionNames.append('workshop')

		wouldBeAction = self.action(card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player)
		if wouldBeAction != 'poop':
			actionNames.remove(wouldBeAction)

		vpCards = hand['province'] + hand['duchy'] + hand['estate'] + hand['curse'] + hand['gardens']
		vpCards = []
		for i in range((hand['province'])):
			vpCards.append('province')
		for i in range((hand['duchy'])):
			vpCards.append('duchy')
		for i in range((hand['estate'])):
			vpCards.append('estate')
		for i in range((hand['curse'])):
			vpCards.append('curse')
		for i in range((hand['gardens'])):
			vpCards.append('gardens')

		while True:
			if wouldBeAction == 'chapel' and hand['chapel'] > 0 and hand['curse'] > 0 and 'curse' in vpCards:
				vpCards.remove('curse')
			else:
				break

		coinCards = []
		for i in range((hand['copper'])):
			coinCards.append('copper')
		for i in range((hand['silver'])):
			coinCards.append('silver')
		for i in range((hand['gold'])):
			coinCards.append('gold')


		discards = []
		while len(discards) < 2:
			if len(actionNames) >= 2:
				discards = [actionNames[0], actionNames[1]]
				actionNames = []
				continue
			if len(actionNames) == 1:
				discards.append(actionNames[0])
				actionNames = []
				continue
			if len(vpCards) >= 2:
				discards = [vpCards[0], vpCards[1]]
				vpCards = []
				continue
			if len(vpCards) == 1:
				discards.append(vpCards[0])
				vpCards = []
				continue
			discards.append(coinCards[0])
			coinCards.remove(coinCards[0])
		#print("HELLO")
		#print(discards)
		return discards


	def action(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player):

		EmptyPiles = 0
		for card in card_map:
			if card_map[card]['supply'] == 0:
				EmptyPiles += 1

		if self.mode == 0:
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
				choice = self.buy(card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player)
				choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, buys, in_play, trash, immune, player)
				while extraMoney < 3:
					if (choice == choice1):
						extraMoney += 1
						choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, buys, in_play, trash, immune, player)
					else:
						break
				chapelValue = hand['curse'] + min(extraMoney, hand['copper'])
				
				if EmptyPiles < 2 and card_map['province']['supply'] > 4:
					chapelValue += hand['estate']
				
				sameBuy = self.buy(card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player) == self.buy(card_map, deck, hand, discard, bonus_coin+2, actions, buys, in_play, trash, immune, player)
				if (chapelValue > 1 or hand['curse'] > 0 or sameBuy):
					return 'chapel'
				else:
					return 'witch'
		if self.mode == 1:
			if hand['workshop'] > 0:
				return 'workshop'
			if hand['militia'] > 0:
				return 'militia'
		return 'poop'

	def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player):
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
		choice = self.buy(card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player)
		choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, buys, in_play, trash, immune, player)
		while extraMoney<3:
			if (choice == choice1):
				extraMoney += 1
				choice1 = self.buy(card_map, deck, hand, discard, bonus_coin-(extraMoney+1), actions, buys, in_play, trash, immune, player)
			else:
				break
		for i in range(min(extraMoney, hand['copper'])):
			trashes.append('copper')

		return trashes


	def buy(self, card_map, deck, hand, discard, bonus_coin, actions, buys, in_play, trash, immune, player):

		coin = bonus_coin
		

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
		myChapels = hand['chapel'] + deck['chapel'] + discard['chapel'] + in_play['chapel']
		myMilitia = hand['militia'] + deck['militia'] + discard['militia'] + in_play['militia']
		myWorkshop = hand['workshop'] + deck['workshop'] + discard['workshop'] + in_play['workshop']

		actionsInHand = hand['witch'] + hand['chapel'] + hand['militia'] + hand['workshop']

		myActionCards = myWitches + myChapels + myMilitia + myWorkshop
		totalCards = myProvinces + myDuchies + myEstates + myCurses + myGold + mySilver + myCopper + myWitches + myMilitia + myWorkshop + myChapels + myGardens

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
			self.mode = 0
			return 'witch'
		if (totalCards < 12 and coin == 2 and myChapels < 1 and ('chapel' in buys)):
			self.mode = 0
			return 'chapel'
		# if 4-3 buy workshop, militia
		if (totalCards < 12 and coin == 4 and ('silver' in buys)):
			self.mode = 1
			return 'workshop'
		if (totalCards < 12 and coin == 3 and myChapels < 1 and ('chapel' in buys)):
			self.mode = 1
			return 'silver'

		if self.mode == 0:

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

		if self.mode == 1:
			if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 0) and (VPs > -3):
				return 'duchy'
			if (EmptyPiles == 2) and (card_map['duchy']['supply'] == 1) and ('duchy' in buys) and (player == 1) and (VPs >= -3):
				return 'duchy'
			if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 0) and (VPs > -1):
				return 'estate'
			if (EmptyPiles == 2) and (card_map['estate']['supply'] == 1) and ('estate' in buys) and (player == 1) and (VPs >= -1):
				return 'estate'

			if ('province' in buys):
				return 'province'

			if provinces > 5 and 'gold' in buys:
				return 'gold'

			if 'duchy' in buys:
				return 'duchy'

			if myWorkshop <= (totalCards/10) and myWorkshop < 3 and ('workshop' in buys) and provinces > 4 and 'workshop' in buys:
				return 'workshop'

			if 'silver' in buys and provinces == 8 and totalCards < 25 and EmptyPiles == 0:
				return 'silver'
			if 'gardens' in buys:
				return 'gardens'

			if (EmptyPiles > 0 or card_map['province']['supply'] < 3) and 'estate' in buys:
				return 'estate'

			if 'silver' in buys:
				return 'silver'

			if 'estate' in buys:
				return 'estate'
			if 'copper' in buys:
				return 'copper'

			else:
				return 'nobuy'

