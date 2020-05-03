from tkinter import *
from PIL import ImageTk, Image
import time

class CreateGUI:

	def __init__(self, p1_move_list, p2_move_list, p1_hand_list, p2_hand_list, bot1_name, bot2_name, winner):

		self.iter = 0
		self.supply = [45, 30, 30, 8, 8, 8, 8]
		self.p1_hand = [6, 6, 6, 6, 6]
		self.p2_hand = [6, 6, 6, 6, 6]
		self.winner = winner

		self.p1_move, self.p2_move = [0, 'copper'], [0, 'copper']
		self.p1_move_list, self.p2_move_list = p1_move_list, p2_move_list
		self.p1_hand_list, self.p2_hand_list = p1_hand_list, p2_hand_list
		self.bot1_name, self.bot2_name = bot1_name, bot2_name

		self.root = Tk()
		self.canvas = Canvas(self.root, width = 900, height = 900)
		self.canvas.pack()
		self.canvas.config(bg='linen')

		self.img_paths = {
			'copper': '/Users/jdobrow/Code/DominionAI/Card Images/copper.jpeg',
			'silver': '/Users/jdobrow/Code/DominionAI/Card Images/silver.jpg',
			'gold': '/Users/jdobrow/Code/DominionAI/Card Images/gold.jpg',
			'estate': '/Users/jdobrow/Code/DominionAI/Card Images/estate.jpg',
			'duchy': '/Users/jdobrow/Code/DominionAI/Card Images/duchy.jpg',
			'province': '/Users/jdobrow/Code/DominionAI/Card Images/province.jpg',
			'curse': '/Users/jdobrow/Code/DominionAI/Card Images/curse.jpg',
			'nobuy': '/Users/jdobrow/Code/DominionAI/Card Images/nobuy.png'
		}

		hand_copper = self.create_image(self.img_paths['copper'], 100, 160)
		hand_silver = self.create_image(self.img_paths['silver'], 100, 160)
		hand_gold = self.create_image(self.img_paths['gold'], 100, 160)
		hand_estate = self.create_image(self.img_paths['estate'], 100, 160)
		hand_duchy = self.create_image(self.img_paths['duchy'], 100, 160)
		hand_province = self.create_image(self.img_paths['province'], 100, 160)
		hand_curse = self.create_image(self.img_paths['curse'], 100, 160)
		self.hand_img = {
			0:hand_copper,
			1:hand_silver,
			2:hand_gold,
			3:hand_estate,
			4:hand_duchy,
			5:hand_province,
			6:hand_curse,
		}

		sup_copper = self.create_image(self.img_paths['copper'], 40, 64)
		sup_silver = self.create_image(self.img_paths['silver'], 40, 64)
		sup_gold = self.create_image(self.img_paths['gold'], 40, 64)
		sup_estate = self.create_image(self.img_paths['estate'], 40, 64)
		sup_duchy = self.create_image(self.img_paths['duchy'], 40, 64)
		sup_province = self.create_image(self.img_paths['province'], 40, 64)
		sup_curse = self.create_image(self.img_paths['curse'], 40, 64)
		self.sup_img = {
			'copper': sup_copper,
			'silver': sup_silver,
			'gold': sup_gold,
			'estate': sup_estate,
			'duchy': sup_duchy,
			'province': sup_province,
			'curse': sup_curse
		}

		purchase_copper = self.create_image(self.img_paths['copper'], 125, 200)
		purchase_silver = self.create_image(self.img_paths['silver'], 125, 200)
		purchase_gold = self.create_image(self.img_paths['gold'], 125, 200)
		purchase_duchy = self.create_image(self.img_paths['duchy'], 125, 200)
		purchase_province = self.create_image(self.img_paths['province'], 125, 200)
		purchase_estate = self.create_image(self.img_paths['estate'], 125, 200)
		purchase_curse = self.create_image(self.img_paths['curse'], 125, 200)
		purchase_nobuy = self.create_image(self.img_paths['nobuy'], 125, 200)
		self.purchase_img = {
			'copper': purchase_copper,
			'silver': purchase_silver,
			'gold': purchase_gold,
			'estate': purchase_estate,
			'duchy': purchase_duchy,
			'province': purchase_province,
			'curse': purchase_curse,
			'nobuy': purchase_nobuy
		}

		self.logo = self.create_image('/Users/jdobrow/Code/DominionAI/Card Images/Battle Bots Logo.jpg', 340, 125)

		self.active = True
		self.move_active()
		x = self.canvas.create_image(387, 193, anchor=NW, image=self.purchase_img[self.p1_move[1]])
		self.root.after(300000, lambda: self.canvas.destroy())
		self.root.mainloop()

	def update(self, hand, move, player):
		new_hand = [0, 0, 0, 0, 0]
		cards_added = 0
		j = 0
		while cards_added < 5:
			if hand[j] > 0:
				new_hand[cards_added] = j
				hand[j] -= 1
				cards_added += 1
			else:
				j += 1
		hand = new_hand
		for i in range(7):
			if list(self.img_paths.keys())[i] == move[1]:
				self.supply[i] -= 1
		if player == 1:
			self.p1_hand[0] = hand[0]
			self.p1_hand[1] = hand[1]
			self.p1_hand[2] = hand[2]
			self.p1_hand[3] = hand[3]
			self.p1_hand[4] = hand[4]
			self.p1_move = move
		else:
			self.p2_hand[0] = hand[0]
			self.p2_hand[1] = hand[1]
			self.p2_hand[2] = hand[2]
			self.p2_hand[3] = hand[3]
			self.p2_hand[4] = hand[4]
			self.p2_move = move
		self.create_supply()


	def move_active(self):
		if self.active:
			if self.iter % 2 == 0:
				self.update(self.p1_hand_list[self.iter//2], self.p1_move_list[self.iter//2], 1)
			else:
				self.update(self.p2_hand_list[self.iter//2], self.p2_move_list[self.iter//2], -1)
			self.iter += 1
		
			self.root.after(2000, self.move_active)

	def create_image(self, path, w, h):
		img = Image.open(path)
		img = img.resize((w, h), Image.ANTIALIAS)
		return ImageTk.PhotoImage(img)

	def create_supply(self):
		canvas = self.canvas
		canvas.delete("all")

		# Supply
		canvas.create_text(775, 100, text='Turn ' + str(self.iter), font=('Purisa', 30))
		canvas.create_text(775, 140, text='Supply', font=('Purisa', 20))
		canvas.create_image(740, 160, anchor=NW, image=self.sup_img['copper'])
		canvas.create_image(740, 230, anchor=NW, image=self.sup_img['silver'])
		canvas.create_image(740, 300, anchor=NW, image=self.sup_img['gold'])
		canvas.create_image(740, 370, anchor=NW, image=self.sup_img['estate'])
		canvas.create_image(740, 440, anchor=NW, image=self.sup_img['duchy'])
		canvas.create_image(740, 510, anchor=NW, image=self.sup_img['province'])
		canvas.create_image(740, 580, anchor=NW, image=self.sup_img['curse'])
		canvas.create_text(800, 192, text=str(self.supply[0]))
		canvas.create_text(800, 262, text=str(self.supply[1]))
		canvas.create_text(800, 332, text=str(self.supply[2]))
		canvas.create_text(800, 402, text=str(self.supply[3]))
		canvas.create_text(800, 472, text=str(self.supply[4]))
		canvas.create_text(800, 542, text=str(self.supply[5]))
		canvas.create_text(800, 612, text=str(self.supply[6]))
		canvas.create_image(20, 325, anchor=NW, image=self.logo)
		if self.supply[5]  == 0:
			canvas.delete("all")
			self.canvas.create_text(400, 400, text='{} Wins!!!'.format(self.winner), font=('Purisa', 50))
		#p1 hand 1-5:
		canvas.create_text(80, 90, text=self.bot1_name, font=('Purisa', 20))
		canvas.create_image(200, 20, anchor=NW, image=self.hand_img[self.p1_hand[0]])
		canvas.create_image(300, 20, anchor=NW, image=self.hand_img[self.p1_hand[1]])
		canvas.create_image(400, 20, anchor=NW, image=self.hand_img[self.p1_hand[2]])
		canvas.create_image(500, 20, anchor=NW, image=self.hand_img[self.p1_hand[3]])
		canvas.create_image(600, 20, anchor=NW, image=self.hand_img[self.p1_hand[4]])

		#p2 hand 1-5:
		canvas.create_text(80, 690, text=self.bot2_name, font=('Purisa', 20))
		canvas.create_image(200, 620, anchor=NW, image=self.hand_img[self.p2_hand[0]])
		canvas.create_image(300, 620, anchor=NW, image=self.hand_img[self.p2_hand[1]])
		canvas.create_image(400, 620, anchor=NW, image=self.hand_img[self.p2_hand[2]])
		canvas.create_image(500, 620, anchor=NW, image=self.hand_img[self.p2_hand[3]])
		canvas.create_image(600, 620, anchor=NW, image=self.hand_img[self.p2_hand[4]])

		#p1 purchase
		self.canvas.create_image(387, 193, anchor=NW, image=self.purchase_img[self.p1_move[1]])

		#p2 purchase
		self.canvas.create_image(387, 407, anchor=NW, image=self.purchase_img[self.p2_move[1]])