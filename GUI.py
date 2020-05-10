from tkinter import *
from PIL import ImageTk, Image
import time

class CreateGUI:

	def __init__(
			self, 
			p1_move_list, 
			p2_move_list, 
			p1_hand_list, 
			p2_hand_list, 
			p1_extra_draw, 
			p2_extra_draw,
			p1_remodel_text,
			p2_remodel_text,
			bot1_name, 
			bot2_name,
			winner):

		self.iter = 0
		self.supply = [45, 30, 30, 8, 8, 8, 10, 10, 10, 10]
		self.hands = [[-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]]
		self.winner = winner

		self.move = [[0, 'none', 'none'], [0, 'none','none']]
		self.move_list = [p1_move_list, p2_move_list]
		self.hand_list = [p1_hand_list, p2_hand_list]
		self.extra_hand_list = [p1_extra_draw, p2_extra_draw]
		self.extra_i = [0, 0]
		self.bot_name = [bot1_name, bot2_name]
		self.remodel_text = [p1_remodel_text, p2_remodel_text]
		self.rem_i = 0
		self.is_rem = False

		self.root = Tk()
		self.canvas = Canvas(self.root, width = 900, height = 900)
		self.canvas.pack()
		self.canvas.config(bg='linen')
		self.card_names = [
			'copper',
			'silver',
			'gold',
			'estate',
			'duchy',
			'province',
			'curse',
			'moneylender',
			'remodel',
			'smithy'
		]

		self.img_paths = {
			'copper': '/Users/jdobrow/Code/DominionAI/Card Images/copper.jpeg',
			'silver': '/Users/jdobrow/Code/DominionAI/Card Images/silver.jpg',
			'gold': '/Users/jdobrow/Code/DominionAI/Card Images/gold.jpg',
			'estate': '/Users/jdobrow/Code/DominionAI/Card Images/estate.jpg',
			'duchy': '/Users/jdobrow/Code/DominionAI/Card Images/duchy.jpg',
			'province': '/Users/jdobrow/Code/DominionAI/Card Images/province.jpg',
			'curse': '/Users/jdobrow/Code/DominionAI/Card Images/curse.jpg',
			'none': '/Users/jdobrow/Code/DominionAI/Card Images/None.png',
			'moneylender' : '/Users/jdobrow/Code/DominionAI/Card Images/moneylender.jpeg',
			'remodel': '/Users/jdobrow/Code/DominionAI/Card Images/Remodel.jpg', 
			'smithy': '/Users/jdobrow/Code/DominionAI/Card Images/smithy.jpg'
		}

		hand_copper = self.create_image(self.img_paths['copper'], 80, 128)
		hand_silver = self.create_image(self.img_paths['silver'], 80, 128)
		hand_gold = self.create_image(self.img_paths['gold'], 80, 128)
		hand_estate = self.create_image(self.img_paths['estate'], 80, 128)
		hand_duchy = self.create_image(self.img_paths['duchy'], 80, 128)
		hand_province = self.create_image(self.img_paths['province'], 80, 128)
		hand_curse = self.create_image(self.img_paths['curse'], 80, 128)
		hand_moneylender = self.create_image(self.img_paths['moneylender'], 80, 128)
		hand_remodel = self.create_image(self.img_paths['remodel'], 80, 128)
		hand_smithy = self.create_image(self.img_paths['smithy'], 80, 128)
		hand_none = self.create_image(self.img_paths['none'], 80, 128)
		self.hand_img = {
			0:hand_copper,
			1:hand_silver,
			2:hand_gold,
			3:hand_estate,
			4:hand_duchy,
			5:hand_province,
			6:hand_curse,
			7:hand_moneylender,
			8:hand_remodel,
			9:hand_smithy,
			-1:hand_none
		}

		sup_copper = self.create_image(self.img_paths['copper'], 40, 64)
		sup_silver = self.create_image(self.img_paths['silver'], 40, 64)
		sup_gold = self.create_image(self.img_paths['gold'], 40, 64)
		sup_estate = self.create_image(self.img_paths['estate'], 40, 64)
		sup_duchy = self.create_image(self.img_paths['duchy'], 40, 64)
		sup_province = self.create_image(self.img_paths['province'], 40, 64)
		sup_curse = self.create_image(self.img_paths['curse'], 40, 64)
		sup_moneylender = self.create_image(self.img_paths['moneylender'], 40, 64)
		sup_remodel = self.create_image(self.img_paths['remodel'], 40, 64)
		sup_smithy = self.create_image(self.img_paths['smithy'], 40, 64)
		self.sup_img = {
			'copper': sup_copper,
			'silver': sup_silver,
			'gold': sup_gold,
			'estate': sup_estate,
			'duchy': sup_duchy,
			'province': sup_province,
			'curse': sup_curse,
			'moneylender': sup_moneylender,
			'remodel': sup_remodel,
			'smithy': sup_smithy
		}

		purchase_copper = self.create_image(self.img_paths['copper'], 125, 200)
		purchase_silver = self.create_image(self.img_paths['silver'], 125, 200)
		purchase_gold = self.create_image(self.img_paths['gold'], 125, 200)
		purchase_duchy = self.create_image(self.img_paths['duchy'], 125, 200)
		purchase_province = self.create_image(self.img_paths['province'], 125, 200)
		purchase_estate = self.create_image(self.img_paths['estate'], 125, 200)
		purchase_curse = self.create_image(self.img_paths['curse'], 125, 200)
		purchase_none = self.create_image(self.img_paths['none'], 125, 200)
		purchase_moneylender = self.create_image(self.img_paths['moneylender'], 125, 200)
		purchase_remodel = self.create_image(self.img_paths['remodel'], 125, 200)
		purchase_smithy = self.create_image(self.img_paths['smithy'], 125, 200)
		self.purchase_img = {
			'copper': purchase_copper,
			'silver': purchase_silver,
			'gold': purchase_gold,
			'estate': purchase_estate,
			'duchy': purchase_duchy,
			'province': purchase_province,
			'curse': purchase_curse,
			'none': purchase_none,
			'moneylender': purchase_moneylender,
			'remodel': purchase_remodel,
			'smithy': purchase_smithy
		}
		self.logo = self.create_image('/Users/jdobrow/Code/DominionAI/Card Images/Battle Bots Logo.jpg', 340, 125)

		self.active = True
		self.create_supply()
		self.root.after(2500, lambda: self.move_active())
		self.root.after(300000, lambda: self.canvas.destroy())
		self.root.mainloop()

	def update(self, hand, moves, player):
		new_hand = [0, 0, 0, 0, 0, 0, 0]
		cards_added = 0
		j = 0
		if moves[1] == 'smithy':
			hand = list(self.extra_hand_list[player][self.extra_i[player]].values())
			self.extra_i[player] += 1
		while cards_added < 7:
			if hand[j] > 0:
				new_hand[cards_added] = j
				hand[j] -= 1
				cards_added += 1
			else:
				j += 1
				if j > 9:
					new_hand[5], new_hand[6] = -1, -1
					cards_added = 7
		hand = new_hand
		for i in range(10):
			if self.card_names[i] == moves[2]:
				self.supply[i] -= 1
		if moves[2] not in self.card_names:
			moves[2] = 'none'
		if moves[1] not in self.card_names:
			moves[1] = 'none'

		if moves[1] == 'remodel':
			self.hands[player][0] = hand[0]
			self.hands[player][1] = hand[1]
			self.hands[player][2] = hand[2]
			self.hands[player][3] = hand[3]
			self.hands[player][4] = hand[4]
			self.hands[player][5] = -1
			self.hands[player][6] = -1
			self.move[player] = moves
			self.rem_trash = self.remodel_text[player][self.rem_i][0]
			self.rem_gain = self.remodel_text[player][self.rem_i][1]
			print(self.rem_trash)
			print(self.rem_gain)
			self.rem_i += 1
			self.is_rem = True

		elif moves[1] not in ['smithy']:
			self.hands[player][0] = hand[0]
			self.hands[player][1] = hand[1]
			self.hands[player][2] = hand[2]
			self.hands[player][3] = hand[3]
			self.hands[player][4] = hand[4]
			self.hands[player][5] = -1
			self.hands[player][6] = -1
			self.move[player] = moves
			self.is_rem = False

		else:
			self.hands[player][0] = hand[0]
			self.hands[player][1] = hand[1]
			self.hands[player][2] = hand[2]
			self.hands[player][3] = hand[3]
			self.hands[player][4] = hand[4]
			self.hands[player][5] = hand[5]
			self.hands[player][6] = hand[6]
			self.move[player] = moves
			self.is_rem = False

		self.create_supply()


	def move_active(self):
		if self.active:
			if self.iter % 2 == 0:
				self.update(self.hand_list[0][self.iter//2], self.move_list[0][self.iter//2], 0)
			else:
				self.update(self.hand_list[1][self.iter//2], self.move_list[1][self.iter//2], 1)
			self.iter += 1
		
			self.root.after(2500, self.move_active)

	def create_image(self, path, w, h):
		img = Image.open(path)
		img = img.resize((w, h), Image.ANTIALIAS)
		return ImageTk.PhotoImage(img)

	def create_supply(self):
		canvas = self.canvas
		canvas.delete("all")

		# Supply
		canvas.create_text(775, 40, text='Turn ' + str(self.iter), font=('Purisa', 30))
		canvas.create_text(775, 80, text='Supply', font=('Purisa', 20))
		canvas.create_text(610, 400, text='Buy', font=('Purisa', 30))
		canvas.create_text(190, 400, text='Action', font=('Purisa', 30))
		canvas.create_image(740, 100, anchor=NW, image=self.sup_img['copper'])
		canvas.create_image(740, 165, anchor=NW, image=self.sup_img['silver'])
		canvas.create_image(740, 230, anchor=NW, image=self.sup_img['gold'])
		canvas.create_image(740, 295, anchor=NW, image=self.sup_img['estate'])
		canvas.create_image(740, 360, anchor=NW, image=self.sup_img['duchy'])
		canvas.create_image(740, 425, anchor=NW, image=self.sup_img['province'])
		canvas.create_image(740, 490, anchor=NW, image=self.sup_img['curse'])
		canvas.create_image(740, 555, anchor=NW, image=self.sup_img['moneylender'])
		canvas.create_image(740, 620, anchor=NW, image=self.sup_img['remodel'])
		canvas.create_image(740, 685, anchor=NW, image=self.sup_img['smithy'])
		canvas.create_text(800, 135, text=str(self.supply[0]))
		canvas.create_text(800, 200, text=str(self.supply[1]))
		canvas.create_text(800, 265, text=str(self.supply[2]))
		canvas.create_text(800, 330, text=str(self.supply[3]))
		canvas.create_text(800, 395, text=str(self.supply[4]))
		canvas.create_text(800, 460, text=str(self.supply[5]))
		canvas.create_text(800, 525, text=str(self.supply[6]))
		canvas.create_text(800, 590, text=str(self.supply[7]))
		canvas.create_text(800, 655, text=str(self.supply[8]))
		canvas.create_text(800, 720, text=str(self.supply[9]))
		canvas.create_image(20, 785, anchor=NW, image=self.logo)
		if self.supply[5]  == 0:
			canvas.delete("all")
			self.canvas.create_text(400, 400, text='{} Wins!!!'.format(self.winner), font=('Purisa', 50))
		#p1 hand 1-5:
		canvas.create_text(80, 90, text=self.bot_name[0], font=('Purisa', 20))
		canvas.create_image(140, 20, anchor=NW, image=self.hand_img[self.hands[0][0]])
		canvas.create_image(220, 20, anchor=NW, image=self.hand_img[self.hands[0][1]])
		canvas.create_image(300, 20, anchor=NW, image=self.hand_img[self.hands[0][2]])
		canvas.create_image(380, 20, anchor=NW, image=self.hand_img[self.hands[0][3]])
		canvas.create_image(460, 20, anchor=NW, image=self.hand_img[self.hands[0][4]])
		canvas.create_image(540, 20, anchor=NW, image=self.hand_img[self.hands[0][5]])
		canvas.create_image(620, 20, anchor=NW, image=self.hand_img[self.hands[0][6]])

		#p2 hand 1-5:
		canvas.create_text(80, 690, text=self.bot_name[1], font=('Purisa', 20))
		canvas.create_image(140, 620, anchor=NW, image=self.hand_img[self.hands[1][0]])
		canvas.create_image(220, 620, anchor=NW, image=self.hand_img[self.hands[1][1]])
		canvas.create_image(300, 620, anchor=NW, image=self.hand_img[self.hands[1][2]])
		canvas.create_image(380, 620, anchor=NW, image=self.hand_img[self.hands[1][3]])
		canvas.create_image(460, 620, anchor=NW, image=self.hand_img[self.hands[1][4]])
		canvas.create_image(540, 620, anchor=NW, image=self.hand_img[self.hands[1][5]])
		canvas.create_image(620, 620, anchor=NW, image=self.hand_img[self.hands[1][6]])

		#p1 purchase
		self.canvas.create_image(250, 193, anchor=NW, image=self.purchase_img[self.move[0][1]])
		self.canvas.create_image(417, 193, anchor=NW, image=self.purchase_img[self.move[0][2]])

		#p2 purchase
		self.canvas.create_image(250, 407, anchor=NW, image=self.purchase_img[self.move[1][1]])
		self.canvas.create_image(417, 407, anchor=NW, image=self.purchase_img[self.move[1][2]])

		if self.is_rem == True:
			self.canvas.create_text(50, 380, text='Trash:', font=('Purisa', 15))
			self.canvas.create_text(50, 450, text='Gain:', font=('Purisa', 15))
			self.canvas.create_image(80, 350, anchor=NW, image=self.sup_img[self.rem_trash])
			self.canvas.create_image(80, 420, anchor=NW, image=self.sup_img[self.rem_gain])



