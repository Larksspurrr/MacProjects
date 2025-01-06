from zorkMisc import items as it
from zorkMisc import monsters as mon
from zorkMSG import *
import traceback

# This file holds the rooms and movement mechanics
# Monsters, items, and texts are imported from separate files to keep everything organized

directions = {
	"north_cmd": ["go north", "north", "n"],
	"east_cmd": ["go east", "east", "e"],
	"south_cmd": ["go south", "south", "s"],
	"west_cmd": ["go west", "west", "w"],
	"northeast_cmd": ["go northeast", "northeast", "ne"],
	"northwest_cmd": ["go northwest", "northwest", "nw"],
	"southeast_cmd": ["go southeast", "southeast", "se"],
	"southwest_cmd": ["go southwest", "southwest", "sw"],
	"down_cmd": ["go down", "down", "d"],
	"up_cmd": ["go up", "up", "u"],
}

grab_cmd = ["grab", "take"]
action_cmd = ["read", "examine", "activate"]


class Player:
	def __init__(self):
		self.inventory = []
		self.position = ""
		self.wounds = 0
		self.heals = 0

	def open_inventory(self):
		if len(self.inventory) == 0:
			print("You have nothing.\n")
		else:
			print("Your inventory: ")
			for i in self.inventory:
				print("A", i.__class__.__name__)

	def diagnostics(self):
		if self.wounds == 0:
			print("You are in perfect health.")
			print("You can be killed by a serious wound.\n")
		elif self.wounds == 1:
			print(f"You have a light wound, which can be cured after {self.heals} moves.")
			print("You can be killed by one more light wound.\n")

	def grab(self, cmd, obj):
		if hasattr(self.position, "opened"):
			if (obj in self.position.items) and (self.position.opened) and (cmd in grab_cmd):
				print("Taken.\n")
				obj.grabbed = True
				self.inventory.append(obj)
				self.position.items.remove(obj)
			elif (obj in self.position.dropped_items):
				print("Taken.\n")
				obj.grabbed = True
				self.inventory.append(obj)
				self.position.dropped_items.remove(obj)
			else:
				print(f"You can't see any {obj.__class__.__name__} here!\n")
		else:
			if (obj in self.position.items) and (cmd in grab_cmd):
				print("Taken.\n")
				obj.grabbed = True
				self.inventory.append(obj)
				self.position.items.remove(obj)
			elif (obj in self.position.dropped_items):
				print("Taken.\n")
				obj.grabbed = True
				self.inventory.append(obj)
				self.position.dropped_items.remove(obj)
			else:
				print(f"You can't see any {obj.__class__.__name__} here!\n")

	def drop(self, obj):
		if (obj in self.inventory):
			self.position.dropped_items.append(obj)
			obj.grabbed = False
			self.inventory.remove(obj)
			print("Dropped.\n")
		elif (len(self.inventory) > 0) and (obj not in self.inventory):
			print(f"You don't have a/an {obj.__class__.__name__}.\n")
		elif len(self.inventory) == 0:
			print("You have nothing to drop.\n")

	def action(self, obj):
		if len(self.inventory) > 0:
			self.inventory.obj.action()

	def death(self):
		for i in self.inventory:
			living_room.dropped_items.append(i)
			self.inventory.remove(i)
		self.position = forest_path
		self.wounds = 0
		self.heals = 0
		print(death_msg)
		self.position.enter()

	def attack(self, monster, weapon, player):
		if (monster in mon) and (mon[monster].position == self.position):
			mon[monster].hurt(player, weapon)
		else:
			print(f"You don't see any {monster} here!\n")

class WestHouse:
	def __init__(self):
		self.items = [it["leaflet"]]
		self.dropped_items = []
		self.entered = False
		self.opened = False
	
	def enter(self):
		print("West of House")
		if self.entered == False:
			print("""You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here.\n""")
		else:
			print("There is a small mailbox here.\n") 
		self.entered = True

	def open(self, obj):
		if (self.opened == False) and (obj == "mailbox"):
			self.opened = True
			print("Opening the small mailbox reveals a leaflet.\n")
		elif self.opened == True:
			print("It is already opened.\n")

	def travel(self, direction):
		if direction == "n":
			return north_house
		elif direction == "e":
			return "The door is boarded and you can't remove the boards.\n"
		elif direction == "s":
			return south_house
		elif direction == "w":
			return forest
		else:
			return "Invalid for some reason!\n"
west_house = WestHouse()

class NorthHouse:
	def __init__(self):
		self.dropped_items = []
		self.entered = False

	def enter(self):
		print("North of House")
		if self.entered == False:
			print(north_house_msg)
		self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "n":
			return forest_path
		elif direction == "e":
			return behind_house
		elif direction == "s":
			return "The windows are all boarded.\n"
		elif direction == "w":
			return west_house
		else:
			return "Invalid for some reason!\n"
north_house = NorthHouse()

class ForestPath:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		print("Forest Path")
		if self.entered == False:
			print(forest_path_msg)
			self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "n":
			return "PLACEHOLDER: CLEARING\n"
		elif direction == "e":
			return "PLACEHOLDER: FOREST 2n"
		elif direction == "s":
			return north_house
		elif direction == "w":
			return forest
		elif direction == "u":
			return up_a_tree
		else:
			return "Invalid for some reason!\n"
forest_path = ForestPath()

class Clearing:
	def __init__(self):
		self.entered = False
		self.dropped_items = []
		self.grating_moved = False
		self.grating_locked = False
		self.leaves_moved = False

	def enter(self):
		print("Clearing")
		if self.entered == False:
			print(clearing_msg)
			self.entered = True
		if self.leaves_moved == False:
			print("On the ground is a pile of leaves.\n")

	def move(self, obj):
		if obj == "leaves":
			print("Done.")
			print("In disturbing the pile of leaves, a grating is revealed.\n")
			self.leaves_moved = True
		elif obj == "grating":
			print("You can't move the grating.\n")

	def open(self, obj):
		if obj == "grating":
			if self.grating_locked:
				pass
			else:
				print("The grating is locked.\n")

	def travel(self, direction):
		if direction == "n":
			return "The forest becomes impenetrable to the north.\n"
		elif direction == "e":
			return "PLACEHOLDER: FOREST 2\n"
		elif direction == "s":
			return forest_path
		elif direction == "w":
			return forest
		else:
			return "You can't go that way.\n"
clearing = Clearing()

class Forest:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		print("Forest")
		if self.entered == False:
			print("This is a forest, with trees in all directions. To the east, there appears to be sunlight.")
			self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "n":
			return clearing
		elif direction == "e":
			return forest_path
		elif direction == "s":
			return "OTHER FOREST\n"
		elif direction == "w":
			return "You would need a machete to go further west.\n"
		else:
			return "You can't go that way.\n"
forest = Forest()

class UpATree:
	def __init__(self):
		self.entered = False
		self.items = [it["egg"]]
		self.dropped_items = []

	def enter(self):
		print("Up a Tree")
		if self.entered == False:
			print(tree_msg)
		print("\n")

	def travel(self, direction):
		if direction == "d":
			return forest_path
		else:
			return "Invalid for some reason!\n"
up_a_tree = UpATree()

class SouthHouse:
	def __init__(self):
		self.dropped_items = []
		self.entered = False

	def enter(self):
		print("South of House")
		if self.entered == False:
			print("You are facing the south side of a white house. There is no door here, and all the windows are boarded.")
		self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "n":
			return "The windows are all boarded.\n"
		elif direction == "e":
			return behind_house
		elif direction == "s":
			return forest
		elif direction == "w":
			return west_house
		else:
			return "Invalid for some reason!\n"
south_house = SouthHouse()

class BehindHouse:
	def __init__(self):
		self.dropped_items = []
		self.entered = False
		self.window_opened = False

	def enter(self):
		print("Behind House")
		if self.entered == False:
			print("You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which is slightly ajar.")
			self.entered = True
		print("\n")

	def open(self, obj):
		self.window_opened = True
		print("With great effort, you open the window far enough to allow entry.\n")

	def travel(self, direction):
		if direction == "n":
			return north_house
		elif direction == "e":
			return "PLACEHOLDER: CLEARING 2\n"
		elif direction == "s":
			return south_house
		elif direction == "w":
			if self.window_opened == False:
				return "The kitchen window is closed.\n"
			else:
				return kitchen
		else:
			return "Invalid for some reason!\n"
behind_house = BehindHouse()

class Kitchen:
	def __init__(self):
		self.items = [it["bottle"], it["bag"]]
		self.dropped_items = []
		self.entered = False

	def enter(self):
		print("Kitchen")
		if self.entered == False:
			self.entered = True
			print(kitchen_msg)
		if it["bag"] in self.items:
			print("On the table is an elongated brown sack, smelling of hot peppers.")
		if it["bottle"] in self.items:
			print("""A bottle is sitting on the table.
The glass bottle contains:
	A quantity of water""")
		print("\n")

	def travel(self, direction):
		if direction == "n":
			return "You can't go that way.\n"
		elif direction == "e":
			return behind_house
		elif direction == "s":
			return "You can't go that way.\n"
		elif direction == "w":
			return living_room
		else:
			return "Invalid for some reason!\n"
kitchen = Kitchen()

class LivingRoom:
	def __init__(self):
		self.items = [it["sword"], it["lantern"]]
		self.dropped_items = []
		self.moved = False
		self.entered = False
		self.door_opened = False
		self.trapdoor_opened = False

	def enter(self):
		print("Living Room")
		if self.entered == False:
			self.entered = True
			print(living_room_msg)

		if it["sword"] in self.items: print("Above the trophy case hangs an elvish sword of great antiquity.")
		if it["lantern"] in self.items: print("A battery-powered brass lantern is on the trophy case.")
		if strange_passage.entered == True: self.door_opened = True
		print("\n")

	def move(self, obj):
		if obj == "rug":
			print("""With great effort, the rug is moved to one side of the room, revealing the
dusty cover of a closed trap door.\n""")
			self.moved = True
			player.positon = living_room

	def open(self, obj):
		self.trapdoor_opened = True
		print("The door reluctantly opens to reveal a rickety staircase descending into darkness.\n")

	def travel(self, direction):
		if direction == "n":
			return "You can't go that way.\n"
		elif direction == "e":
			return kitchen
		elif direction == "s":
			return "You can't go that way.\n"
		elif direction == "w":
			if self.door_opened == False:
				return "The door is nailed shut.\n"
			else:
				return strange_passage
		elif direction == "d":
			if self.moved == False:
				return "You can't go that way.\n"
			elif (self.trapdoor_opened == False) and (self.moved):
				return "The trapdoor is closed.\n"
			elif self.trapdoor_opened:
				return cellar
		else:
			return "Invalid for some reason!\n"
living_room = LivingRoom()

class Cellar:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		if player.position == living_room:
			living_room.trapdoor_opened = False
			print("The trap door crashes shut, and you hear someone barring it.\n")

			player.position = cellar

		if ((it["lantern"] in player.inventory) and (it["lantern"].on == False)) or (it["lantern"] not in player.inventory):
			print("You have moved into a dark place.")
			print("It is pitch black and you're likely to be eaten by a grue.")
		else:
			print("Cellar")
			if self.entered == False:
				print(cellar_msg)
				if (it["sword"] in player.inventory) and (mon["troll"].alive == True):
					print("Your sword is glowing with a faint blue glow.")
			print("\n")

	def travel(self, direction):
		if direction == "n":
			if ((it["lantern"] in player.inventory) and (it["lantern"].on == False)) or (it["lantern"] not in player.inventory):
				print("Oh no! A lurking grue slithered into the room and devoured you!\n")
				player.death()
				return ""
			else: 
				return troll_room
		elif direction == "e":
			return "You can't go that way.\n"
		elif direction == "s":
			return "PLACEHOLDER: EAST OF CHASM\n"
		elif direction == "w":
			return "You try to ascend the ramp, but it is impossible, and you slide back down.\n"
		elif direction == "u":
			return "The trapdoor is closed. \n"
		else:
			return "Invalid for some reason!\n"
cellar = Cellar()

class TrollRoom:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		print("Troll Room")
		if self.entered == False:
			print(troll_room_msg)
		if mon["troll"].alive:
			print("A nasty looking troll, brandishing a bloody axe, blocks all passages out of the room.")
			if it["sword"] in player.inventory:
				print("Your sword has begun to glow very brightly.\n")


	def travel(self, direction):
		if direction == "n":
			return "You can't go that way.\n"
		elif direction == "e":
			if mon["troll"].alive:
				print("The troll fends you off with a menacing gesture.")
				mon["troll"].attack(player)
				return ""
			else:
				return "PLACEHOLDER: EAST-WEST PASSAGE\n"
		elif direction == "s":
			return cellar
		elif direction == "w":
			if mon["troll"].alive:
				print("The troll fends you off with a menacing gesture.")
				mon["troll"].attack(player)
				return ""
			else:
				return maze_entrance
		else:
			return "Invalid for some reason!\n"
troll_room = TrollRoom()
mon["troll"].position = troll_room

class Maze:
	def __init__(self):
		self.dropped_items = []
		self.entrance = False
		self.skeleton = False
		self.north = ""
		self.east = ""
		self.south = ""
		self.west = ""
		self.up = ""
		self.down = ""
		self.northeast = ""
		self.southeast = ""
		self.northwest = ""
		self.southwest = ""

	def enter(self):
		print("Maze")
		print(maze_msg)
		if self.entrance:
			print("You are back at the beginning of the maze.")
		elif self.skeleton:
			print(skeleton_room_msg)

	def add_directions(self, n, e, s, w, u, d, ne, se, nw, sw, *args):
		self.north = n
		self.east = e
		self.south = s
		self.west = w
		self.up = u
		self.down = d
		self.northeast = ne
		self.southeast = se
		self.northwest = nw
		self.southwest = sw

		for arg in args:
			if arg == "entrance":
				self.entrance = True
			elif arg == "skeleton":
				self.skeleton = True

	def travel(self, direction):
		direction_dict = {
			"n": self.north,
			"e": self.east,
			"s": self.south,
			"w": self.west,
			"u": self.up,
			"d": self.down,
			"ne": self.northeast,
			"se": self.southeast,
			"nw": self.northwest,
			"sw": self.southwest
		}

		return direction_dict.get(direction, self.invalid_direction)

	def invalid_direction(self):
		print("Invalid for some reason!\n")


class CyclopsRoom:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		print("Cyclops Room")
		if self.entered == False:
			print(cyclops_room_msg)
			if it["sword"] in player.inventory:
				print("Your sword has begun to glow very brightly.")
			self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "nw":
			return correct_maze_5
		elif direction == "e":
			if mon["cyclops"].alive:
				return "The east wall is solid rock.\n"
			else:
				return strange_passage
		else:
			return "You can't go that way.\n"
cyclops_room = CyclopsRoom()
mon["cyclops"].position = cyclops_room

class StrangePassage:
	def __init__(self):
		self.entered = False
		self.dropped_items = []

	def enter(self):
		print("Strange Passage")
		if self.entered == False:
			print("""This is a long passage. To the west is one entrance. On the east there is an
old wooden door, with a large opening on it (about cyclops sized).""")
			self.entered = True
		print("\n")

	def travel(self, direction):
		if direction == "e":
			return living_room
		elif direction == "w":
			return cyclops_room
		else:
			return "You can't go that way."
strange_passage = StrangePassage()

maze_entrance = Maze()
correct_maze_1 = Maze()
correct_maze_2 = Maze()
skeleton_room = Maze()
correct_maze_3 = Maze()
correct_maze_4 = Maze()
correct_maze_5 = Maze()
# "N", "E", "S", "W", "U", "D", "NE", "SE", "NW", "SW"
# Doing all of this so that there are no errors when setting up the rooms between each maze room.
# Path from maze to cyclops is [W W U SW E S SE]
# I UNDERSTAND THIS IS MESSY AND NOT THE SAME AS THE ORIGINAL, IT IS WHAT I COULD COME UP WITH
# SUBJECT TO CHANGE, I REPEAT: SUBJECT TO CHANGE
maze_entrance.add_directions(maze_entrance, maze_entrance, troll_room, correct_maze_1, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, "entrance")
correct_maze_1.add_directions(maze_entrance, maze_entrance, maze_entrance, correct_maze_2, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance)
correct_maze_2.add_directions(maze_entrance, correct_maze_1, maze_entrance, maze_entrance, skeleton_room, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance)
skeleton_room.add_directions(maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, correct_maze_2, maze_entrance, maze_entrance, maze_entrance, correct_maze_3, "skeleton")
correct_maze_3.add_directions(maze_entrance, correct_maze_4, maze_entrance, maze_entrance, maze_entrance, maze_entrance, skeleton_room, maze_entrance, maze_entrance, maze_entrance)
correct_maze_4.add_directions(maze_entrance, maze_entrance, correct_maze_5, correct_maze_3, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance)
correct_maze_5.add_directions(correct_maze_4, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, maze_entrance, cyclops_room, maze_entrance, maze_entrance)
# I WANTED TO LEAVE THIS FOR ANOTHER DAY, BUT I GUESS I FORGOT OR GOT TOO BUSY
# IT JUST BRINGS YOU BACK TO THE BEGINNING IF YOU CHOOSE A WRONG OPTION

player = Player()
player.position = west_house
west_house.enter()

def heal():
	if player.wounds == 1:
		if player.heals > 0:
			player.heals -= 1
		else:
			player.wounds -= 1
	elif player.wounds == 2:
		player.death()

while True:
	try:
		x = input(">")

		# This for loop handles movement.
		for key in directions:
			if x in directions[key]:
				if (mon["thief"].position == player.position) and (mon["thief"].alive):
					print("The thief will not let you through.")
					mon["thief"].attack(player)
				else:
					direction = directions[key][2]
					result = player.position.travel(direction)
					if isinstance(result, str):
						print(result)
					else:
						player.position = result
						player.position.enter()
						heal()
						if (player.position != cyclops_room) and (player.position != troll_room):
							mon["thief"].spawn(player)
					
						if len(player.position.dropped_items) > 0:
							for i in player.position.dropped_items:
								print(f"There is a/an {i.__class__.__name__} on the ground")
							print("\n")

		# Handles the cyclops' agitation.
		if (mon["cyclops"].position == player.position) and (mon["cyclops"].alive) and (x not in directions["northwest_cmd"]):
			mon["cyclops"].agitate(player)
		
		# Handles the one-word inputs. Could be put into a dictionary to simply match the keyword with the command
		if x == "quit": break
		elif x == "inventory": player.open_inventory()
		elif x == "diagnostics": player.diagnostics()
		elif x == "": print("I beg your pardon?\n")
		elif (x == "ODYSSEUS"):
			if (player.position == cyclops_room) and (mon["cyclops"].alive): mon["cyclops"].death()
			else: print("Wasn't he a sailor?\n")

		# From here up to 'except', the code handles the commands by splitting the input into separate words.
		x_parts = x.split()
		if (len(x_parts) == 4) and (x_parts[0].strip() == "attack"):
			player.attack(x_parts[1].strip(), x_parts[3].strip(), player)

		if (len(x_parts) == 2) and (x_parts[1].strip() not in mon):
			cmd, obj = x_parts[0].strip().lower(), x_parts[1].strip().lower()
			if cmd in grab_cmd:
				obj = it[obj]
				player.grab(cmd, obj)
			elif cmd == "drop":
				obj = it[obj]
				player.drop(obj)
			elif cmd == "open":
				if (len(player.inventory) > 0) and (obj in it) and (it[obj] in player.inventory):
					it[obj].open()
				elif hasattr(player.position, "open"):
					player.position.open(obj)
			elif cmd == "move":
				player.position.move(obj)
			elif cmd in action_cmd:
				obj = it[obj]
				obj.action()
			elif (cmd == "inspect") and (it[obj] in it) and (it[obj] in player.inventory):
				it[obj].inspect()

	except Exception as e:
		# This was for debugging purposes
		print("An error occurred:")
		print(traceback.format_exc())
