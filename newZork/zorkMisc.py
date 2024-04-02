from numpy import arange
from numpy.random import choice
from random import randint
from random import choice as randchoice
import traceback

# <-- Items START -->
class Leaflet:
	def __init__(self):
		self.grabbed = False

	def action(self):
		if self.grabbed:
			print("""\"WELCOME TO ZORK!

ZORK is a game of adventure, danger, and low cunning. In it you will explore
some of the most amazing territory ever seen by mortals. No computer should be
without one!\"\n""")

	def inspect(self): action(self)
leaflet = Leaflet()

class Lantern:
	def __init__(self):
		self.grabbed = False
		self.on = False

	def action(self):
		if self.grabbed:
			self.on = not self.on
			if self.on:
				print("The brass lantern is now on.\n")
			else:
				print("The brass lantern is now off.\n")

	def inspect(self):
		if self.grabbed:
			if self.on:
				print("The lamp is on.\n")
			else:
				print("The lamp is turned off.\n")
lantern = Lantern()

class Sword:
	def __init__(self):
		self.grabbed = False
		self.weapon = True
		self.valuable = True
		self.glow = 0

	def action(self):
		if self.grabbed: print("Whoosh!\n")

	def inspect(self):
		if self.glow == 0:
			print("There is nothing special about the sword.\n")
		elif self.glow == 1:
			print("The sword is glowing with a faint blue glow.\n")
		elif self.glow == 2:
			print("The sword is glowing very brightly.\n")
sword = Sword()

class Axe:
	def __init__(self):
		self.grabbed = False
		self.weapon = True

	def action(self): 
		if self.grabbed: print("Whoosh!\n")

	def inspect(self):
		if self.grabbed: print("There is nothing special about the axe.\n")
axe = Axe()

class JewelEncrustedEgg:
	def __init__(self):
		self.grabbed = False
		self.valuable = True
		self.opened = False

	def open(self):
		print("You have neither the tools nor the expertise.\n")

	def inspect(self):
		if self.opened:
			print("Idk what happens if it's opened.\n")
		else:
			print("The jewel-encrusted egg is closed.\n")
jewelEgg = JewelEncrustedEgg()

class Bottle:
	def __init__(self):
		self.water = True
		self.grabbed = False
		self.opened = False

	def open(self):
		print("Opened.\n")
		self.opened = True

	def drink(self):
		if self.opened and self.water:
			print("Thank you very much. I was rather thirsty (from all this talking, probably).\n")
			self.water = False

	def inspect(self):
		if self.water:
			print("""The glass bottle contains:
	A quantity of water.\n""")
		elif not self.water:
			print("The glass bottle is empty.\n")
bottle = Bottle()

class Bag:
	def __init__(self):
		self.grabbed = False
		self.opened = False
		self.sub = ["lunch", "clove of garlic"]

	def open(self):
		if self.opened == False:
			print("Opening the brown sack reveals a lunch, and a clove of garlic.\n")
			self.opened = True

	def inspect(self):
		if self.opened:
			print("The brown sack contains:")
			for i in self.sub:
				print(f"A", {i})
			print("\n")
		else:
			print("The brown sack is closed.\n")
bag = Bag()
# <-- Items END -->



# <-- Monsters START -->
class Troll:
	def __init__(self):
		self.alive = True
		self.wounds = 0
		self.position = ""

	def attack(self, player):
		atk_num = choice(arange(0, 3), p=[.4, .4, .2])
		if atk_num == 0:
			print("The troll's axe barely misses your ear.\n")
		elif atk_num == 1:
			print("The axe gets you right in the side. Ouch!\n")
			player.heals = 30
			player.wounds += 1
			if player.wounds == 2:
				player.death()
		elif atk_num == 2:
			print("The axe digs into your body, killing you instantly.\n")
			player.death()

	def hurt(self, player, weapon):
		try:
			if self.wounds == 2:
				atk_num = 3
			else:
				atk_num = choice(arange(0, 4), p=[.5, .2, .15, .15])

			if atk_num == 0:
				print("A quick stroke, but the troll is on guard.")
				self.attack(player)
			elif atk_num == 1:
				print("""The troll is confused and can't fight back.
The troll slowly regains his feet.""")
				self.wounds = 1
			elif atk_num == 2:
				print("The troll is battered into unconsciousness.\n")
				self.wounds = 2
			elif atk_num == 3:
				if self.wounds != 2:
					msg = [f"It's curtains for the troll as your {weapon.__class__.__name__} removes his head.",
					"The fatal blow strikes the troll square in the heart: He dies."]
					print(randchoice(msg))
				else:
					print("The unarmed troll cannot defend himself: He dies.")
				print("""Almost as soon as the troll breathes his last breath, a cloud of sinister
black fog envelops him, and when the fog lifts, the carcass has disappeared.""")
				if weapon == sword:
					print("Your sword is no longer glowing.\n")
				self.alive = False
		except Exception as e:
			print("An error occurred:")
			print(traceback.format_exc())
troll = Troll()

class Thief:
	def __init__(self):
		self.alive = True
		self.position = ""
		self.aggro = False
		self.checked = False
		self.wounds = 0
		self.checks = 0


	# REWORK: NOT DESIGNED WELL
	def spawn(self, player):
		spawn_num = choice(arange(0, 2), p=[.95, .05])
		if spawn_num == 1:
			self.position = player.position
			# Next if statement and 2 for loops check if any valuables are in items, dropped_items, or player's inventory
			for i in player.inventory:
				if hasattr(i, "valuable"):
					self.aggro = True
					self.checked = True
					break
			if hasattr(player.position, "items") and self.checked == False:
				for i in player.position.items:
					if hasattr(i, "valuable"):
						self.aggro = True
						self.checked = True
						break
			for i in player.position.dropped_items and self.checked == False:
				if hasattr(i, "valuable"):
					self.aggro = True
					self.checked = True
					break

			if self.aggro:
				fight_num = randint(1, 5)
				if fight_num not in [1, 2] and (len(player.inventory) > 0):
					for i in player.inventory:
						if hasattr(i, "valuable"):	
							print("The thief wants to fight you! This is just placeholder text btw\n")
							self.checks = 0
							break
						self.checks += 1
						if self.checks == len(player.inventory):
							print("The thief found nothing interesting and has left.\n")
							self.aggro = False
							self.position = ""
							self.checks = 0
				else:
					print("""A seedy-looking individual with a large bag just wandered through the room. On
the way through, he quietly abstracted some valuables from the room and from
your possesion, Mumbling something about \"Doing unto others before...\"\n""")
					for i in player.inventory:
						if player.inventory == 0:
							break
						else:
							if hasattr(i, "valuable"):
								player.inventory.remove(i)

					if (hasattr(player.position, "items")) or (hasattr(player.position, "dropped_items")):
						try:
							for i in player.position.items:
								if hasattr(i, "valuable"):
									player.position.items.remove(i)
							for i in player.position.dropped_items:
								if hasattr(i, "valuable"):
									player.position.dropped_items.remove(i)
						except:
							for i in player.position.dropped_items:
								if hasattr(i, "valuable"):
									player.position.dropped_items.remove(i)
					self.aggro = False
					self.position = ""

			else:
				self.aggro = False
				self.position = ""

	def attack(self, player):
		atk_num = choice(arange(0, 3), p=[.4, .4, .2])
		if atk_num == 0:
			print("The thief is too good! More placeholder text btw.\n")
		elif atk_num == 1:
			print("Too slow! You're hurt! Again, placeholder txt\n")
			player.heals = 30
			player.wounds += 1
			if player.wounds == 2:
				player.death()
		elif atk_num == 2:
			print("You suck.\n")
			player.death()

	def hurt(self, player, weapon):
		try:
			atk_num = choice(arange(0, 4), p=[.45, .45, .05, .05])

			if atk_num == 0:
				print("The thief parries.")
				self.attack(player)
			elif atk_num == 1:
				print("The thief barely dodges your attack.\n")
				self.attack(player)
			elif atk_num == 2:
				print("You actually hit him!\n")
				self.wounds = 2
			elif atk_num == 3:
				print("Too impressive! You killed the thief!\n")
				self.alive = False
		except Exception as e:
			tb = traceback.extract_tb(e.__traceback__)
			print(f"An error occurred on line {tb[-1].lineno}: {e}")
thief = Thief()

class Cyclops:
	def __init__(self):
		self.alive = True
		self.wounds = 0
		self.position = ""
		self.agitation = 0

	def hurt(self, player, weapon):
		print("The cyclops shurgs but otherwise ignores your pitful attempt.")
		self.agitate()

	def agitate(self, player):
		self.agitation += 1
		if self.agitation == 1:
			print("The cyclops seems somewhat agitated.\n")
		elif self.agitation == 2:
			print("The cyclops appears to be getting more agitated.\n")
		elif self.agitation == 3:
			print("The cyclops is moving about the room, looking for something.\n")
		elif self.agitation == 4:
			print("""The cyclops was looking for salt and pepper. No doubt they are condiments for
his upcoming snack.\n""")
		elif self.agitation == 5:
			print("The cyclops is moving toward you in an unfriendly manner.\n")
		elif self.agitation == 6:
			print("You have two choices: 1. Leave  2. Become dinner.\n")
		else:
			print("""The cyclops, tired of all of your games and trickery, grabs you firmly. As he
licks his chops, he says \"Mmm. Just like Mom used to make 'em.\" It's nice to
be appreciated.\n""")
			player.death()

	def death(self):
		print("""The cyclops, hearing the name of his father's deadly nemesis, flees the room
by knocking down the wall on the east of the room.\n""")
		self.alive = False
cyclops = Cyclops()			
# <-- Monsters END -->


items = {
	"leaflet": leaflet,
	"lantern": lantern,
	"sword": sword,
	"axe": axe,
	"egg": jewelEgg,
	"bottle": bottle,
	"bag": bag,
}


monsters = {
	"troll": troll,
	"thief": thief,
	"cyclops": cyclops,
}
