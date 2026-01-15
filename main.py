import pygame, random, math, json, sys
from pygame.locals import *
from map import *
from cutscene import *
from timers import Timer

RESOLUTION = WIDTH, HEIGHT = 350, 350
FPS = 30

print("Initializing Pygame...")

pygame.init()
pygame.mixer.init(44100, -16, 4, 2048)
display = pygame.display.set_mode(RESOLUTION, flags = pygame.SCALED | pygame.RESIZABLE)
screen = pygame.surface.Surface(RESOLUTION)
pygame.display.set_caption('Retraich 2')
clock = pygame.time.Clock()

retrofont = pygame.font.Font('Fonts/retroville.ttf', 20)
retrofontmedium = pygame.font.Font('Fonts/retroville.ttf', 16)
retrofontsmall = pygame.font.Font('Fonts/retroville.ttf', 12)
retrofonttiny = pygame.font.Font('Fonts/retroville.ttf', 10)

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

sword_sfx = pygame.mixer.Sound("Sounds/sfx/sword.wav")
bow_sfx = pygame.mixer.Sound("Sounds/sfx/bow.wav")
hit_sfx = pygame.mixer.Sound("Sounds/sfx/hit.wav")
hurt_sfx = pygame.mixer.Sound("Sounds/sfx/hurt.wav")
break_sfx = pygame.mixer.Sound("Sounds/sfx/break.wav")
kill_sfx = pygame.mixer.Sound("Sounds/sfx/kill.wav")
scroll_sfx = pygame.mixer.Sound("Sounds/sfx/scroll.wav")
collect_sfx = pygame.mixer.Sound("Sounds/sfx/collect.wav")
collect2_sfx = pygame.mixer.Sound("Sounds/sfx/collect2.wav")
collect3_sfx = pygame.mixer.Sound("Sounds/sfx/collect3.wav")
collect4_sfx = pygame.mixer.Sound("Sounds/sfx/collect4.wav")
grappling_sfx = pygame.mixer.Sound("Sounds/sfx/grappling.wav")
grapple_sfx = pygame.mixer.Sound("Sounds/sfx/grapple.wav")
dig_sfx = pygame.mixer.Sound("Sounds/sfx/dig.wav")
dug_sfx = pygame.mixer.Sound("Sounds/sfx/dug.wav")
change_by_sfx = pygame.mixer.Sound("Sounds/sfx/change by.wav")
one_up_sfx = pygame.mixer.Sound("Sounds/sfx/1 up.wav")
secret_sfx = pygame.mixer.Sound("Sounds/sfx/secret.wav")
click_sfx = pygame.mixer.Sound("Sounds/sfx/click.wav")
select_sfx = pygame.mixer.Sound("Sounds/sfx/select.wav")
select2_sfx = pygame.mixer.Sound("Sounds/sfx/blip2.wav")
blip_sfx = pygame.mixer.Sound("Sounds/sfx/blip.wav")
beep_sfx = pygame.mixer.Sound("Sounds/sfx/beep.wav")
swoosh_sfx = pygame.mixer.Sound("Sounds/sfx/swoosh.wav")
startup_sfx = pygame.mixer.Sound("Sounds/sfx/startup.wav")

icon = pygame.image.load("Assets/icon.png").convert_alpha()
pygame.display.set_icon(icon)

background = pygame.image.load("Assets/background.png").convert_alpha()
logo = pygame.image.load("Assets/logo.png").convert_alpha()
heart = pygame.image.load("Assets/heart.png").convert_alpha()
shadow = pygame.image.load("Assets/shadow.png").convert_alpha()
wave = pygame.image.load("Assets/waves.png").convert_alpha()
wave_light = pygame.image.load("Assets/waves light.png").convert_alpha()

texts_end = [
  " ", " ",
  "This ends the story", "of Retraich.",
  " ", " ", " ",
  "Finally, no more evil lurking",
  "in the dark",
  "Peace and harmony returns",
  "to the nation.",
  " ", " ", " ", " ", " ", " ", " ", " ",
  "Game created by Kaan, Tunari-",
  " ", " ", " ", " ",
  "Another quest awaits in Retraich 2-",
  "Push START button",
]

def maxint(int, max):
  if int > max: return max
  else: return int

def minint(int, min):
  if int < min: return min
  else: return int

def inverse(int, min, max):
  balance = (min + max) / 2
  if int < balance: int = (int + ((int - balance) * 2) + (max * 2))
  if int > balance: int = (int - ((balance - int) * 2) - (min * 2))
  return int

game_over_controller_delay = Timer()

saves = {
  "save1": {
    "save": "save1", "name": "New Save Slot         ", "started": False,
    "x": WIDTH / 2, "y": WIDTH / 2, "scroll": [0, 0], "place": "start", "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3,
    "actors": {}, "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  "save2": {
    "save": "save2", "name": "New Save Slot         ", "started": False,
    "x": WIDTH / 2, "y": WIDTH / 2, "scroll": [0, 0], "place": "start", "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3,
    "actors": {}, "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  "save3": {
    "save": "save3", "name": "New Save Slot         ", "started": False,
    "x": WIDTH / 2, "y": WIDTH / 2, "scroll": [0, 0], "place": "start", "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3,
    "actors": {}, "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  "savedefault": {
    "save": "savedefault", "name": "New Save Slot         ", "started": False,
    "x": WIDTH / 2, "y": WIDTH / 2, "scroll": [0, 0], "place": "start", "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3,
    "actors": {}, "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
}

monster_types = {
  "madpuff":      {"hearts": 3, "speed": 2, "can shoot": False, "drop": "diamond"},
  "croaker":      {"hearts": 2, "speed": 5, "can shoot": False, "drop": "diamond"},
  "regall":       {"hearts": 5, "speed": 0, "can shoot": True, "drop": ""},

  "scorpio":      {"hearts": 2, "speed": 6, "can shoot": False, "drop": "diamond"},
  "husk":         {"hearts": 6, "speed": 1, "can shoot": False, "drop": "arrow"},
  "yuma":         {"hearts": 4, "speed": 0, "can shoot": True, "drop": ""},

  "foxox":        {"hearts": 3, "speed": 4, "can shoot": True, "drop": "diamond"},
  "sharpy":       {"hearts": 2, "speed": 5, "can shoot": False, "drop": "arrow"},

  "xroaker":      {"hearts": 3, "speed": 6, "can shoot": False, "drop": "diamond"},
  "regalios":     {"hearts": 1, "speed": 0, "can shoot": True, "drop": ""},
  "madpuff weak": {"hearts": 1, "speed": 2, "can shoot": False, "drop": ""},

  "madpuff renk": {"hearts": 35, "speed": 1, "can shoot": True, "drop": "renk 4"},
}

container_types = {
  "stone": {"contents": ["diamonds"], "price": 0, "sound": secret_sfx},

  "chest": {"contents": ["diamonds"], "price": 0, "sound": break_sfx},
  "arrow chest": {"contents": ["diamond", "diamond", "diamond", "arrow"], "price": 0, "sound": break_sfx},
  "arrow vase": {"contents": ["arrow"], "price": 0, "sound": break_sfx},
  "heart chest": {"contents": ["heart"], "price": 0, "sound": break_sfx},

  "treasure": {"contents": ["healing potion"], "price": 0, "sound": break_sfx},
  
  "granite right": {"contents": [], "price": 0, "sound": secret_sfx},

  "fragile granite": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile granite 2": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile granite 3": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile boulder": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile boulder hpp": {"contents": ["healing potion priceless"], "price": 0, "sound": secret_sfx},
  "fragile wall horizontal": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile wall vertical": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile block heart": {"contents": ["heart"], "price": 0, "sound": secret_sfx},
  "fragile block diamonds": {"contents": ["diamonds"], "price": 0, "sound": secret_sfx},

  "ship": {"contents": [], "price": 0, "sound": secret_sfx},
}

collictible_types = {
  "diamond":           {"value": 1, "arrow": 0, "heart": 0, "price": 0, "sound": collect2_sfx, "title": ""},
  "diamonds":          {"value": 5, "arrow": 0, "heart": 0, "price": 0, "sound": collect_sfx, "title": ""},
  "shovel":            {"value": "shovel", "arrow": 0, "heart": 0, "price": 20, "sound": "", "title": ""},
  "bow":               {"value": "bow", "arrow": 0, "heart": 0, "price": 20, "sound": "", "title": ""},
  "arrow":             {"value": 0, "arrow": 3, "heart": 0, "price": 0, "sound": collect3_sfx, "title": ""},
  "heart":             {"value": 0, "arrow": 0, "heart": 1, "price": 0, "sound": one_up_sfx, "title": ""},
  "heart with price":  {"value": 0, "arrow": 0, "heart": 1, "price": 5, "sound": one_up_sfx, "title": ""},
  "grapple hook":      {"value": "grapple hook", "arrow": 0, "heart": 0, "price": 50, "sound": "", "title": ""},
  "healing capsule":   {"value": "healing capsule", "arrow": 0, "heart": 0, "price": 8, "sound": "", "title": ""},
  "healing potion":    {"value": "healing potion", "arrow": 0, "heart": 0, "price": 0, "sound": collect3_sfx, "title": ""},
  "renk 1":            {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 2":            {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 3":            {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 4":            {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
}

npcs = {
  "fidda": ["Would you like a tool? Feel free to buy anything!"],
  "ivan": ["There might or might not be a secret somewhere..."],
}

flash_logo_timer = Timer()
sword_load = 0
sword_go = 0
flash_more = 0

class Main:
  def __init__(self):
    print("Running Game...")
    pygame.mixer.music.load("Sounds/tracks/Introduction Theme.mp3")
    pygame.mixer.music.play(-1, 0.0)
    self.started = False
    self.volume = 1
    self.scrolly = 0
    self.gamestate = 0
    self.score = 0
    self.tiles = []
    self.actors = []
    self.interactables = []
    self.past_actors = []
    self.scrolls = [0, 0]
    self.minimaps = [0, 0]
    self.projectiles = []
    self.items = [save for save in saves.values() if save["save"] != "savedefault"]
    self.keyboard = [["A", "B", "C", "D", "E", "F", "G"],
                     ["H", "I", "J", "K", "L", "M", "N"],
                     ["O", "P", "Q", "R", "S", "T", "U"],
                     ["V", "W", "X", "Y", "Z", "<", "_"]]
    self.selected_item_y = 0
    self.selected_item_x = 0
    self.timer = Timer()
    self.save = "save1"
    self.savename = "New Save Slot         "
    self.letter = ""
    self.autosave_timer = Timer()
    self.renk_timer = Timer()
    self.gameover_timer = Timer()
    self.item_float_timer = Timer()
    self.immobilize = False
    self.hide_player = False
    self.theme = "Polovo's Struggle"
    self.place = "start"
    self.traveling_to = ""
    self.shake = [0, 0]
    self.saving_works = True
    self.transition_2nd_half = False
    self.transition_timer = Timer()
    self.cutscene = ""
    self.from_edge = ""
    self.cs_key = 0
    self.heart_shake_timer = Timer()
    self.cs_wait_timer = Timer()
    self.map_memory = {}
    self.saveable = True
    #pygame.mixer.music.set_volume(0)
  
  def update(self):
    global FPS
    if self.gamestate == 0: self.title()
    if self.gamestate == 1: self.menu()
    if self.gamestate == 2: self.new_save()
    if self.gamestate == 3: self.are_you_sure()
    if self.gamestate == 4: self.intro_cutscene()
    if self.gamestate == 4: self.gameplay()
    if self.gamestate == 6: self.ending()

    if self.gamestate == 0: FPS = 20
    else: FPS = 30

    run()
  
  def title(self):
    global k_select, k_start, k_a, sword_load, sword_go, flash_more
    if k_start and not self.started: self.started = True; k_select = False; swoosh_sfx.play()
    if self.started:
      self.volume -= 0.2; sword_load += 20; pygame.mixer.music.set_volume(minint(self.volume, 0))
      if sword_load >= 150: sword_go += 50
      if sword_go == 150: flash_more = True; startup_sfx.play()
    screen.blit(background, (0, 0)); flash_type = [pygame.BLEND_RGBA_MIN, pygame.BLEND_RGB_ADD]; flash_type2 = [pygame.BLEND_RGBA_MULT, pygame.BLEND_RGB_ADD]; logows = pygame.image.load("Assets/logo ws.png").convert_alpha() ;logoos = pygame.image.load("Assets/logo os.png").convert_alpha(); logos = pygame.image.load("Assets/logo s.png").convert_alpha(); logoss = pygame.image.load("Assets/logo ss.png").convert_alpha(); fl = round(maxint(minint(abs(((flash_logo_timer.oscillate(1, 11.25 * (int(flash_more) + 1), 0) - 10) * 15) - 100), 0), 255)); logows.fill((fl, fl, fl), special_flags=flash_type[int(flash_more)]); logoos.fill((fl, fl, fl), special_flags=flash_type2[int(flash_more)]); screen.blit(logos, (0, 0)); screen.blit(logoss, ((0 + maxint(sword_go, 145)) - maxint(sword_load, 20), -5)); screen.blit(logoos, ((0 + maxint(sword_go, 145)) - maxint(sword_load, 20), -5)); screen.blit(logows, (0, 0)); screen.blit(retrofontmedium.render("Press START", True, "White"), (195 - (sword_load * 5), 200)); screen.blit(retrofontmedium.render("Tunari Presents...", True, "Black"), (-198 + (maxint(sword_go, 80) * 3.25) + (maxint(sword_go, 500) * 0.15), 201)); screen.blit(retrofontmedium.render("Tunari Presents...", True, "White"), (-200 + (maxint(sword_go, 80) * 3.25) + (maxint(sword_go, 500) * 0.15), 200))
    try:
      if sword_go > 2000: screen.fill((abs(sword_go) - 2000, abs(sword_go) - 2000, abs(sword_go) - 2000), special_flags=pygame.BLEND_RGBA_SUB); sword_go -= 46
    except: screen.fill("Black"); self.gamestate = 1; pygame.mixer.music.stop(); self.volume = 1; pygame.mixer.music.set_volume(self.volume)
    k_select = False; k_start = False; k_a = False; self.selected_item_x, self.selected_item_y = 0, 0

  def menu(self):
    self.tiles.clear()
    self.actors.clear()
    self.map_memory = {}
    #screen.blit(logo, ((WIDTH / 2) - (logo.get_width() / 2), 40))
    screen.blit(retrofont.render("Select Game File", False, "White"), (35, 50))
    pygame.draw.rect(screen, (0, 0, 50), ((-45, 100), (450, 155)), 3)
    pygame.draw.rect(screen, "Blue", ((-45, 102), (450, 157)), 3)
    for index, item in enumerate(self.items):
      if index == self.selected_item_y:
        screen.blit(retrofontmedium.render("> " + item["name"], False, "White"), (30, 120 + (index * 40)))
        #screen.blit(pygame.image.load(f"Assets/tuff/walkfront{self.timer.keep_count(FPS / 3, 3, 1)}.png").convert_alpha(), (75, 120 + (index * 40)))
        self.save = item["save"]; self.savename = item["name"]
      else:
        screen.blit(retrofontmedium.render(item["name"], False, "White"), (35, 120 + (index * 40)))
        #screen.blit(pygame.image.load(f"Assets/tuff/walkfront0.png").convert_alpha(), (60, 120 + (index * 40)))
    screen.blit(retrofontsmall.render('Press SELECT to Delete a Save', True, 'White'), (3, HEIGHT-15))
    self.controls()

  def new_save(self):
    pygame.draw.rect(screen, (0, 0, 50), ((-45, 100), (450, 190)), 3); pygame.draw.rect(screen, "Blue", ((-45, 102), (450, 192)), 3)
    screen.blit(retrofont.render("New Game File", False, "White"), (60, 50)); screen.blit(retrofont.render(self.savename + "_", False, "White"), (45, 110))
    for indexy, itemsx in enumerate(self.keyboard):
      for indexx, letter in enumerate(itemsx):
        if indexy == self.selected_item_y and indexx == self.selected_item_x:
          if self.timer.wait(FPS / 3): screen.blit(retrofont.render(letter, False, "White"), (37 + (indexx * 42), 145 + (indexy * 35)))
          self.letter = letter
        else: screen.blit(retrofont.render(letter, False, "White"), (37 + (indexx * 42), 145 + (indexy * 35)))
    screen.blit(retrofontsmall.render('Press START to Continue', True, 'White'), (3, HEIGHT-30)); screen.blit(retrofontsmall.render('Press SELECT to See Accents', True, 'White'), (3, HEIGHT-15)); self.controls()

  def are_you_sure(self):
    screen.blit(retrofont.render("Are you sure?", False, "White"), (16, 50)); pygame.draw.rect(screen, "Blue", ((45, 120), (250, 120)), 5)
    for index, item in enumerate(["No", "Yes"]):
      if index == self.selected_item_y: screen.blit(retrofontmedium.render(item, False, "White"), (110, 145 + (index * 40)))
      else: screen.blit(retrofontmedium.render(item, False, "White"), (95, 145 + (index * 40)))
    self.controls()
  
  def controls(self):
    global k_a, saves
    if self.gamestate == 1:
      if k_up: self.selected_item_y -= 1; click_sfx.play()
      if k_down: self.selected_item_y += 1; click_sfx.play()
      if self.selected_item_y >= len(self.items): self.selected_item_y = 0
      if self.selected_item_y == -1: self.selected_item_y = len(self.items) - 1

      if k_a or k_start:
        if self.items[self.selected_item_y]["name"] == "New Save Slot         ": self.gamestate = 2; k_a = False; self.savename = ""; select2_sfx.play(); self.selected_item_x, self.selected_item_y = 0, 0
        else: self.load_game(); k_a = False; select_sfx.play()

      if k_select and self.items[self.selected_item_y]["name"] != "New Save Slot         ":
        self.gamestate = 3; self.selected_item_y = 0

    if self.gamestate == 2:
      if k_up: self.selected_item_y -= 1; click_sfx.play(); self.timer.reset()
      if k_down: self.selected_item_y += 1; click_sfx.play(); self.timer.reset()
      if self.selected_item_y >= len(self.keyboard): self.selected_item_y = 0; self.timer.reset()
      if self.selected_item_y == -1: self.selected_item_y = len(self.keyboard) - 1; self.timer.reset()
      if k_left: self.selected_item_x -= 1; click_sfx.play(); self.timer.reset()
      if k_right: self.selected_item_x += 1; click_sfx.play(); self.timer.reset()
      if self.selected_item_x >= 7: self.selected_item_x = 0; self.timer.reset()
      if self.selected_item_x == -1: self.selected_item_x = 7 - 1; self.timer.reset()
      if k_a:
        if self.letter == "<": self.savename = self.savename[:-1]; self.timer.reset(); select2_sfx.play()
        elif self.letter == "_":
          if len(self.savename) < 13: self.savename += " "; self.timer.reset(); select2_sfx.play()
        else:
          if len(self.savename) < 13: self.savename += self.letter; self.timer.reset(); select2_sfx.play()

      if k_start and len(self.savename) > 0: self.gamestate = 1; k_a = False; saves[self.save]["name"] = self.savename; self.timer.reset(); self.selected_item_x, self.selected_item_y = 0, 0

      if k_select:
        self.keyboard = [["Æ", "ß", "Ç", "Ð", "Ë", "F", "Ğ"],
                         ["H", "i", "J", "K", "Ł", "M", "Ñ"],
                         ["Ö", "P", "Q", "R", "Š", "T", "Ü"],
                         ["V", "W", "X", "Ÿ", "Ž", "<", "_"]]
      else:
        self.keyboard = [["A", "B", "C", "D", "E", "F", "G"],
                         ["H", "I", "J", "K", "L", "M", "N"],
                         ["O", "P", "Q", "R", "S", "T", "U"],
                         ["V", "W", "X", "Y", "Z", "<", "_"]]
        
    if self.gamestate == 3:
      if k_up: self.selected_item_y -= 1; click_sfx.play()
      if k_down: self.selected_item_y += 1; click_sfx.play()
      if self.selected_item_y >= 2: self.selected_item_y = 0
      if self.selected_item_y == -1: self.selected_item_y = 1

      if k_a and self.selected_item_y == 1:
        saves[self.save]["name"] = "New Save Slot         "; saves[self.save]["x"], saves[self.save]["y"] = WIDTH / 2, HEIGHT / 2; saves[self.save]["direction"] = "front"
        saves[self.save]["started"], saves[self.save]["scroll"] = False, [0, 0]; saves[self.save]["hearts"] = 5; saves[self.save]["wealth"] = 0
        saves[self.save]["place"] = "start"; saves[self.save]["weapon"] = "sword"; saves[self.save]["items"] = ["sword"]; saves[self.save]["arrows"] = 3
        saves[self.save]["renks"] = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}; saves[self.save]["actors"] = {}
        with open("Saves/memory_card/savefile.txt", "w") as out_: json.dump(saves, out_)
        self.items = [save for save in saves.values() if save["save"] != "savedefault"]
        self.gamestate = 1
        self.selected_item_y = 0
      
      if k_a and self.selected_item_y == 0: self.gamestate = 1

  def intro_cutscene(self):
    pass
  
  def ending(self):
    maxnum = 550; self.scrolly += 1.4
    screen.blit(logo, (40, ((HEIGHT * 2) - 10) - maxint(self.scrolly, maxnum)))
    for index, text in enumerate(texts_end):
      if type(text) == str:
        dialogue = retrofontmedium.render(text, True, "White")
        if text[len(text) - 1] == "~": dialogue = retrofontmedium.render(text[:-1], True, "Black")
        if text[len(text) - 1] == "": dialogue = retrofontsmall.render(text[:-1], True, "White")
        screen.blit(dialogue, ((WIDTH / 2) - (dialogue.get_width() / 2), ((index * 22.5) + (HEIGHT / 3.5)) - maxint(self.scrolly, maxnum)))
    if self.scrolly > maxnum and k_start:
      saves[self.save]["name"] = "New Save Slot         "; saves[self.save]["x"], saves[self.save]["y"] = WIDTH / 2, HEIGHT / 2
      saves[self.save]["position"] = [0, 0]; saves[self.save]["minimaps"] = [0, 0]; saves[self.save]["direction"] = "front"
      saves[self.save]["hearts"] = 5; saves[self.save]["wealth"] = 0; saves[self.save]["weapon"] = "sword"; saves[self.save]["items"] = ["sword"]; saves[self.save]["arrows"] = 3
      saves[self.save]["renks"] = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}; saves[self.save]["actors"] = []
      saves[self.save]["past actors"] = []; saves[self.save]["theme"] = "Legends of the Renk Gems"; saves[self.save]["Immobilize"] = False
      self.actors.clear()
      self.past_actors.clear()
      self.save_game(); self.gamestate = 1; self.selected_item_y = 0; pygame.mixer.music.stop()
  
  def gameplay(self):
    global screen
    if self.player.hearts > 0:
      self.timer.count(5, 4, 0)
      if self.timer.tally == 3 and self.timer.time == 1: beep_sfx.play()
      if self.timer.tally >= 3:
        for tile in [tile for tile in self.tiles if not tile.front]:
          if tile.rect.right > self.scrolls[0] and tile.rect.x < self.scrolls[0] + WIDTH and tile.rect.bottom > self.scrolls[1] and tile.rect.y < self.scrolls[1] + HEIGHT: tile.update()
        #screen.blit(shadow, ((self.player.rect.x - 5) - main.scrolls[0], (self.player.rect.y - 10) - main.scrolls[1] + 7))
        for actor in self.actors:
          if not isinstance(actor, NPC):
            if actor.alive and actor.rect.right > self.scrolls[0] and actor.rect.bottom > self.scrolls[1] and actor.rect.x < self.scrolls[0] + WIDTH and actor.rect.y < self.scrolls[1] + HEIGHT:
              actor.update()
        for actor in [actor for actor in self.actors if isinstance(actor, Furniture)]: actor.update()
        for actor in self.actors:
          if isinstance(actor, NPC):
            if actor.alive: actor.update()
        self.player.update()
        for actor in [actor for actor in self.actors if isinstance(actor, Furniture)]: actor.draw_top()
        for tile in [tile for tile in self.tiles if tile.front]:
          if tile.rect.right > self.scrolls[0] and tile.rect.x < self.scrolls[0] + WIDTH and tile.rect.bottom > self.scrolls[1] and tile.rect.y < self.scrolls[1] + HEIGHT: tile.update()
        for actor in self.actors:
          if isinstance(actor, NPC):
            if actor.alive:
              try:
                if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "speech":
                  if actor.type == cutscenes[self.cutscene]["keys"][self.cs_key][1]:
                    actor.active, actor.full_dialogue = True, cutscenes[self.cutscene]["keys"][self.cs_key][2]
                  else: actor.active = False
                elif cutscenes[self.cutscene]["keys"][self.cs_key][0] == "number state":
                  if actor.type == cutscenes[self.cutscene]["keys"][self.cs_key][1]: actor.frame = cutscenes[self.cutscene]["keys"][self.cs_key][2]; self.cs_key += 1
                else: actor.active = False
                if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "wait": actor.active = False
                else: actor.speak()
              except: pass

        for interactable in self.interactables:
          interactable.update()
          if not interactable.alive: self.interactables.remove(interactable)
            
        for proj in self.projectiles: proj.update()
        self.projectiles = [proj for proj in self.projectiles if proj.alive]

        for actor in self.actors:
          if isinstance(actor, NPC):
            if actor.alive: actor.speak_minor()

        if self.saveable and not self.immobilize:
          if self.autosave_timer.timer(FPS * 30):
            try: self.save_game(); self.saving_works = True
            except Exception as e: self.saving_works = False; print(e)
          if self.autosave_timer.time <= FPS * 3:
            if self.saving_works: screen.blit(retrofontsmall.render('Saving in memory card...', True, 'White'), (3, HEIGHT-25)); screen.blit(retrofontsmall.render('Don\'t power off the console', True, 'White'), (3, HEIGHT-15))
            else: screen.blit(retrofontsmall.render('The system had trouble saving...', True, 'White'), (3, HEIGHT-25)); screen.blit(retrofontsmall.render('No memory card inserted', True, 'White'), (3, HEIGHT-15))
      else: self.player.update()
      if not self.immobilize: self.saveable = True
      else: self.saveable = False
    else:
      self.player.update()
      self.gameover_timer.count(FPS, 12, 0); self.projectiles.clear()
      if self.gameover_timer.tally == 0 and self.gameover_timer.time == 1: pygame.mixer.music.stop(); self.autosave_timer.reset()
      if self.gameover_timer.tally == 1 and self.gameover_timer.time == 1: pygame.mixer.music.load("Sounds/tracks/Defeat.mp3")
      if self.gameover_timer.tally == 1 and self.gameover_timer.time == 2: pygame.mixer.music.play(1, 0.0)
      if self.gameover_timer.tally >= 11: self.gamestate = 1; self.gameover_timer.reset(); self.end_game(False)
      screen.blit(retrofont.render("- Game Over -", False, "Yellow"), (30 + self.autosave_timer.oscillate(FPS / 4, 10, 0), 20))
      self.saveable = False

    if not self.immobilize: self.player.controls()
    else: self.player.movement = [0, 0]

    if self.player.hearts <= 0: self.immobilize = True
    if not self.immobilize: self.draw_ui()

    self.player.scroll()

    try:
      if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "enable":
        if cutscenes[self.cutscene]["keys"][self.cs_key][1] == "immobilize": self.immobilize = True; self.cs_key += 1
      if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "disable":
        if cutscenes[self.cutscene]["keys"][self.cs_key][1] == "immobilize": self.immobilize = False; self.cs_key += 1
      if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "end": self.cs_key = 0; self.cutscene = ""
      if cutscenes[self.cutscene]["keys"][self.cs_key][0] == "wait":
        if self.cs_wait_timer.timer(cutscenes[self.cutscene]["keys"][self.cs_key][1] * FPS) or k_debug: self.cs_key += 1; self.cs_wait_timer.reset()
    except: pass

    if self.transition_timer.tally != 0:
      screen = pygame.transform.scale(pygame.transform.scale(screen, (WIDTH - (self.transition_timer.tally * 15), HEIGHT - (self.transition_timer.tally * 15))), RESOLUTION)
      if not self.transition_2nd_half: self.transition_timer.count(1, WIDTH / 15, 1)
      else: self.transition_timer.subcount(1, 0, WIDTH / 15)
      if self.transition_timer.tally >= (WIDTH / 15) - 2: self.transition_2nd_half = True; self.load_map(self.traveling_to)
    else: self.transition_2nd_half = False; self.transition_timer.tally = 0

  def switch_map(self, place): self.transition_2nd_half = False; self.transition_timer.tally = 0; global k_debug; self.transition_timer.tally, self.traveling_to = 1, place; k_debug = False

  def draw_ui(self):
    pygame.draw.rect(screen, "Black", ((0, 0), (WIDTH, 20)))
    screen.blit(retrofontsmall.render("Hearts", False, "White"), (1, 1))
    for index in range(math.ceil(self.player.hearts)):
      screen.blit(heart, (64 + (index * 10), 4 - (self.heart_shake_timer.keep_count(2, 3, 1) * int(self.player.hearts <= 1.1)) ))
    for index, weapon in enumerate(self.player.items):
      if self.player.equiped_item == index: screen.blit(pygame.transform.scale(pygame.image.load(f"Assets/{weapon}.png").convert_alpha(), (18, 18)), (120 + (index * 16), -1 + self.item_float_timer.oscillate(4, 4, 1)))
      else: screen.blit(pygame.transform.scale(pygame.image.load(f"Assets/{weapon}.png").convert_alpha(), (18, 18)), (120 + (index * 16), 1))
    screen.blit(pygame.image.load("Assets/diamond/1.png").convert_alpha(), (220, 4))
    screen.blit(pygame.image.load("Assets/tuff/arrowback.png").convert_alpha(), (280, -2))
    screen.blit(retrofontsmall.render("× " + str(self.player.wealth), False, "White"), (240, 2))
    screen.blit(retrofontsmall.render("× " + str(self.player.arrows), False, "White"), (300, 2))

    for index, renk in enumerate(["renk 1", "renk 2", "renk 3", "renk 4"]):
      if self.player.renks[renk] and self.timer.tally >= 4: screen.blit(pygame.transform.scale(pygame.image.load(f"Assets/{renk}/{int(self.timer.wait(FPS / 2)) + 1}.png").convert_alpha(), (16, 16)), (275 + (index * 18), HEIGHT - 18))

  def set_player_standard(self): main.player.frame = 1; main.player.state = "stand"; main.player.movement = [0, 0]

  def load_map(self, place, alter_game=True):
    if self.traveling_to:
      l = {"Monster": [], "NPC": [], "Furniture": [], "Chest": [], "Collectible": [],}
      for actor in self.actors:
        if type(actor).__name__ == "Monster": l["Monster"].append(actor.__dict__())
        if type(actor).__name__ == "NPC": l["NPC"].append(actor.__dict__())
        if type(actor).__name__ == "Furniture": l["Furniture"].append(actor.__dict__())
        if type(actor).__name__ == "Chest": l["Chest"].append(actor.__dict__())
        if type(actor).__name__ == "Collectible": l["Collectible"].append(actor.__dict__())
      self.map_memory[self.place] = l

      if l == {"Monster": [], "NPC": [], "Furniture": [], "Chest": [], "Collectible": [],}: self.map_memory.pop(self.place)

    global k_a, k_b, k_right, k_left, k_up, k_down, k_select, k_start
    self.tiles.clear()
    self.actors.clear()
    self.interactables.clear()
    self.immobilize = False
    self.hide_player = False
    for y, mapx in enumerate(map[place]["layout"]):
      for x, tile in enumerate(mapx):
        self.tiles.append(Tile(tile, x, y))
        if not place in self.map_memory:
          if tile_types[tile]["entity"]: self.actors.append(Monster(tile_types[tile]["entity"], x * 25, y * 25))
          if tile_types[tile]["npc"]: self.actors.append(NPC(tile_types[tile]["npc"], x * 25, y * 25))
          if tile_types[tile]["item"]: self.actors.append(Collectible(tile_types[tile]["item"], x * 25, y * 25))
          if tile_types[tile]["asset"]: self.actors.append(Chest(tile_types[tile]["asset"], x * 25, y * 25, tile))
          if tile_types[tile]["furniture"]: self.actors.append(Furniture(tile, x * 25, y * 25))
          
    if place in self.map_memory:
      self.actors.clear()
      for s in self.map_memory[place]["Monster"]:
        t = Monster(s["type"], s["x"], s["y"])
        t.frame, t.state = s["frame"], s["state"]
        t.flipped, t.hearts = s["flipped"], s["hearts"]
        t.solid = s["solid"]; t.alive = s["alive"]
        self.actors.append(t)
      for s in self.map_memory[place]["NPC"]:
        t = NPC(s["type"], s["x"], s["y"])
        t.frame, t.state = s["frame"], s["state"]
        t.flipped, t.hearts = s["flipped"], s["hearts"]
        t.solid = s["solid"]; t.alive = s["alive"]
        self.actors.append(t)
      for s in self.map_memory[place]["Furniture"]:
        t = Furniture(s["tile"], s["x"], s["y"])
        t.frame, t.state = s["frame"], s["state"]
        t.solid = s["solid"]; t.alive = s["alive"]
        self.actors.append(t)
      for s in self.map_memory[place]["Chest"]:
        t = Chest(s["type"], s["x"], s["y"], "")
        t.frame, t.state = s["frame"], s["state"]
        t.solid = s["solid"]; t.dug = s["dug"]; t.alive = s["alive"]
        self.actors.append(t)
      for s in self.map_memory[place]["Collectible"]:
        t = Collectible(s["type"], s["x"], s["y"])
        t.frame, t.state = s["frame"], s["state"]
        t.solid = s["solid"]; t.alive = s["alive"]
        self.actors.append(t)

    if alter_game:
      if self.from_edge:
        if type(self.from_edge) == str:
          self.player.dir = map[self.place][self.from_edge]["dir"]
          self.player.rect.x, self.player.rect.y = (map[self.place][self.from_edge]["spawn"][0] * 25) - 18, map[self.place][self.from_edge]["spawn"][1] * 25
          self.player.state, self.player.frame = "stand", 1
          self.cutscene = map[self.place][self.from_edge]["cutscene"]
        else:
          self.player.dir = transportations[place]["dir"]
          self.player.rect.x, self.player.rect.y = (transportations[place]["spawn"][0] * 25) - 18, transportations[place]["spawn"][1] * 25
          self.player.state, self.player.frame = "stand", 1
          self.cutscene = transportations[place]["cutscene"]
      self.place = place
      self.traveling_to = ""
      self.from_edge = ""
      self.cs_key = 0
      k_a, k_b, k_right, k_left, k_up, k_down, k_select, k_start = False, False, False, False, False, False, False, False
      if map[place]["track"]:
        if self.theme != map[place]["track"]:
          pygame.mixer.music.load(f"Sounds/tracks/{map[place]['track']}.mp3"); pygame.mixer.music.play(-1, 0.0)
          self.theme = map[place]["track"]
      else: pygame.mixer.music.stop()

    for tile in self.tiles:
      if tile.id == "ab": self.interactables.append(Interactable(tile.rect.x, tile.rect.y, "sailboat right"))
      if tile.id == "bä": self.interactables.append(Interactable(tile.rect.x, tile.rect.y, "sailboat left"))
  
  def load_game(self):
    self.gamestate = 4
    self.player = Player()
    self.timer.reset()
    self.autosave_timer.reset()
    try: self.load_save()
    except Exception as e: print(e)
    self.load_map(self.place)
    #pygame.mixer.music.load(f"Sounds/tracks/{self.theme}.mp3")

  def load_save(self):
    global saves
    if saves[self.save]["started"]:
      with open("Saves/memory_card/savefile.txt", "r") as savefile: saves = json.load(savefile)
      self.actors = []
      self.player.rect.x, self.player.rect.y = saves[self.save]["x"], saves[self.save]["y"]
      self.scrolls = saves[self.save]["scroll"]
      self.place = saves[self.save]["place"]
      self.player.dir = saves[self.save]["direction"]
      self.player.hearts = saves[self.save]["hearts"]
      self.player.wealth = saves[self.save]["wealth"]
      self.player.item = saves[self.save]["weapon"]
      self.player.items = saves[self.save]["items"]
      self.player.arrows = saves[self.save]["arrows"]
      self.player.renks = saves[self.save]["renks"]
      self.map_memory = saves[self.save]["actors"]

  def save_game(self):
    global saves
    if not main.immobilize:
      open("Saves/memory_card/savefile.txt", "r")
      saves[self.save]["name"] = self.savename
      saves[self.save]["started"] = True
      saves[self.save]["x"], saves[self.save]["y"] = self.player.rect.x, self.player.rect.y
      saves[self.save]["scroll"] = self.scrolls
      saves[self.save]["place"] = self.place
      saves[self.save]["direction"] = self.player.dir
      saves[self.save]["hearts"] = self.player.hearts
      saves[self.save]["wealth"] = self.player.wealth
      saves[self.save]["weapon"] = self.player.item
      saves[self.save]["items"] = self.player.items
      saves[self.save]["arrows"] = self.player.arrows
      saves[self.save]["renks"] = self.player.renks
      l = {"Monster": [], "NPC": [], "Furniture": [], "Chest": [], "Collectible": [],}
      for actor in self.actors:
        if type(actor).__name__ == "Monster": l["Monster"].append(actor.__dict__())
        if type(actor).__name__ == "NPC": l["NPC"].append(actor.__dict__())
        if type(actor).__name__ == "Furniture": l["Furniture"].append(actor.__dict__())
        if type(actor).__name__ == "Chest": l["Chest"].append(actor.__dict__())
        if type(actor).__name__ == "Collectible": l["Collectible"].append(actor.__dict__())
      self.map_memory[self.place] = l
      saves[self.save]["actors"] = self.map_memory

      try:
        with open("Saves/memory_card/savefile.txt", "w") as out_: json.dump(saves, out_)
      except: print("Saving failed.")
    else: print("Saving failed: A cutscene was playing.")

  def end_game(self, save_game=True):
    pygame.mixer.music.stop()
    #if save_game and self.saveable: main.save_game()
    self.actors.clear()
    self.map_memory = {}
    self.tiles = []
    self.timer.reset()
    self.cutscene = ""
    self.immobilize = False
    self.cs_key = 0
    
  def quit(self, save_game=True):
    global saves
    #try: self.save_game()
    #except: print("Loading failed.")
    try:
      if save_game and self.saveable: self.save_game()
    except FileNotFoundError: print("Save file not found.")
    except EOFError: print("Save file is empty or invalid.")
    except Exception as e: print("An error occurred in saving:", str(e))
    pygame.quit()
    exit()
      

class Player:
  def __init__(self):
    self.rect = pygame.Rect((WIDTH / 2, HEIGHT / 2), (15, 15))
    self.speed = 3
    self.timer = Timer()
    self.hit_timer = Timer()
    self.dir = "front"
    self.state = "stand"
    self.frame = 1
    self.movement = [0, 0]
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.enemy_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.image = pygame.image.load(f"Assets/tuff/{self.state} {self.dir} {self.frame}.png").convert_alpha()
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.wealth = 50
    self.solid = True

    self.hearts = 5
    self.equiped_item = 0
    self.items = ["sword", "bow"]
    self.arrows = 300
    self.renks = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}
    try: self.item = self.items[self.equiped_item]
    except: print("Tuff has no weapons!?")

  def update(self):
    try: self.image = pygame.image.load(f"Assets/tuff/{self.state} {self.dir} {self.frame}.png").convert_alpha()
    except: self.frame = 1
    if self.hit_timer.time:
      self.image.fill("White", special_flags=pygame.BLEND_RGB_MAX)
      self.hit_timer.wait(FPS / 8)
    if not main.hide_player: screen.blit(self.image, ((self.rect.x - 5) - (int(self.state == "sword" and self.dir == "left" and self.frame >= 2) * 5) - main.scrolls[0], (self.rect.y - 10) - main.scrolls[1]))
    if k_select:
      self.equiped_item += 1
      if self.equiped_item >= len(self.items): self.equiped_item = 0
      self.item = self.items[self.equiped_item]
    #pygame.draw.rect(screen, "Blue", self.rect, 2)
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    #self.rect.x -= main.scrolls[0]; self.rect.y -= main.scrolls[1]

    self.rect, self.collision = self.move(self.rect, self.movement, main.tiles + [actor for actor in main.actors if isinstance(actor, Furniture)] + [actor for actor in main.actors if (not isinstance(actor, Monster) or (self.state != "grapple hook"))])

    for proj in main.projectiles:
      if self.rect.colliderect(proj.rect) and not isinstance(proj, Arrow) and not isinstance(proj, Grapple) and not isinstance(proj, Shovel):
        proj.alive = False
        self.hearts -= proj.damage
        self.hit_timer.time = 1
        hurt_sfx.play()
        if self.hearts <= 0: main.timer.reset()

    if self.hearts > 5: self.hearts = 5
    self.speed = 3 + (int(k_debug) * 30)

  def scroll(self):
    tilemaxx = 0
    for tile in main.tiles:
      if tile.rect.x > tilemaxx: tilemaxx = (tile.rect.x - WIDTH) + 25
    tilemaxy = 0
    for tile in main.tiles:
      if tile.rect.y > tilemaxy: tilemaxy = (tile.rect.y - HEIGHT) + 25

    main.scrolls[0] = maxint(minint(self.rect.x - WIDTH / 2, 0), tilemaxx)
    main.scrolls[1] = maxint(minint(self.rect.y - HEIGHT / 2, 0), tilemaxy)
    
    if self.rect.x > tilemaxx + WIDTH - 15 and main.traveling_to != map[main.place]["right"]["place"] and map[main.place]["right"]["place"]: main.from_edge = "right"; main.switch_map(map[main.place]["right"]["place"])
    if self.rect.x < 0 and main.traveling_to != map[main.place]["left"]["place"] and map[main.place]["left"]["place"]: main.from_edge = "left"; main.switch_map(map[main.place]["left"]["place"])
    if self.rect.y > tilemaxy + HEIGHT and main.traveling_to != map[main.place]["bottom"]["place"] and map[main.place]["bottom"]["place"]: main.from_edge = "bottom"; main.switch_map(map[main.place]["bottom"]["place"])
    if self.rect.y < 0 and main.traveling_to != map[main.place]["top"]["place"] and map[main.place]["top"]["place"]: main.from_edge = "top"; main.switch_map(map[main.place]["top"]["place"])

    self.rect.x = minint(self.rect.x, 0)
    self.rect.x = maxint(self.rect.x, tilemaxx + WIDTH - 15)
    self.rect.y = minint(self.rect.y, 0)
    self.rect.y = maxint(self.rect.y, tilemaxy + HEIGHT)

  def controls(self):
    global k_a
    if self.state != self.item:
      if k_right or k_left or k_up or k_down: self.state = "walk"; self.frame = self.timer.keep_count(FPS / 5, 3, 1)
      if k_right: self.movement[0] = self.speed; self.dir = "right"
      elif k_left: self.movement[0] = -self.speed; self.dir = "left"
      else: self.movement[0] = 0
      if k_up: self.movement[1] = -self.speed; self.dir = "back"
      elif k_down: self.movement[1] = self.speed; self.dir = "front"
      else: self.movement[1] = 0
      if not k_right and not k_left and not k_up and not k_down: self.movement = [0, 0]; self.state, self.frame = "stand", 1
      if k_a and self.items != [] and ((self.item == "bow" and self.arrows > 0) or self.item != "bow") and (self.item != "healing potion" and self.item != "healing capsule" and self.item != "grapple hook"): self.state = self.item; self.frame = 1
      if k_a and self.item == "healing potion": collect4_sfx.play(); self.hearts += 2; self.items.remove(self.item); k_a = False; self.item = self.items[0]
      if k_a and self.item == "healing capsule": collect4_sfx.play(); self.hearts += 1; self.items.remove(self.item); k_a = False; self.item = self.items[0]
      if k_a and self.item == "grapple hook": grappling_sfx.play(); main.projectiles.append(Grapple(self.rect.x, self.rect.y, self.dir, self)); self.state = self.item
    if self.state == self.item:
      if self.state != "grapple hook":
        self.frame = self.timer.count(FPS / 10, 4, 0)
        if self.state == "sword" and self.frame == 2 and self.timer.time == 1: sword_sfx.play()
        if self.state == "shovel" and self.frame == 2 and self.timer.time == 1: main.projectiles.append(Shovel(self.rect.x - 4, self.rect.y - 4, self.dir))
        self.movement = [0, 0]
        if self.state != "shovel":
          if self.timer.tally == 4:
            main.projectiles.append(Arrow(self.rect.x - 4, self.rect.y - 4, self.dir, self.item != "bow", self.item == "adham sword"))
            if self.item == "bow": self.arrows -= 1
        if self.timer.tally == 4: self.state = "stand"; self.frame = 1; self.timer.reset()
      else: self.frame = 1

  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]

    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if tile.solid and not k_debug:
        if movement[0] > 0:
          rect.right = tile.rect.left
          collision_type['right'] = True
        elif movement[0] < 0:
          rect.left = tile.rect.right
          collision_type['left'] = True
      if type(tile) == Tile:
        if tile.transport and main.from_edge != tile: main.from_edge = tile; main.switch_map(transportations[tile.transport]["place"])
    
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if tile.solid and not k_debug:
        if movement[1] > 0:
          rect.bottom = tile.rect.top
          collision_type['bottom'] = True
        elif movement[1] < 0:
          rect.top = tile.rect.bottom
          collision_type['top'] = True

    return rect, collision_type
  
  def get_hit(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if movement[0] > 0: collision_type['right'] = True
      elif movement[0] < 0: collision_type['left'] = True
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if movement[1] > 0: collision_type['bottom'] = True
      elif movement[1] < 0: collision_type['top'] = True
    return rect, collision_type


class Tile:
  def __init__(self, tile, x, y):
    self.type = tile_types[tile]
    self.rect = pygame.Rect((x * 25, y * 25), (25, 25))
    self.image = pygame.image.load("Assets/tiles/" + tile_types[tile]["name"] + ".png").convert_alpha()
    self.name = tile_types[tile]["name"]
    self.solid = tile_types[tile]["solid"]
    self.front = tile_types[tile]["front"]
    self.id = tile
    self.transport = tile_types[tile]["transport_to"]
    self.wave_timer = Timer()
    if self.transport: self.rect.x += 4; self.rect.width -= 8; self.rect.y += 4; self.rect.height -= 8

  def update(self):
    #self.rect.x += main.scrolls[0]; self.rect.y += main.scrolls[1]
    if self.name == "water" or self.name == "salty water":
      if self.rect.y % 2 == 0: self.wave_timer.keep_count(1, 25, 0)
      else: self.wave_timer.subcount(1, 0, 25)
    if self.name == "water": self.image = pygame.image.load("Assets/tiles/water.png").convert_alpha(); self.image.blit(wave, (self.wave_timer.tally, 0)); self.image.blit(wave, (self.wave_timer.tally - 25, 0))
    if self.name == "salty water": self.image = pygame.image.load("Assets/tiles/salty water.png").convert_alpha(); self.image.blit(wave_light, (self.wave_timer.tally, 0)); self.image.blit(wave_light, (self.wave_timer.tally - 25, 0))
    screen.blit(self.image, ((self.rect.x - main.scrolls[0]) - (int(bool(self.transport)) * 4), (self.rect.y - main.scrolls[1]) - (int(bool(self.transport)) * 4)))
    #pygame.draw.rect(screen, "Red", self.rect, 2)


class Furniture:
  def __init__(self, tile, x, y):
    self.type = tile_types[tile]["furniture"]
    self.tile = tile
    self.rect = pygame.Rect((x, y), (25, 25))
    self.image = pygame.image.load("Assets/tiles/" + tile_types[tile]["furniture"] + ".png").convert_alpha()
    try: self.image_top = pygame.image.load("Assets/tiles/" + tile_types[tile]["furniture"] + " top.png").convert_alpha()
    except FileNotFoundError: self.image_top = None
    self.state = ""
    self.frame = 1
    self.solid = True
    self.alive = True

  def update(self):
    #self.rect.x += main.scrolls[0]; self.rect.y += main.scrolls[1]
    screen.blit(self.image, (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))
    #pygame.draw.rect(screen, "Red", self.rect, 2)

  def draw_top(self):
    if self.image_top != None: screen.blit(self.image_top, (self.rect.x - main.scrolls[0], (self.rect.y - main.scrolls[1]) - self.rect.height))

  def __dict__(self):
    return {"x": self.rect.x, "y": self.rect.y, "frame": self.frame, "state": self.state, "type": self.type, "tile": self.tile, "solid": self.solid, "alive": self.alive}


class Monster:
  def __init__(self, type, x, y):
    self.rect = pygame.Rect((x, y), (25 / (int(type == "madpuff weak") + 1), 25 / (int(type == "madpuff weak") + 1)))
    self.type = type
    self.speed = monster_types[self.type]["speed"]
    self.timer = Timer()
    self.dirx = "stay"
    self.diry = "stay"
    if self.type == "sharpy": self.diry = ["left", "right"][random.randrange(0, 2)]
    self.solid = True
    self.state = "walk"
    self.frame = 1
    self.movement = [0, 0]
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.enemy_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha()
    self.flipped = False
    self.shoot_timer = Timer()
    self.hit_timer = Timer()
    self.hearts = monster_types[self.type]["hearts"]
    self.object = "monster"
    self.alive = True
    self.hop_timer = Timer()
    self.hopping = 0
    if self.type == "regalios": self.flipped = bool(random.randrange(0, 2))
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def __str__(self):
    return f"{self.rect}, {self.alive}, {self.type}, {self.state}, {self.hearts}"

  def update(self):
    try:
      if self.type != "madpuff weak": self.image = pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False)
      elif self.type == "madpuff weak": self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False), (16, 16))
    except: self.frame = 1
    #screen.blit(retrofontsmall.render(str(self), False, "White"), (self.rect.x, self.rect.y - 10))
    if self.hit_timer.time:
      self.image.fill("White", special_flags=pygame.BLEND_RGB_MAX)
      self.hit_timer.wait(FPS / 8)
    screen.blit(self.image, (self.rect.x - main.scrolls[0], (self.rect.y - self.hopping) - main.scrolls[1]))
    if self.hearts > 0:
      #pygame.draw.rect(screen, "Blue", self.rect, 2)
      #self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
      #self.rect.x -= main.scrolls[0]; self.rect.y -= main.scrolls[1]
      #if self.rect.x > WIDTH: self.rect.x = 0; main.minimaps[0] += 1; main.load_map()
      #if self.rect.x < -32: self.rect.x = WIDTH; main.minimaps[0] -= 1; main.load_map()
      #if self.rect.y > HEIGHT: self.rect.y = 0; main.minimaps[1] += 1; main.load_map()
      #if self.rect.y < -32: self.rect.y = HEIGHT; main.minimaps[1] -= 1; main.load_map()
      if self.hop_timer.tally <= 2:
        if self.type != "regalios":
          if self.dirx == "right": self.flipped = False
          if self.dirx == "left": self.flipped = True

        if self.type == "croaker" or self.type == "xroaker": self.state, self.frame = "jump", 1

        if self.type != "regall" and self.type != "yuma" and self.type != "regalios": self.rect, self.collision = self.move(self.rect, self.movement, main.tiles + main.actors + [main.player])

        if self.collision["bottom"]: self.diry = "back"
        if self.collision["top"]: self.diry = "front"
        if self.collision["left"]: self.dirx = "right"
        if self.collision["right"]: self.dirx = "left"

        if self.type != "sharpy":
          if self.rect.x > main.player.rect.x:
            self.dirx = "left"
            if self.rect.x - 45 < main.player.rect.x: self.dirx = "stay"
          if self.rect.x < main.player.rect.x:
            self.dirx = "right"
            if self.rect.x + 45 > main.player.rect.x: self.dirx = "stay"
          if self.rect.y > main.player.rect.y:
            self.diry = "back"
            if self.rect.y - 45 < main.player.rect.y: self.diry = "stay"
            else: self.stayy = False
          if self.rect.y < main.player.rect.y:
            self.diry = "front"
            if self.rect.y + 45 > main.player.rect.y: self.diry = "stay"
          
        if self.type != "regalios":
          if self.dirx == "right":
            self.movement[0] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          elif self.dirx == "left":
            self.movement[0] = -self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          else: self.movement[0] = 0
          if self.diry == "back":
            self.movement[1] = -self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          elif self.diry == "front":
            self.movement[1] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          else: self.movement[1] = 0
        
      else:
        if self.type == "croaker" or self.type == "xroaker": self.state, self.frame = "idle", self.timer.keep_count(FPS / 13, 1, 3)

      if self.type == "croaker" or self.type == "xroaker":
        self.hop_timer.keep_count(FPS / 4, 5, 0)
        if self.hop_timer.tally == 1: self.hopping += self.hop_timer.time * 1.5
        if self.hop_timer.tally == 2: self.hopping -= self.hop_timer.time * 1.5
      else: self.hop_timer.tally = 1

      if self.type == "regalios":
        self.frame = self.timer.keep_count(2, 26, 1)
        if self.state == "attack": self.state = "walk"

      proj_angle = math.atan2(self.rect.centery - main.player.rect.centery, self.rect.centerx - main.player.rect.centerx)

      if self.shoot_timer.timer(FPS * (3 - (int(self.type == "madpuff renk") * 2.2))): self.state = "attack"; self.frame = 1; main.projectiles.append(Projectile(self.rect.x, self.rect.y, proj_angle, monster_types[self.type]["can shoot"]))

      for proj in main.projectiles:
        if self.rect.colliderect(proj.rect) and not isinstance(proj, Projectile) and not isinstance(proj, Shovel):
          if not isinstance(proj, Grapple):
            proj.alive = False
            self.hearts -= proj.damage
            self.hit_timer.time = 1
            hit_sfx.play()
            if proj.not_bow:
              if self.rect.y + 30 > main.player.rect.y and self.rect.y - 30 < main.player.rect.y:
                if self.rect.x >= main.player.rect.x: self.movement[0] = 15
                elif self.rect.x <= main.player.rect.x and self.rect.y + 30 > main.player.rect.y: self.movement[0] = -15
          if self.rect.x + 30 > main.player.rect.x and self.rect.x - 30 < main.player.rect.x:
            if self.rect.y >= main.player.rect.y: self.movement[1] = 15
            elif self.rect.y <= main.player.rect.y: self.movement[1] = -15
          if isinstance(proj, Grapple):
            if proj.retract:
              if proj.length > 40:
                self.hearts -= 1
                self.hit_timer.time = 1
                grapple_sfx.play()
              if proj.length > 15: self.rect.x, self.rect.y = proj.rect.x, proj.rect.y

    else:
      self.state = "defeat"
      self.frame = self.timer.tally
      self.alive = not self.timer.timer(4)
      if not self.alive and monster_types[self.type]["drop"] != "": main.actors.append(Collectible(monster_types[self.type]["drop"], self.rect.x + 8, self.rect.y + 8))
      if self.timer.time == 2: kill_sfx.play()
      self.solid = False

  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]

    if self.type != "sharpy":
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if tile.solid and tile is not self:
          if movement[0] > 0:
            rect.right = tile.rect.left
            collision_type['right'] = True
          elif movement[0] < 0:
            rect.left = tile.rect.right
            collision_type['left'] = True
    
      rect.y += movement[1]
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if tile.solid and tile is not self:
          if movement[1] > 0:
            rect.bottom = tile.rect.top
            collision_type['bottom'] = True
          elif movement[1] < 0:
            rect.top = tile.rect.bottom
            collision_type['top'] = True
    else:
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if not tile.solid and tile is not self:
          if movement[0] > 0:
            rect.right = tile.rect.left
            collision_type['right'] = True
          elif movement[0] < 0:
            rect.left = tile.rect.right
            collision_type['left'] = True
      if self.hop_timer.wait(FPS): self.dirx = "right"
      else: self.dirx = "left"

    return rect, collision_type
  
  def __dict__(self):
    return {"x": self.rect.x, "y": self.rect.y, "frame": self.frame, "state": self.state, "type": self.type, "flipped": self.flipped, "hearts": self.hearts, "solid": self.solid, "alive": self.alive}
  

class Chest:
  def __init__(self, type, x, y, tile):
    self.type = type
    self.state = "closed"
    self.rect = pygame.Rect((x, y), (25, 25))
    self.frame = 1
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}.png").convert_alpha()
    self.solid = True
    self.contents = container_types[self.type]["contents"]
    #self.sound = container_types[self.type]["sound"]
    self.object = "container"
    self.alive = True
    self.dug = True
    self.dig_level = 0
    self.hit_timer = Timer()
    if tile == "rx": self.dug = False
    if tile == "rX": self.dug = False
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1
  
  def __str__(self): return f"{self.rect}, {self.alive}, {self.type}, {self.state}"
  
  def update(self):
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}.png").convert_alpha()
    if self.hit_timer.time:
      self.image.fill("White", special_flags=pygame.BLEND_RGB_MAX)
      self.hit_timer.wait(FPS / 8)
    if self.dug:
      screen.blit(self.image, (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))
      for proj in main.projectiles:
        if self.rect.colliderect(proj.rect) and isinstance(proj, Arrow) and self.state == "closed":
          proj.alive = False
          self.state = "open"
          self.solid = False
          container_types[self.type]["sound"].play()
          for prize in self.contents: main.actors.append(Collectible(prize, self.rect.x + 8, self.rect.y + 8))
    else:
      for proj in main.projectiles:
        if self.rect.colliderect(proj.rect) and isinstance(proj, Shovel) and proj.alive:
          self.dig_level += 1
          self.hit_timer.time = 1
          dig_sfx.play()
          proj.alive = False
    if self.dig_level >= 5 and not self.dug: self.dug = True; dug_sfx.play()

  def __dict__(self):
    return {"x": self.rect.x, "y": self.rect.y, "frame": self.frame, "state": self.state, "type": self.type, "solid": self.solid, "dug": self.dug, "alive": self.alive}


class NPC:
  def __init__(self, type, x, y):
    self.type = type
    self.rect = pygame.Rect((x, y), (25, 25))
    if self.type == "vike": self.rect.y -= 6
    self.frame = 1
    self.state = None
    self.flipped = False
    self.hearts = 1
    self.image = pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha(), self.flipped, False)
    self.solid = True
    #self.contents = []
    #if npcs[self.type]["content"] != "": self.contents = [Collectible(npcs[self.type]["content"], self.rect.x + npcs[self.type]["item x relative to npc"], self.rect.y + npcs[self.type]["item y relative to npc"])]
    self.full_dialogue = ""
    self.dialogue = ""
    self.text_timer = Timer()
    self.object = "npc"
    self.alive = True
    self.timer = Timer()
    self.behavior_timer = Timer()
    self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha()
    self.active = False
    self.set_heard = False
    self.text_index = 0
    self.press_a_timer = Timer()
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def __str__(self): return f"{self.rect}, {self.alive}, {self.type}"
  
  def update(self):
    global k_a, k_start, k_right
    screen.blit(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha(), self.flipped, False), (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))

    #for item in self.contents:
    #  if item.alive: item.update()
    #  else:
    #    self.contents.remove(item); self.frame = 3; self.contents = []
    #    if npcs[self.type]["text 2"] != "": self.full_dialogue = npcs[self.type]["text 2"]; self.dialogue = ""; self.text_timer.reset()

  def speak(self):
    global k_debug
    if self.active:
      pygame.draw.rect(screen, "Black", ((0, 275), (WIDTH, 75))), pygame.draw.rect(screen, "White", ((0, 275), (WIDTH, 75)), 2), pygame.draw.line(screen, "White", (0, 292), (WIDTH, 292), 2), screen.blit(retrofonttiny.render(self.type.capitalize(), False, "White"), (15, 277))
      try: self.dialogue += self.full_dialogue[self.text_timer.tally]
      except IndexError:
        screen.blit(retrofonttiny.render("Press A >", False, "White"), (265 + ((self.press_a_timer.oscillate(1, 10, 0) * (self.press_a_timer.tally / 1.5)) / 5), 335))
        if k_a or k_start: main.cs_key += 1; self.dialogue = ""; self.full_dialogue = ""; self.text_timer.reset()
      self.text_timer.count(1, len(self.full_dialogue), 0), screen.blit(retrofontsmall.render(self.dialogue, False, "White", wraplength=WIDTH - 9), (3, 294))
      if k_debug: main.cs_key += 1; self.dialogue = ""; self.full_dialogue = ""; self.text_timer.reset(); k_debug = False

  def speak_minor(self):
    if main.player.rect.x > self.rect.x - 100 and main.player.rect.x < self.rect.x + 100 and main.player.rect.y > self.rect.y - 100 and main.player.rect.y < self.rect.y + 100:
      if self.type == "fidda": self.frame = 1
      if self.type in npcs:
        pygame.draw.rect(screen, "Black", ((0, 275), (WIDTH, 75))), pygame.draw.rect(screen, "White", ((0, 275), (WIDTH, 75)), 2), pygame.draw.line(screen, "White", (0, 292), (WIDTH, 292), 2), screen.blit(retrofonttiny.render(self.type.capitalize(), False, "White"), (15, 277))
        if not self.set_heard: self.dialogue = ""; self.full_dialogue = npcs[self.type][0] + " "; self.text_timer.reset()
        self.set_heard = True
        self.dialogue += self.full_dialogue[self.text_timer.tally]
        self.text_timer.count(1, len(self.full_dialogue) - 1, 0), screen.blit(retrofontsmall.render(self.dialogue, False, "White", wraplength=WIDTH - 9), (3, 294))
    else:
      self.set_heard = False
      if self.type == "fidda": self.frame = 2

  def __dict__(self):
    return {"x": self.rect.x, "y": self.rect.y, "frame": self.frame, "state": self.state, "type": self.type, "flipped": self.flipped, "hearts": self.hearts, "solid": self.solid, "alive": self.alive}


class Interactable:
  def __init__(self, x, y, object):
    self.rect = pygame.Rect((x, y), (25, 25))
    self.frame = 1
    self.state = None
    self.object = object
    self.image = pygame.image.load("Assets/" + self.object + "/1.png").convert_alpha()
    self.solid = True
    self.alive = True
    self.timer = Timer()
    self.x_vel = 0
    self.y_vel = 0
    if self.object == "sailboat right": self.rect.x += 5; self.rect.width, self.rect.height = 50, 50
    if self.object == "sailboat left": self.rect.x -= 5; self.rect.width, self.rect.height = 50, 50
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def update(self):
    self.image = pygame.image.load("Assets/" + self.object + "/" + str(self.timer.keep_count(FPS / 5, 3, 1)) + ".png").convert_alpha()
    screen.blit(self.image, (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))
    #pygame.draw.rect(screen, "Red", self.rect, 2)
    if self.object == "sailboat right":
      # if player is close to the sailboat, show the "Press A to board" message
      if (self.rect.x + (self.rect.width / 2)) - 50 < main.player.rect.x < (self.rect.x + (self.rect.width / 2)) + 50 and (self.rect.y + (self.rect.height / 2)) - 50 < main.player.rect.y < (self.rect.y + (self.rect.height / 2)) + 50:
        screen.blit(retrofontsmall.render("Press A to Board", False, "White"), (2, 20))
        if k_a or k_start: self.object = "sailboat right boarded"; main.hide_player = True; main.immobilize = True; main.set_player_standard()

    if self.object == "sailboat right boarded":
      main.player.rect.x, main.player.rect.y = self.rect.x + 5, self.rect.y + 25
      if self.x_vel < 5: self.x_vel += 0.05
      self.rect.x += self.x_vel

    if self.object == "sailboat left":
      # if player is close to the sailboat, show the "Press A to board" message
      if (self.rect.x + (self.rect.width / 2)) - 50 < main.player.rect.x < (self.rect.x + (self.rect.width / 2)) + 50 and (self.rect.y + (self.rect.height / 2)) - 50 < main.player.rect.y < (self.rect.y + (self.rect.height / 2)) + 50:
        screen.blit(retrofontsmall.render("Press A to Board", False, "White"), (2, 20))
        if k_a or k_start: self.object = "sailboat left boarded"; main.hide_player = True; main.immobilize = True; main.set_player_standard()

    if self.object == "sailboat left boarded":
      main.player.rect.x, main.player.rect.y = self.rect.x + 5, self.rect.y + 25
      if self.x_vel > -5: self.x_vel -= 0.05
      self.rect.x += self.x_vel

  def __str__(self): return f"{self.rect}, {self.alive}, {self.object}"


class Collectible:
  def __init__(self, type, x, y):
    self.type = type
    self.rect = pygame.Rect((x, y), (13, 13))
    self.frame = 1
    self.state = None
    self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png")
    self.timer = Timer()
    self.value = collictible_types[self.type]["value"]
    self.arrow = collictible_types[self.type]["arrow"]
    self.heart = collictible_types[self.type]["heart"]
    self.price = collictible_types[self.type]["price"]
    self.title = collictible_types[self.type]["title"]
   #self.sound = collictible_types[self.type]["sound"]
    self.paid = 0
    self.bought = False
    self.solid = False
    self.object = "collectible"
    self.held = False
    self.alive = type != ""
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def update(self):
    if not self.bought:
      self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png")
      if not self.held: screen.blit(self.image, (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))
      if self.price > 0: screen.blit(retrofontsmall.render(str(self.price) + " Liras", False, "White"), ((self.rect.x - 20) - main.scrolls[0], (self.rect.y + 20) - main.scrolls[1]))
      self.frame = int(self.timer.wait(FPS / (16 - (self.type == "arrow" * 15)))) + 1

      if self.rect.colliderect(main.player.rect) and main.player.wealth >= self.price:
        if type(self.value) == int: main.player.wealth += self.value
        elif not self.held: main.player.items.append(self.value)
        main.player.arrows += self.arrow
        main.player.hearts += self.heart
        if collictible_types[self.type]["sound"] != "":
          if self.title == "": collictible_types[self.type]["sound"].play(); self.bought = True
          else:
            if not self.held: pygame.mixer.music.load(f"Sounds/tracks/{collictible_types[self.type]['sound']}.mp3"); pygame.mixer.music.play(1, 0.0)
            self.held = True
            main.immobilize = True
            main.player.dir = "front"
            if self.frame - 1 or pygame.mixer.music.get_pos() / 1000 > 1.5: screen.blit(retrofont.render(self.title, False, "White"), (3, 2))
            if pygame.mixer.music.get_pos() / 1000 < 4.8:
              if   self.type == "renk 1": main.player.state = "holdred"; main.player.renks[self.type] = True
              elif self.type == "renk 2": main.player.state = "holdyellow"; main.player.renks[self.type] = True
              elif self.type == "renk 3": main.player.state = "holdgreen"; main.player.renks[self.type] = True; main.theme = "Sword of Adham"
              elif self.type == "renk 4": main.player.state = "holdblue"; main.player.renks[self.type] = True; main.theme = "Waves and Flutters"
              elif self.type == "adham sword": main.player.state = "holdsword"; main.player.renks[self.type] = True
            else: main.player.state = "walk"; main.player.frame = 0
            if not pygame.mixer.music.get_busy():
              self.bought = True
              if self.type != "renk 4": pygame.mixer.music.load(f"Sounds/tracks/{main.theme}.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False; main.player.frame = 1
              else:
                for actor in [actor for actor in main.actors if actor.type == "naman 3"]: actor.rect.y = 1
        else: self.bought = True
          
      for proj in main.projectiles:
        if isinstance(proj, Grapple) and self.price <= 0:
          if proj.retract and self.rect.colliderect(proj.rect):
            if proj.length > 40: grapple_sfx.play()
            if proj.length > 15: self.rect.x, self.rect.y = proj.rect.x, proj.rect.y

    else:
      if self.price: self.pay()
      else: self.alive = False

  def pay(self):
    if not self.paid > self.price: main.player.wealth -= 1; self.paid += 1; change_by_sfx.play()
    if not self.paid > self.price - 15: main.player.wealth -= 10; self.paid += 10
    self.alive = not self.paid >= self.price

  def __dict__(self):
    return {"x": self.rect.x, "y": self.rect.y, "frame": self.frame, "state": self.state, "type": self.type, "paid": self.paid, "bought": self.bought, "solid": self.solid, "alive": self.alive}
  

class Projectile:
  def __init__(self, x, y, angle, can_shoot, damage=0.5):
    self.rect = pygame.Rect((x, y), (13, 13))
    self.colors = [(250, 0, 0), (200, 15, 0), (180, 30, 0), (140, 45, 0), (180, 30, 0), (200, 15, 0)]
    self.speed = 5
    self.damage = damage
    self.dirx = self.speed * math.cos(angle)
    self.diry = self.speed * math.sin(angle)
    self.lifetime = 4 - ((not can_shoot) * 3.9)
    self.timer = Timer()
    self.color_timer = Timer()
    self.can_shoot = can_shoot
    self.alive = True

  def update(self):
    if self.can_shoot: pygame.draw.rect(screen, self.colors[self.color_timer.keep_count(2, len(self.colors), 0)], ((self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]), (self.rect.width, self.rect.height)), border_radius=6)
    self.rect.move_ip(-self.dirx, -self.diry)
    if not self.can_shoot: self.rect.move_ip(-self.dirx, -self.diry); self.rect.move_ip(-self.dirx, -self.diry); self.rect.move_ip(-self.dirx, -self.diry)
    if self.timer.timer(self.lifetime * FPS): self.alive = False


class Arrow:
  def __init__(self, x, y, dir, other_weapon=False, adham_sword=False):
    self.image = pygame.image.load(f"Assets/tuff/arrow{dir}.png").convert_alpha()
    self.rect = pygame.Rect((x, y), (13, 13))
    self.dir = dir
    self.lifetime = 0.7
    self.timer = Timer()
    self.alive = True
    self.damage = 1
    self.not_bow = other_weapon
    if other_weapon: self.lifetime = 0.2
    if adham_sword: self.lifetime = 0.4; self.damage = 2
    self.not_hook = True

  def update(self):
    if not self.not_bow: screen.blit(self.image, (self.rect.x - main.scrolls[0], self.rect.y - main.scrolls[1]))
    if self.dir == "right": self.rect.x += 15
    if self.dir == "left": self.rect.x -= 15
    if self.dir == "front": self.rect.y += 15
    if self.dir == "back": self.rect.y -= 15
    if self.timer.timer(self.lifetime * FPS): self.alive = False


class Shovel:
  def __init__(self, x, y, dir):
    self.rect = pygame.Rect((x, y), (13, 13))
    self.dir = dir
    self.lifetime = 0.1
    self.timer = Timer()
    self.damage = 0.0
    self.not_bow = False
    self.alive = True

  def update(self):
    if self.dir == "right": self.rect.x += 15
    if self.dir == "left": self.rect.x -= 15
    if self.dir == "front": self.rect.y += 15
    if self.dir == "back": self.rect.y -= 15
    if self.timer.timer(self.lifetime * FPS): self.alive = False


class Grapple:
  def __init__(self, x, y, dir, user):
    self.rect = pygame.Rect((x, y), (25, 25))
    self.dir = dir
    self.length = 0
    self.retract = False
    self.alive = True
    self.player = user
    self.not_bow = True
    self.not_hook = False
    self.damage = 1

  def update(self):
    pygame.draw.line(screen, "Grey", ((self.player.rect.x + 15) - main.scrolls[0], (self.player.rect.y + 15) - main.scrolls[1]), ((self.rect.x + 15) - main.scrolls[0], (self.rect.y + 15) - main.scrolls[1]), width=2)
    #pygame.draw.rect(screen, "White", self.rect)
    if self.dir == "right": self.rect.x = self.player.rect.x + self.length
    if self.dir == "left": self.rect.x = self.player.rect.x - self.length
    if self.dir == "front": self.rect.y = self.player.rect.y + self.length
    if self.dir == "back": self.rect.y = self.player.rect.y - self.length
    if self.retract: self.length -= 9
    else: self.length += 7
    if self.length > 50 and not self.retract: self.retract = True
    if self.length <= 2 and self.retract: self.alive = False; self.player.state = "walk"
    

def collision_test(rect, tiles):
  hit_list = []
  for tile in tiles:
    if rect.colliderect(tile):
      hit_list.append(tile)
  return hit_list

k_right, k_left, k_down, k_up, k_a, k_up2, k_select, k_start = False, False, False, False, False, False, False, False
k_debug = False

def run():
  global k_down, k_up, k_right, k_left, k_a, k_up2, k_select, k_start, k_debug, sword_load, sword_go, flash_more
  if main.gamestate != 4: k_a, k_left, k_right, k_up, k_down, k_start = False, False, False, False, False, False
  if main.gamestate != 2: k_select = False
  k_start = False
  for event in pygame.event.get():
    if event.type == pygame.QUIT: main.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN: k_start = True
      if event.key == pygame.K_e or event.key == pygame.K_SPACE: k_a = True
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = True
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = True
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = True
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = True
      if event.key == pygame.K_i: k_select = True
      if event.key == pygame.K_z: k_debug = True
      if event.key == pygame.K_ESCAPE:
        if main.gamestate == 1: main.gamestate = 0; main.scrolly = 0; main.started = False; sword_load, sword_go, flash_more = 0, 0, False; pygame.mixer.music.load("Sounds/tracks/Introduction Theme.mp3"); pygame.mixer.music.play(-1, 0.0); pygame.mixer.music.set_volume(1)
        elif (main.gamestate == 4 or main.gamestate == 5) and not main.immobilize: main.gamestate = 1; pygame.mixer.music.stop(); main.end_game()
        elif main.gamestate == 2: main.gamestate = 1
        else: main.quit()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_RETURN: k_start = False
      if event.key == pygame.K_SPACE or event.key == pygame.K_e: k_a = False
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = False
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = False
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = False
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = False
      if event.key == pygame.K_i: k_select = False
      if event.key == pygame.K_z: k_debug = False
    if event.type == JOYBUTTONDOWN:
      if event.button == 0:
        if main.gamestate == 0: k_a = True
        else: k_a = True #x A
      if event.button == 1: k_select = True #menu
      if event.button == 2: k_a = True #□ X
      if event.button == 3: k_select = True #△ Y
      if event.button == 4: pygame.image.save(screen, "screenshot.png"); #share
      if event.button == 5: k_start = True #PS
      if event.button == 6:
        if main.gamestate == 0: k_select = True
        elif main.gamestate > 0: main.gamestate = 0; main.reset() #menu
      if event.button == 7:
        if main.gamestate == 0: k_start = True #L3
      if event.button == 8: k_start = True #R3
      if event.button == 9: k_start = True #L1 LB
      if event.button == 10: k_select = True #R1 RB
      if event.button == 11: k_up = True #up
      if event.button == 12: k_down = True #down
      if event.button == 13: k_left = True #left
      if event.button == 14: k_right = True #right
      if event.button == 15: pygame.image.save(screen, "screenshot.png"); #pad
    if event.type == JOYAXISMOTION:
      if abs(event.value) > 0.1:
        k_up, k_down = False, False
        if event.axis == 0:
          if event.value < -0.5: k_left = True #go left
          else: k_left = False
          if event.value > 0.5: k_right = True #go right
          else: k_right = False
        if event.axis == 1:
          if event.value < -0.5 + (main.gamestate == 0) / 5: k_up = True #go up
          else: k_up = False
          if event.value > 0.4 + (main.gamestate == 0) / 5: k_down = True #go down
          else: k_down = False
        if event.axis == 2:
          if event.value < -0.6: pass #look left
          if event.value > 0.6: pass #look right
        if event.axis == 3:
          if event.value < -0.6: pass #look up
          if event.value > 0.6: pass #look down
    if event.type == JOYBUTTONUP:
      if event.button == 0: k_a = False #x A
      if event.button == 1: k_select = False #o B
      if event.button == 2: k_a = False #□ X
      if event.button == 3: k_select = False #△ Y
      if event.button == 4: pass #share
      if event.button == 5: pass #PS
      if event.button == 6: pass #menu
      if event.button == 7: pass #L3
      if event.button == 8: pass #R3
      if event.button == 9: pass #L1 LB
      if event.button == 10: pass #R1 RB
      if event.button == 11: k_up = False #up
      if event.button == 12: k_down = False #down
      if event.button == 13: k_left = False #left
      if event.button == 14: k_right = False #right
      if event.button == 15: pass #pad
    if event.type == JOYDEVICEADDED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
    if event.type == JOYDEVICEREMOVED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
  if k_down and k_up and pygame.mouse.get_pressed(): pygame.image.save(screen, "screenshot.png")
  display.fill("Black")
  display.blit(screen, (0 + main.shake[0], 0 + main.shake[1]))
  pygame.display.update()
  screen.fill("Black")
  clock.tick(FPS)

#out_ = open("Saves/memory_card/savefile.txt", "w"); json.dump(saves, out_); out_.close()
try:
  in_ = open("Saves/memory_card/savefile.txt", "r"); saves = json.load(in_)

  print("JSON serializer", "Enabling ReadableBuffer"); print("SAVES FOUND!", open("Saves/memory_card/savefile.txt", "r"))
except: print("No memory card inserted - if you want to keep saves, install the card in the itch.io page.")

main = Main()

main.player = Player()

while True:
  main.update()