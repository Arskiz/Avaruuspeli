import math
import pygame as game
import os
import sys
import random as r
import datetime as d;
import json
objektit = [] # Pelaajan ammukset lista
objektit2 = [] # Vihollisen ammukset lista



clock = game.time.Clock() # Määritä kello
WIDTH, HEIGHT = 1920, 1080 # Määritä ikkunan leveys ja korkeus
game.init() # Initializoi peli
WIN = game.display.set_mode((WIDTH, HEIGHT)) # Aseta ikkunan kooksi WIDTH ja HEIGHT

# Määritä Score & Level muuttujat
score = 0
level = 0

# Määritä onko pelaaja ensimmäistä kertaa painanut settings-nappia
firstTime2 = True

# Huijauskoodit
HackStatus = False
godMode = False
text = ""


# Värit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
color = BLACK

# Mainmenu
mainMenu = True

# Paused
firstTime = True

# reuna
BORDERTHICKNESS = 5

LEFT_BORDER = game.Rect(0, 0, BORDERTHICKNESS, HEIGHT)
RIGHT_BORDER = game.Rect(WIDTH - BORDERTHICKNESS, 0, BORDERTHICKNESS, HEIGHT)
UPPER_BORDER = game.Rect(0, 0, WIDTH, BORDERTHICKNESS)
DOWN_BORDER = game.Rect(0, HEIGHT - BORDERTHICKNESS, WIDTH, BORDERTHICKNESS)

# FPS
FPS = 60
showCounter = True

# -- Aseen parametrit --|
nykyinenAmmo = 0  
nykyinenLipas = 0  
maxAmmo = 0  
maxLipas = 0 
maxAmmoEnemy = 0
infiniteAmmo = False 
PLAYER_BULLET_VEL = 5  
ENEMY_BULLET_VEL = 5 
gun = 2 
textBGColor = True  


# Pelaajan parametrit
VEL = 0  # Nopeus
OriginalVEL = 2  # Alkuperäinen nopeus
BOOST_AMOUNT = 5  # Boostin määrä
BOOSTING = False  # Boostaako?
nykyinenHealth = 5  # Elämät
maxHealth = 5  # max elämät
enemiesKilled = 0 # paljon vihollisia tapettu?
damageDone = 0 # paljon damagea tehty vihollisiin?
killsUntilLevelUP = 3 # paljon tappoja tarvii kunnes level upataan?
pelaajat = [] # lista pelaajista


# Idk
reloadfont = game.font.SysFont('Consolas', 30)

# Äänet
nykyinenSound = "Menu"
musicID = 1
playerID = 2
enemyID = 3
music = game.mixer.Channel(1).get_volume()

# Vihollisten parametrit
enemies = []
enemy = None
maxEnemies = 10
atLeft = False
atRight = False
leftMovement = False
rightMovement = False

# Tallenna json-tiedostona nämä variablet
data = {
    'Highscore' : score,
    'Highest Level' : level,
    'Enemies Killed' : enemiesKilled,
    'Damage Done' : damageDone
}



# Yritä avata save.txt - tiedosto
try:
    with open('save.txt') as save_file:
        data = json.load(save_file)
except:
    print("Ei löytynyt savea.") # Tekee uuden saven pelin päättyessä halutessaan


# Pelaajan Rectangle (Määritä kuva)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
SPACESHIP_IMAGE = game.image.load(os.path.join('Assets/Player', 'spaceship.png'))
PLAYER = game.transform.rotate(game.transform.scale(
    SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

# Vihollisen Rectangle (Määritä kuva)
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
ENEMY_IMAGE = game.image.load(os.path.join('Assets/Enemy', 'enemy.png'))
ENEMY = game.transform.rotate(game.transform.scale(
    ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)), 0)

# Luodit (Määritä kuvat)
BULLET_WIDTH, BULLET_HEIGHT = 10, 20
RED_BULLET_IMG = game.image.load(
    os.path.join('Assets/Player', 'pixel_laser_red.png'))
GREEN_BULLET_IMG = game.image.load(
    os.path.join('Assets/Player', 'pixel_laser_green.png'))
YELLOW_BULLET_IMG = game.image.load(
    os.path.join('Assets/Player', 'pixel_laser_yellow.png'))
BLUE_BULLET_IMG = game.image.load(
    os.path.join('Assets/Player', 'pixel_laser_blue.png'))
RED_BULLET = game.transform.rotate(game.transform.scale(
    RED_BULLET_IMG, (BULLET_WIDTH, BULLET_HEIGHT)), 0)
GREEN_BULLET = game.transform.rotate(game.transform.scale(
    GREEN_BULLET_IMG, (BULLET_WIDTH, BULLET_HEIGHT)), 0)
YELLOW_BULLET = game.transform.rotate(game.transform.scale(
    YELLOW_BULLET_IMG, (BULLET_WIDTH, BULLET_HEIGHT)), 0)
BLUE_BULLET = game.transform.rotate(game.transform.scale(
    BLUE_BULLET_IMG, (BULLET_WIDTH, BULLET_HEIGHT)), 0)

# Nappien leveys ja pituus arvot
MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT = 200, 80
ITEM_BUTTON_WIDTH, ITEM_BUTTON_HEIGHT = 100, 100

# Main-Menu nappien kuvat
PLAY_BUTTON = game.image.load(os.path.join('Assets/UI', 'play.png'))
PLAY  = game.transform.rotate(game.transform.scale(PLAY_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

SETTINGS_BUTTON = game.image.load(os.path.join('Assets/UI', 'settings.png'))
SETTINGS  = game.transform.rotate(game.transform.scale(SETTINGS_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

EXIT_BUTTON = game.image.load(os.path.join('Assets/UI', 'exit.png')) 
EXIT  = game.transform.rotate(game.transform.scale(EXIT_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

EXIT_SAVE_BUTTON = game.image.load(os.path.join('Assets/UI', 'exit_save.png')) 
EXIT_SAVE  = game.transform.rotate(game.transform.scale(EXIT_SAVE_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

DELETE_BUTTON = game.image.load(os.path.join('Assets/UI', 'delete.png')) 
DELETE  = game.transform.rotate(game.transform.scale(DELETE_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

# Settings-Menu nappien kuvat
ULTIMATEFPS_BUTTON = game.image.load(os.path.join('Assets/UI', 'ULTIMATEFPS.png'))
ULTIMATEFPS  = game.transform.rotate(game.transform.scale(ULTIMATEFPS_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

FPS_TOGGLE_BUTTON = game.image.load(os.path.join('Assets/UI', 'fps_toggle.png'))
FPSS  = game.transform.rotate(game.transform.scale(FPS_TOGGLE_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

BACK_BUTTON = game.image.load(os.path.join('Assets/UI', 'back.png')) 
BACK  = game.transform.rotate(game.transform.scale(BACK_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

FPS_BG_BUTTON = game.image.load(os.path.join('Assets/UI', 'fps_bg_toggle.png')) 
FPS_BG_BTN  = game.transform.rotate(game.transform.scale(FPS_BG_BUTTON, (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)), 0)

# Item-nappien kuvat
ITEM1_BUTTON = game.image.load(os.path.join('Assets/UI', '1.png')) 
ITEM1  = game.transform.rotate(game.transform.scale(ITEM1_BUTTON, (ITEM_BUTTON_WIDTH, ITEM_BUTTON_HEIGHT)), 0)

ITEM2_BUTTON = game.image.load(os.path.join('Assets/UI', '2.png')) 
ITEM2  = game.transform.rotate(game.transform.scale(ITEM2_BUTTON, (ITEM_BUTTON_WIDTH, ITEM_BUTTON_HEIGHT)), 0)

ITEM3_BUTTON = game.image.load(os.path.join('Assets/UI', '3.png')) 
ITEM3  = game.transform.rotate(game.transform.scale(ITEM3_BUTTON, (ITEM_BUTTON_WIDTH, ITEM_BUTTON_HEIGHT)), 0)

# Taustakuva
BACKGROUND = game.image.load(os.path.join('Assets/UI', 'background-black.png'))

# Taustakuva
DEATH_BACKGROUND = game.image.load(os.path.join('Assets/UI', 'background-death.png'))

#level & score
KILL_SCORE = r.randint(100, 120)
HIT_SCORE = r.randint(1, 3)

# Luodin luokka
class Bullet:

    # Perusarvot
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = game.mask.from_surface(self.img)

    # Piirrä näytölle luoti
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Liikuta objektia
    def move(self, vel):
        self.y += vel

    # Jos on pois näytöstä funktio
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    # Osuma funktio
    def collision(self, obj):
        return collide(self, obj)

# Ship class
class Ship:
    FIRERATE_PLAYER = gun * 5
    FIRERATE_ENEMY = gun * 5
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.enemies = []
        self.firerate_player = 0
        self.firerate_enemy = 0

    # Objektien piirto
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for objekti in objektit:
            objekti.draw(window)
        for objekti2 in objektit2:
            objekti2.draw(window)

    # Pelaajan firerate
    def fireratee(self):
        if self.firerate_player >= self.FIRERATE_PLAYER:
            self.firerate_player = 0
        elif self.firerate_player > 0:
            self.firerate_player += 1

    # Vihollisen firerate
    def firerateee(self):
        if self.firerate_enemy >= self.FIRERATE_ENEMY:
            self.firerate_enemy = 0
        elif self.firerate_enemy > 0:
            self.firerate_enemy += 0.1

    # Pelaajan ammunta-funktio
    def playerShoot(self):
        global gun         # Käytetään globaalia muuttujaa "gun"
        global nykyinenAmmo # Käytetään globaalia muuttujaa "nykyinenAmmo"
        if self.firerate_player == 0 and nykyinenAmmo != 0: # Tarkistetaan, että ase ei ole cooldownissa ja että pelaajalla on ammuksia
            if(gun == 2): # Jos pelaajalla on aseena kaksi pistoolia
                bullet = Bullet(self.x, self.y, self.bullet_img)  # Luodaan uusi ammus pelaajan sijaintiin
                bullet2 = Bullet(self.x + 44, self.y, self.bullet_img) # Luodaan toinen ammus pelaajan sijaintiin
                objektit.append(bullet) # Lisätään ammukset objektit-listalle
                objektit.append(bullet2) # Lisätään ammukset objektit-listalle
            elif(gun == 1): # Jos pelaajalla on aseena yksi pistooli
                bullet = Bullet(self.x + 23, self.y, self.bullet_img) # Luodaan uusi ammus pelaajan sijaintiin
                objektit.append(bullet) # Lisätään ammus objektit-listalle
            elif(gun == 3): # Jos pelaajalla on aseena kolme pistoolia
                bullet = Bullet(self.x, self.y, self.bullet_img) # Luodaan uusi ammus pelaajan sijaintiin
                bullet2 = Bullet(self.x + 44, self.y, self.bullet_img) # Luodaan toinen ammus pelaajan sijaintiin
                bullet3 = Bullet(self.x + 23, self.y, self.bullet_img) # Luodaan kolmas ammus pelaajan sijaintiin
                objektit.append(bullet) # Lisätään ammukset objektit-listalle
                objektit.append(bullet2) # Lisätään ammukset objektit-listalle
                objektit.append(bullet3) # Lisätään ammukset objektit-listalle
            if(nykyinenAmmo > 0): # Jos pelaajalla on ammuksia jäljellä
                if(gun == 3):
                    play_audio("hitHurt.wav", 2) # Soitetaan ääniefekti
                else:
                    play_audio("laserShoot.wav", 2) # Soitetaan ääniefekti
                if not infiniteAmmo:
                    nykyinenAmmo -=gun # Vähennetään pelaajan aseeseen käytettyjen ammusten määrä "nykyinenAmmo"-muuttujasta
            self.firerate_player = 1 # Asetetaan cooldown-tila "1"-arvoon

    # Vihollisen ammunta-funktio
    def enemyShoot(self):
        global gun         # Käytetään globaalia muuttujaa "gun"
        if self.firerate_enemy == 0: # Tarkistetaan, että ase ei ole cooldownissa ja että vihollisella on ammuksia
            bullet = Bullet(self.x + 23, self.y, self.bullet_img) # Luodaan uusi ammus vihollisen sijaintiin
            objektit2.append(bullet) # Lisätään ammus objektit2-listalle(vihollisten ammukset)
            if(self.nykyinenAmmo2 > 0): # Jos vihollisella on ammuksia jäljellä
                play_audio("hitHurt.wav", 2) # Soitetaan ääniefekti
                self.nykyinenAmmo2 -=gun # Vähennetään vihollisen aseeseen käytettyjen ammusten määrä "nykyinenAmmo"-muuttujasta
            self.firerate_enemy = 1 # Asetetaan cooldown-tila "1"-arvoon

   

    # Funktio joka ottaa aluksen Leveyden
    def get_width(self):
        return self.ship_img.get_width()

    # Funktio joka ottaa aluksen Pituuden
    def get_height(self):
        return self.ship_img.get_height()
    
# Player class
class Player(Ship):

    # Määritä perusarvo hommat
    def __init__(self, x, y, health=maxHealth):
        super().__init__(x, y, health)
        self.ship_img = PLAYER
        self.rect = self.ship_img.get_rect()
        x = self.rect.x
        y = self.rect.y
        self.bullet_img = BLUE_BULLET
        self.mask = game.mask.from_surface(self.ship_img)
        self.max_health = health

     # Osuma funktio
    def collision(self, obj):
        return collide(self, obj)

    def bullet_move(self, vel, objs):

        # Tarkistaa, onko pelaajan ase laukaistu ja vähentää odotusaikaa
        self.fireratee()
        
        # Jokaiselle objektille objektit-listassa
        for objekti in objektit:

            # Liikuttaa luoteja määritellyn nopeuden mukaisesti
            objekti.move(vel)
            
            # Tarkistaa, onko luoti poistunut näytöltä
            if objekti.off_screen(HEIGHT):
                objektit.remove(objekti)
            
            # Jos ei ole
            else:

                # Käy läpi kaikki peliobjektit ja tarkistaa, onko luoti osunut johonkin niistä
                for obj in objs:

                    # Määrittelee globaalit piste- ja taso-muuttujat
                    global score
                    global level
                    global enemiesKilled
                    global damageDone

                    # Jos luoti osuu peliobjektiin
                    if objekti.collision(obj):

                        # Jos peliobjektilla on elämää jäljellä, vähennetään sitä yhdellä ja poistetaan luoti
                        if (obj.health > 0):
                            obj.health -= 1

                            # Jos objekti on objektit listassa:
                            if(objekti in objektit):

                                # Poista objektit-listasta objekti
                                objektit.remove(objekti)

                            # Lisää score muuttujaan HIT_SCORE määrä
                            score += HIT_SCORE

                            # Lisää damageDone muuttujaan HIT_SCORE määrä
                            damageDone += HIT_SCORE

                            # Soita viholliseen osuma ääni
                            play_audio("hitHurt2.wav", 3)

                        # Jos peliobjekti kuolee, toistetaan räjähdysääni, lisätään pisteitä ja lisätään räjähdyksen animaatio
                        else:

                            # Soita räjähdys ääni ja toista animaatio
                            play_audio("explosion.wav", 4)
                            explosion = Explosion(obj.x + (ENEMY_WIDTH / 2), obj.y + (ENEMY_HEIGHT / 2))
                            explosion_group.add(explosion)
                            objs.remove(obj)

                            # Lisää scoreen KILL_SCORE
                            score = score + KILL_SCORE

                            # Lisää damageen KILL_SCORE
                            damageDone += KILL_SCORE
                            enemiesKilled += 1
                            
                            if len(enemies) < maxEnemies: # Tarkistetaan onko vihollisten määrä pienempi kuin maksimi sallittu määrä
                                instantiate_enemy(level) # Luodaan uusi vihollinen levelin perusteella
                            else: # Jos on isompi kuin maksimi sallittu määrä

                                # Printtaa varoitus teksti
                                print("VAROITUS! Vihollisia liikaa!!\n" + "Vihollisia liikaa: (" + str(int(len(enemies)) - maxEnemies)   + ") yhteensä: (" + str(len(enemies)) + ")!!")
                                
                                # Jos vanhaVihollinen on rangessa (enemies-listan vihollisten määrä) - Maksimi vihollis määrä
                                for vanhaVihollinen in range(len(enemies) - int(maxEnemies)):

                                    # Jos vanhaVihollinen on enemies-listassa
                                    if vanhaVihollinen in enemies:

                                        # Poista "vanhaVihollinen" enemies-listasta
                                        enemies.remove(vanhaVihollinen) # poistetaan vihollisia

                                        # Printtaa 
                                        print("poistetaan 1 vihollinen")
        
# Määritellään vihollisen avaruusalus Ship-luokan periytyväksi alaluokaksi.
class Enemy(Ship):
    
    # Luokan konstruktori, joka kutsuu Ship-luokan konstruktoria.

    # Asettaa viholliselle kuvan, ammuksen kuvan ja satunnaisen värin.
    def __init__(self, x, y, health=10):
        super().__init__(x, y, health)
        self.ship_img = ENEMY
        self.bullet_img = RED_BULLET
        self.nykyinenAmmo2 = maxLipas
        self.maxAmmo = maxAmmoEnemy
        self.mask = game.mask.from_surface(self.ship_img)
        self.max_health = health
        self.rect = self.ship_img.get_rect()
        x = self.rect.x
        y = self.rect.y

        # Luodaan avaruusaluksen maski.
        self.mask = game.mask.from_surface(self.ship_img)
        
        # Asetetaan avaruusaluksen maksimielämät.
        self.max_health = health
        
    def bullet_move(self, vel, objs):

        # Tarkistaa, onko vihollisen ase laukaistu ja vähentää odotusaikaa
        self.firerateee()
        
        for objekti in objektit2:

            # Liikuttaa luoteja määritellyn nopeuden mukaisesti
            objekti.move(vel)
            
            # Tarkistaa, onko luoti poistunut näytöltä
            if objekti.off_screen(HEIGHT):

                # Jos on, poista luoti objektit2-listasta
                objektit2.remove(objekti)
                
            else:
                # Käy läpi kaikki viholliset ja tarkistaa, onko luoti osunut johonkin niistä
                for obj in objs:
                    global nykyinenHealth
                    global godMode
                    # Jos luoti osuu pelaajaan
                    if objekti.collision(obj):

                        # Jos pelaajalla on elämää jäljellä enemmän kuin yksi, vähennetään sitä yhdellä ja poistetaan luoti
                        if (obj.health > 1):
                            if(godMode != True):
                                obj.health -= 1

                            # Jos nykyinen elämä on isompi kuin 0, poista yksi
                            if(nykyinenHealth > 0):
                                if(godMode != True):
                                    nykyinenHealth -= 1

                            # Jos objekti on objektit2-listassa
                            if(objekti in objektit2):

                                # Poista objekti objektit2-listasta
                                objektit2.remove(objekti)
                            
                            # Soita pelaajan osuma ääni
                            play_audio("hitHurt.wav", 3)
                        # Jos pelaaja kuolee, toistetaan räjähdysääni ja lisätään räjähdyksen animaatio
                        else:

                            # Soita räjähdyksen ääni 4-kanavalla
                            play_audio("explosion.wav", 4)

                            # Näytä kuolema-näyttö
                            death_screen()

                            # Tee räjähdys-animaatio pelaajan näyttöön
                            explosion = Explosion(obj.x + (ENEMY_WIDTH / 2), obj.y + (ENEMY_HEIGHT / 2)) # --- ENEMYLLÄ JA PELAAJALLA SAMAT WIDTH JA HEIGHT ARVOT!!
                            explosion_group.add(explosion)
                            # objs.remove(obj) -------- EI KÄYTÖSSÄ --------


    # Palauttaa avaruusaluksen leveyden.
    def get_width(self):
        return self.ship_img.get_width()

    # Palauttaa avaruusaluksen korkeuden.
    def get_height(self):
        return self.ship_img.get_height()

# Tallenna score
def save_score():

    # Ottaa datasta muuttujia
    currentScore = data['Highscore']
    currentLevel = data["Highest Level"]
    currentKills = data["Enemies Killed"]
    currentDamage = data["Damage Done"]

    # Katsoo jos muuttujien arvot on isompia kuin save-tiedostossa olevat arvot
    if currentScore < score:
        data['Highscore'] = score

    if currentLevel < level:
        data["Highest Level"] = level

    if currentKills < enemiesKilled:
        data["Enemies Killed"] = enemiesKilled

    if currentDamage < damageDone:
        data["Damage Done"] = damageDone

    # Tallenna tiedot tiedostoon 'save.txt'
    with open('save.txt','w') as save_file:

        # Käytä jsonia ja kirjoita save_file-tiedostoon data
        json.dump(data, save_file)
    
class Button():

    # Perusarvot
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.mask = game.mask.from_surface(self.image)

    # Piirto - funktio
    def draw(self):

        # Aseta action pois päältä
        action = False

        # Saa hiiren lokaatio näytöllä
        pos = game.mouse.get_pos()

        # Jos hiiri on napin päällä
        if self.rect.collidepoint(pos):

            # Jos painetaan hiiren nappia, ja ei olla painettu jo
            if game.mouse.get_pressed()[0] == 1 and not self.clicked:
                
                # Aseta clicked ja action true-arvoon
                self.clicked = True
                action = True
        else:

            # Aseta clicked false-arvoon
            self.clicked = False

        #game.draw.rect(WIN, (255, 0, 0), self.rect, 1) # piirtää napin rectin punaisella testausta varten
        
        if self.rect.collidepoint(pos) and self.mask.get_at((pos[0] - self.rect.x, pos[1] - self.rect.y)):
            # Tarkistaa, että hiiri osoittaa värillistä pikseliä napin päällä
            self.rect.y += 5
        WIN.blit(self.image, self.rect)
        return action
    
# Räjähdys - class
class Explosion(game.sprite.Sprite):
        
    # Määritä perusjutut
	def __init__(self, x, y):
		game.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = game.image.load(f"Assets/Enemy/exp{num}.png")
			img = game.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

    # Päivitä - funktio
	def update(self):
                
        # Räjähdyksen nopeus
		explosion_speed = 4
                
		# Päivitä räjähdyksen animaatio
		self.counter += 1

        # Jos animaatio ei ole lopussa, mene seuraavaan keyframeen
		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		# Jos animaatio on valmis, resetoi animaation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

explosion_group = game.sprite.Group()

# Soita audio - funktio
def play_audio(file, channelID):
    game.init()
    game.mixer.Channel(channelID).play(game.mixer.Sound("Assets/Sound/" + file))

# Soita audio - funktio
def play_music(file, channelID):
    game.init()
    game.mixer.Channel(channelID).play(game.mixer.Sound("Assets/Sound/" + file), 0)

# Menu-musiikin funktio
def Play_MenuMusic(channelID):
    if game.mixer.Channel(channelID).get_busy() != True:
        menuMusic = r.randint(0, 1)
        if(menuMusic == 0):
            play_music("MainTheme.mp3", 1)
        else:
            play_music("ImperialMarch.mp3", 1)
# Osuma funktio
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Initializoi fps meter & font
game.init()
font = game.font.SysFont("comicsans", 18)


# ----------------- Saa erilaisia asioita ----------------- #

# Ammo
def getAmmo():
    global nykyinenAmmo
    global nykyinenLipas
    return (str(int(nykyinenAmmo))) + " / " + str(int(nykyinenLipas))

# Ääni
def getSound():
    global nykyinenSound
    return str(nykyinenSound)



# Score
def getScore():
    global score
    global level
    return "Score: " + str(int(score)) + " / Level: " + str(int(level))

# Elämät
def getHealth():
    global nykyinenHealth
    global maxHealth
    return "(" + (str(int(nykyinenHealth))) + ") - " + str(int(maxHealth)) + ":stä"

# Kello
def getClock():
    currentClock = d.datetime.now()
    return(str(currentClock.hour) + "." + str(currentClock.minute) + "." + str(currentClock.second))

# ----------------- PÄIVITYKSET ----------------- #

# Päivitä fps meter
def update_fps():
    global color
    fps = str(int(clock.get_fps()))
    if (textBGColor == True):
        fps_text = font.render(" FPS: " + fps + " ", 1, color,  CYAN)
    else:
        fps_text = font.render(" FPS: " + fps + " ", 1, color)
    return fps_text

# Päivitä ammo
def update_ammo():
    ammo = getAmmo()
    ammo_text = font.render(" Ammo: " + ammo + " ", 1, game.Color("black"),  CYAN)
    return ammo_text

# Päivitä score & level
def update_scoreLevel():
    scoreLevel = getScore()
    scoreLevel_text = font.render(" " + scoreLevel + " [" + f"Highscore: {data['Highscore']}, Highest Level: {data['Highest Level']}] ", 1, game.Color("black"),  CYAN)
    return scoreLevel_text

# Päivitä health
def update_health():
    health = getHealth()
    health_text = font.render(" Elämiä jäljellä: " + health + " ", 1, game.Color("black"),  GREEN)
    return health_text

# Päivitä kello
def update_clock():
    clock = getClock()
    clock_text = font.render(" Kello: " + clock + " ", 1, game.Color("black"), CYAN)
    return clock_text

# Päivitä musiikin teksti
def update_current_sound():
    sound_text = font.render(" Voit laittaa musiikin pois päältä pelissä painamalla 'M'. ", 1, game.Color("black"),  GREEN)
    return sound_text

# Päivitä musiikin teksti
def UpdateHackStatus():
    global HackStatus
    if(HackStatus):
        status_text = font.render(" Hacks: PÄÄLLÄ " , 1, game.Color("black"),  RED)
    else:
        status_text = font.render(" Hacks: POIS " , 1, game.Color("black"),  GREEN)
    return status_text


# Laita audio joko päälle taikka pois päältä
def audio_toggle(status=bool, currentID=int):
    if(status):
        game.mixer.Channel(currentID).set_volume(100)
    else:
        game.mixer.Channel(currentID).set_volume(0)
        
# Lisää level - funktio        
def level_increase():
    global level
    level += 1

# Luo uusi vihollinen
def instantiate_enemy(amount):
    print("Instantiated An Enemy!")
    for each in range(0, amount):
        each = Enemy((r.randint(0, WIDTH)), r.randint(0,200))
        enemies.append(each)

# Piirrä pää peli-ikkuna
def game_window(player):

    # Määritellään julkiset muuttujat
    global text
    global gun

    # Laita taustaväriksi musta
    WIN.fill(BLACK)

    # Piirrä pelaajan alus
    player.draw(WIN)

    # Piirrä jokaisen vihollisen alus
    for enemy in enemies:
        enemy.draw(WIN)

    # Piirrä räjähdys
    explosion_group.draw(WIN)

    # Päivitä räjähdys
    explosion_group.update()

    # Tee Item-napit
    Item1 = Button(WIDTH/2 - ITEM1.get_width()/2 - 150, HEIGHT - ITEM1.get_height() - BORDERTHICKNESS * 3, ITEM1)
    Item2 = Button(WIDTH/2 - ITEM1.get_width()/2,  HEIGHT - ITEM1.get_height() - BORDERTHICKNESS * 3, ITEM2)
    Item3 = Button(WIDTH/2 - ITEM1.get_width()/2 + 150, HEIGHT - ITEM1.get_height() - BORDERTHICKNESS * 3, ITEM3)

    # Piirrä "Paina M laittaaksesi musiikin päälle tai pois"
    WIN.blit(update_current_sound(), (0, HEIGHT - 30))

    # Piirrä "HackStatus" funktion status tekstinä näytölle
    WIN.blit(UpdateHackStatus(), (WIDTH / 2 - UpdateHackStatus().get_width() /2, HEIGHT - 150))

    # Jos item1 - nappia painetaan, aseta aseeksi 1
    if Item1.draw():
        gun = 1

    # Jos item2 - nappia painetaan, aseta aseeksi 2
    if Item2.draw():
        gun = 2

    # Jos item4 - nappia painetaan, aseta aseeksi 3
    if Item3.draw():
        gun = 3

    # Piirrä reload teksti
    WIN.blit(reloadfont.render(text, True, WHITE), (WIDTH / 2 - 120, HEIGHT / 2 + 60))

# Piirrä pelin punaiset reunat, joiden yli pelaaja ei voi mennä

    # Vasen kulma
    game.draw.rect(WIN, RED, LEFT_BORDER)

    # Oikea kulma
    game.draw.rect(WIN, RED, RIGHT_BORDER)

    # Yläkulma
    game.draw.rect(WIN, RED, UPPER_BORDER)

    # Alakulma
    game.draw.rect(WIN, RED, DOWN_BORDER)

    # Jos fps counter-bool on päällä, piirrä fps teksti näytölle ja laita otsikoksi nimi & fps
    if (showCounter):
        fps = str(int(clock.get_fps()))
        game.display.set_caption("Testipeli - FPS: " + fps)
        WIN.blit(update_fps(), (10, 10))
    else:
        game.display.set_caption("Testipeli")

    # Piirrä ammo-teksti näytölle
    rectAmmo = update_ammo().get_rect()
    WIN.blit(update_ammo(), ((WIDTH - rectAmmo.width - (BORDERTHICKNESS * 2)), 10))
    
    # Piirrä score/level-teksti näytölle
    rectScoreLevel = update_scoreLevel().get_rect()
    WIN.blit(update_scoreLevel(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - (BORDERTHICKNESS * 3)), 10))

    # Piirrä score/level-teksti näytölle
    rectHealth = update_health().get_rect()
    WIN.blit(update_health(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - rectHealth.width - (BORDERTHICKNESS * 4)), 10))
    
    # Piirrä kello-teksti näytölle
    rectClock = update_clock().get_rect()
    WIN.blit(update_clock(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - rectHealth.width - rectClock.width -(BORDERTHICKNESS * 5)), 10))
    game.display.update()
    
    # Todo: itemit
    
# Rotate funktio
def rotation(self, angle):
    self.rect = game.transform.rotate(self.rect, angle)
    
# Liikkumisen händläys    
def handleMovement(keys_pressed):

    # Määritellään julkiset muuttujat
    global VEL
    global BOOSTING
    global OriginalVEL
    global objektit

    # VEL on alkuperäinen VEL
    VEL = OriginalVEL
    
    # Jokaiselle objektille objektit-listassa
    for objekti in objektit:
            
            # Jos painetaan a-kirjainta - muut objektit menee vasemmalle
            if (keys_pressed[game.K_a]):  # left key
                objekti.x += VEL

            # Jos painetaan d-kirjainta - muut objektit menee oikealle
            if (keys_pressed[game.K_d]):  # right key
                objekti.x -= VEL
            # Jos painaa w-kirjainta - kaikki muut objectit menevät alaspäin
            if (keys_pressed[game.K_w]): # up key
                objekti.y += VEL

            # Jos painaa s-kirjainta - kaikki muut objectit menevät ylöspåin
            if (keys_pressed[game.K_s]): # down key
                objekti.y -= VEL

    for objekti2 in objektit2:# -- muut objektit
                
                # Jos painetaan a-kirjainta - muut objektit menee vasemmalle
                if (keys_pressed[game.K_a]):  # left key
                    objekti2.x += VEL

                # Jos painetaan d-kirjainta - muut objektit menee oikealle
                if (keys_pressed[game.K_d]):  # right key
                    objekti2.x -= VEL
                # Jos painaa w-kirjainta - kaikki muut objectit menevät alaspäin
                if (keys_pressed[game.K_w]): # up key
                    objekti2.y += VEL

                # Jos painaa s-kirjainta - kaikki muut objectit menevät ylöspåin
                if (keys_pressed[game.K_s]): # down key
                    objekti2.y -= VEL

    for enemy in enemies: # -- viholliset

        # Jos painetaan a-kirjainta - kaikki muut viholliset menee vasemmalle
        if (keys_pressed[game.K_a]):  # left key
                enemy.x += VEL

        # Jos painetaan d-kirjainta - kaikki muut viholliset menee oikealle
        if (keys_pressed[game.K_d]):  # right key
            enemy.x -= VEL

        # Jos painaa w-kirjainta - kaikki muut viholliset menevät alaspäin
        if (keys_pressed[game.K_w]): # up key
            enemy.y += VEL

        # Jos painaa s-kirjainta - kaikki muut viholliset menevät ylöspåin
        if (keys_pressed[game.K_s]): # down key
            enemy.y -= VEL

    # Jos painetaan boost-nappia (space) - objektit liikkuvat nopeampaa
    if (keys_pressed[game.K_SPACE] and BOOSTING != True):
        
        # VEL on BOOST_AMOUNT
        VEL = BOOST_AMOUNT

        # BOOSTING on päällä
        BOOSTING = True

    # Jos ei paineta boost-nappia (space)
    else:

        # Muuttuja VEL on alkperäinen VEL
        VEL = OriginalVEL

        # BOOSTING on pois päältä
        BOOSTING = False

# Pelaajan reload weapon
def Player_Reload_Weapon():

    # Määritellään julkiset muuttujat
    global nykyinenLipas
    global nykyinenAmmo
    global maxAmmo
    global maxLipas
    global text

    # uusiAmmo tarkoittaa sitä että maxAmmosta poistetaan nykyinen ammo kapasiteetti, josta saa ammon joka täytyy poistaa lippaista
    uusiAmmo = 0
    
    # Jos nykyinen lipas ei ole maxAmmo ja jos on isompi kuin 0
    if(nykyinenAmmo != maxAmmo):
        if(nykyinenLipas > 0):

            # Jos nykyinen ammo on 0
            if (nykyinenAmmo == 0):

                # Jos nykyinen lipas on surempi kuin max ammo
                if (nykyinenLipas > maxAmmo):

                    # Nykyinen ammo on max ammo
                    nykyinenAmmo = maxAmmo

                    # Nykyisestä lippaasta poistetaan max ammo
                    nykyinenLipas -= maxAmmo
                else:

                    # Nykyinen ammo on nykyinen lipas
                    nykyinenAmmo = nykyinenLipas

                    # Nykyinen lipas on 0
                    nykyinenLipas = 0

            # Muuten jos nykyinen ammo on isompi kuin nolla mutta pienempi kun max ammo 
            elif (nykyinenAmmo > 0 < maxAmmo):
                # uusiAmmo on max Ammo - nykyinenlipas
                uusiAmmo = (maxAmmo - nykyinenAmmo)

                print(str(maxAmmo) +  "-" + str(nykyinenAmmo) + "=" + str(uusiAmmo))
                # Nykyinen ammo on max ammo
                nykyinenAmmo = maxAmmo

                # Nykyisestä lippaasta poistetaan uusiAmmo
                nykyinenLipas -= uusiAmmo
            
            # Muuten jos nykyinen lipas on pienempi kuin max ammo
            elif (nykyinenLipas < maxAmmo):

                # Nykyinen ammo on nykyinen lipas
                nykyinenAmmo = nykyinenLipas

                # Nykyinen lipas on 0
                nykyinenLipas = 0

# Vihollisen reload weapon ( --- EI KÄYTÖSSÄ ---)
def Enemy_Reload_Weapon():

    # Määritellään julkiset muuttujat (VÄÄRÄT)
    global nykyinenLipas
    global nykyinenAmmo
    global maxAmmo
    
    # uusiAmmo tarkoittaa sitä että maxAmmosta poistetaan nykyinen ammo kapasiteetti, josta saa ammon joka täytyy poistaa lippaista
    uusiAmmo = 0

    # Jos nykyinen lipas on isompi kuin 0
    if(nykyinenLipas > 0):

        # Jos nykyinen ammo on 0
        if (nykyinenAmmo == 0):

            # Jos nykyinen lipas on surempi kuin max ammo
            if (nykyinenLipas > maxAmmo):

                # Nykyinen ammo on max ammo
                nykyinenAmmo = maxAmmo

                # Nykyisestä lippaasta poistetaan max ammo
                nykyinenLipas -= maxAmmo
            else:

                # Nykyinen ammo on nykyinen lipas
                nykyinenAmmo = nykyinenLipas

                # Nykyinen lipas on 0
                nykyinenLipas = 0

        # Muuten jos nykyinen ammo on isompi kuin nolla mutta pienempi kun max ammo 
        elif (nykyinenAmmo > 0 < maxAmmo):

            # uusiAmmo on max ammo - nykyinenlipas
            uusiAmmo = maxAmmo - nykyinenLipas

            # Nykyinen ammo on max ammo
            nykyinenAmmo = maxAmmo

            # Nykyisestä lippaasta poistetaan uusiAmmo
            nykyinenLipas -= uusiAmmo
        
        # Muuten jos nykyinen lipas on pienemp kuin max ammo
        elif (nykyinenLipas < maxAmmo):

            # Nykyinen ammo on nykyinen lipas
            nykyinenAmmo = nykyinenLipas

            # Nykyinen lipas on 0
            nykyinenLipas = 0

# Godmode
def GodMode():
    global godMode
    if (godMode == True):
        godMode = False
    else:
        godMode = True

# Infinite Ammo
def InfiniteAmmo():
    global infiniteAmmo
    if (infiniteAmmo == True):
        infiniteAmmo = False
    else:
        infiniteAmmo = True


# Fps:n taustakuva
def FPS_BG():
    global textBGColor
    global color
    if (textBGColor == True):
        textBGColor = False
        color = WHITE
    else:
        textBGColor = True
        color = BLACK

# Fps päällä vai ei
def FPS_Toggle():
    global showCounter
    if (showCounter == True):
        showCounter = False
    else:
        showCounter = True

# Musiikki päällä vai ei
def MUSIC_TOGGLE():
    global music
    if(music):
        music = False
    else:
        music = True

# Ammu-funktio pelaajalle
def player_shoot(player):
    player.playerShoot()

# Ammu-funktio viholliselle
def enemy_shoot(enemy):
    enemy.enemyShoot()

# Pause - Piirto funktio
def pause_draw():
    # Jos fps counter-bool on päällä, piirrä fps teksti näytölle ja laita otsikoksi nimi & fps
        if (showCounter):
            fps = str(int(clock.get_fps()))
            game.display.set_caption("Testipeli - FPS: " + fps)
            WIN.blit(update_fps(), (10, 10))
        else:
            game.display.set_caption("Testipeli")

        # Piirrä ammo-teksti näytölle
        rectAmmo = update_ammo().get_rect()
        WIN.blit(update_ammo(), ((WIDTH - rectAmmo.width - (BORDERTHICKNESS * 2)), 10))
        
        # Piirrä score/level-teksti näytölle
        rectScoreLevel = update_scoreLevel().get_rect()
        WIN.blit(update_scoreLevel(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - (BORDERTHICKNESS * 3)), 10))

        # Piirrä score/level-teksti näytölle
        rectHealth = update_health().get_rect()
        WIN.blit(update_health(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - rectHealth.width - (BORDERTHICKNESS * 4)), 10))
        
        # Piirrä kello-teksti näytölle
        rectClock = update_clock().get_rect()
        WIN.blit(update_clock(), ((WIDTH - rectAmmo.width - rectScoreLevel.width - rectHealth.width - rectClock.width -(BORDERTHICKNESS * 5)), 10))
        game.display.update()        

    

# Pause menu
def pause_menu():

    # Määritä julkiset muuttujat
    global firstTime
    global gun
    
    # Määritä titlen fontti
    title_font = game.font.SysFont("comicsans", 50)


    run = True

    # Kun run-loop on päällä
    while run:

        pause_draw()

        # Piirrä taustakuva
        WIN.blit(BACKGROUND, (0,0))

        # Määritä title:n teksti
        title_label = title_font.render('Paina "Play" Jatkaaksesi...', 1, CYAN, BLACK)

        # Piirrä title
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT / 2 - 50))

        # Piirrä "Paina M laittaaksesi musiikin päälle tai pois"
        WIN.blit(update_current_sound(), (WIDTH/2 - update_current_sound().get_width()/2, HEIGHT - 30))

        # Määritä nappulat play ja exit
        play = Button((WIDTH / 2 - PLAY.get_width() - 10), (HEIGHT / 2 + 30), PLAY)
        exit = Button((WIDTH / 2), (HEIGHT / 2 + 30), EXIT)

        # Jos painetaan play-nappia, mene main-funktioon
        if play.draw():
            main()
            
        # Jos painetaan exit-nappia, poistu pelistä
        if exit.draw():
            game.quit()

        # Jos fps counter-bool on päällä, piirrä fps teksti näytölle ja laita otsikoksi nimi & fps
        if (showCounter):
            fps = str(int(clock.get_fps()))
            game.display.set_caption("Testipeli - FPS: " + fps)
            WIN.blit(update_fps(), (10, 10))
        else:
            game.display.set_caption("Testipeli")

        # Piirrä kello-teksti näytölle
        rectClock = update_clock().get_rect()
        WIN.blit(update_clock(), ((WIDTH - rectClock.width -(BORDERTHICKNESS * 5)), 10))      

        # Päivitä ikkuna
        game.display.update()

        # Saa kaikki eventit
        for event in game.event.get():
            # Jos eventti on game.QUIT, sulje run-loop
            if(event.type == game.QUIT):
                run = False


    # Poistu pelistä
    game.quit()

# pääfunktio
def main():

    # Määritä julkiset muuttujat
    global maxAmmo
    global maxLipas
    global nykyinenAmmo
    global nykyinenLipas
    global music
    global infiniteAmmo
    global firstTime
    global level
    global score
    global enemiesKilled
    global killsUntilLevelUP
    global damageDone
    global maxAmmoEnemy
    global godMode
    global nykyinenHealth
    global HackStatus

    player = Player(1, 1) # Laita lokaatio pelaajalle ennen sen alkuperäistä määrittämistä
    player = Player((WIDTH - player.ship_img.get_width()) / 2, HEIGHT / 2) # Määritä pelaajan lokaatio
    pelaajat.append(player) # Lisää pelaja player-listaan
    
    # Katso onko pelaaja ensimmäistä kertaa pelissä
    if(firstTime == True):

        # Tee vihollinen
        enemy = Enemy((r.randint(0, WIDTH)), 100)

        # Lisää Vihollinen enemy-listaan
        enemies.append(enemy)

        # Aseta score ja level
        score = 0
        level = 1
        enemiesKilled = 0
        damageDone = 0

        # Musiikki päälle
        music = True
        
        # Aseta aseen data
        maxAmmo = 50
        maxLipas = 350
        maxAmmoEnemy = 350
        infiniteAmmo = False
        
        # Aseta ammot maksimiin
        if (infiniteAmmo == False):
            nykyinenAmmo = maxAmmo
            nykyinenLipas = maxLipas
        else:
            nykyinenAmmo = int(sys.maxsize)
            nykyinenLipas = int(sys.maxsize)

        # Aseta firstTime pois
        firstTime = False

    # Looppaa jos run on True
    run = True
    while run:
        
        # Päivitä FPS:n verran
        clock.tick(FPS)
        
        # Päivitä Hacks-funktio
        HackStatus = infiniteAmmo
        # Laita aseen ammot nollaan jos reload asettaa ne nollan alapuolelle
        if(nykyinenLipas < 0):
            nykyinenLipas = 0
        if(nykyinenAmmo < 0):
            nykyinenAmmo = 0

        
        audio_toggle(music, 1)

        # Jos vihollisia tapettu on yhtä kuin level kertaa Tappoja-Tarvii-Kunnes-Level-UP:
        if(enemiesKilled == level * killsUntilLevelUP):
            # Kutsu lisää uusi level
            level_increase()
            print("Increased Level!")

        # Tee kaikille vihollisille viholliset-listassa
        for enemyy in enemies:
            global atLeft
            global atRight

            # ==ENEMY MOVEMENT==
            if enemyy.x > (player.x + r.randrange(1.0, 10.0)):
                atRight = True
                enemy_shoot(enemyy)
            else:
                atRight = False

            if enemyy.x < (player.x - r.randrange(1.0, 10.0)):
                atLeft = True
                enemy_shoot(enemyy)
            else:
                atLeft = False

            if(atLeft): # Tarkastaa onko vihollinen pelaajan vasemmalla puolella
                enemyy.x += 1

            if(atRight): # Tarkastaar onko vihollinen pelaajan oikealla puolella
                    enemyy.x -= 1
            # ==ENEMY MOVEMENT==

            # ==Vihollisen luodin nopeuden päivitys==     
            enemyy.bullet_move(ENEMY_BULLET_VEL, pelaajat)   


        # Saa kaikki eventit
        for event in game.event.get():
            global text
            # Tarkista jos eventti on poistuminen
            if event.type == game.QUIT:
                # sulje loop
                run = False

            # Jos eventtinä on oma, Päivitä Ammo ja Reload teksti.
            if event.type == game.USEREVENT: 
                Player_Reload_Weapon()
                game.time.set_timer(game.USEREVENT, 0)
                text = ""
                        
                    
            
            # Tunnista jos näppäintä painaa kerran
            if event.type == game.KEYDOWN:
                global gun
                # Reload - Jos R-nappia painetaan
                if (event.key == game.K_r):
                   text = "Ladataan asetta..."
                   game.time.set_timer(game.USEREVENT, (1000 * gun))

                # Vaihda item
                if(event.key == game.K_1):
                    gun = 1
                if(event.key == game.K_2):
                    gun = 2
                if(event.key == game.K_3):
                    gun = 3

                # Vaihda item
                if(event.key == game.K_q):
                    if gun != 3:
                        gun += 1
                    else:
                        gun = 1

                # Jumala tila
                if (event.key == game.K_F5):
                    GodMode()
                    InfiniteAmmo()

                # Tarkasta onko tausta fps:lle päällä
                if (event.key == game.K_INSERT):  # kun insert-nappia painetaan
                    FPS_BG()

                # Tarkasta onko fps päällä
                if (event.key == game.K_HOME):  # kun home-nappia painetaan
                    FPS_Toggle()

                # Jos painetaan "M" nappia, musiikki menee pois päältä tai päälle riippuen sen statuksesta
                if (event.key == game.K_m):
                    MUSIC_TOGGLE()
                    

        # saa lista kaikista näppäimistön näppäimistä joita painetaan pohjassa
        keys_pressed = game.key.get_pressed()

        # Händlää liikkuminen 
        handleMovement(keys_pressed)

        # Piirrä peli-ikkuna
        game_window(player)

        # Jos painetaan ammunta-nappia
        if(keys_pressed[game.K_LSHIFT]):
            player_shoot(player)

        # Jos painetaan esc-nappia
        if(keys_pressed[game.K_ESCAPE]):
            pause_menu()

        # Päivitä luotien nopeus
        player.bullet_move(-PLAYER_BULLET_VEL, enemies)
        

        
    # Lopeta peli jos loop menee pois päältä
    game.quit()

# Kuolema näkymä
def death_screen():
    Button_Space = 10
    title_label_text = " Kuolit noob "
    title_font = game.font.SysFont("comicsans", 50)
    play_audio("Death.mp3", 1)
    run = True
    while run:
        WIN.blit(DEATH_BACKGROUND, (0,0))
        title_label = title_font.render(title_label_text, 1, CYAN, BLACK)

        # Jos "Enemies Killed" muuttuja data-taulukossa on pienempi kuin nykyisen pelin tapetut viholliset, kerro että uusi ennätys on tehty.
        if enemiesKilled > data["Enemies Killed"]:
            results_label = title_font.render(' Vihollisia tapettu: ' + str(enemiesKilled) + " [Ennätys: " + str(data["Enemies Killed"]) + "] UUSI ENNÄTYS!!!!!!!",1, CYAN, BLACK)
        else:
            results_label = title_font.render(' Vihollisia tapettu: ' + str(enemiesKilled) + " [Ennätys: " + str(data["Enemies Killed"]) + "] ",1, CYAN, BLACK)
        
        # Jos "Damage Done" muuttuja data-taulukossa on pienempi kuin nykyisen pelin vihollisiin tehdyt damaget, kerro että uusi ennätys on tehty.
        if damageDone > data['Damage Done']:
            results2_label = title_font.render(" Damagea tehty: " + str(damageDone) + " [Ennätys: " + str(data["Damage Done"]) + "] UUSI ENNÄTYS!!!!!!!",1, CYAN, BLACK)
        else:
            results2_label = title_font.render(" Damagea tehty: " + str(damageDone) + " [Ennätys: " + str(data["Damage Done"]) + "] ",1, CYAN, BLACK)
        
        # Jos "Highscore" muuttuja data-taulukossa on pienempi kuin nykyisen pelin score, kerro että uusi ennätys on tehty.
        if score > data['Highscore']:
            results3_label = title_font.render(" Score: " + str(score) + " [Ennätys: " + str(data["Highscore"]) + "] UUSI ENNÄTYS!!!!!!!",1, CYAN, BLACK)
        else:
            results3_label = title_font.render(" Score: " + str(score) + " [Ennätys: " + str(data["Highscore"]) + "] ",1, CYAN, BLACK)
        
        # Jos "Enemies Killed" muuttuja data-taulukossa on pienempi kuin nykyisen pelin tapetut viholliset, kerro että uusi ennätys on tehty.
        if level > data['Highest Level']:
            results4_label = title_font.render(" Level: " + str(level) + " [Ennätys: " + str(data["Highest Level"]) + "] UUSI ENNÄTYS!!!!!!!",1, CYAN, BLACK)
        else:
            results4_label = title_font.render(" Level: " + str(level) + " [Ennätys: " + str(data["Highest Level"]) + "] ",1, CYAN, BLACK)

        # Piirrä Title "Kuolit noob"
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT / 2 - 50))

        # Piirrä Vihollisia tapettu-teksti
        WIN.blit(results_label, (0, HEIGHT / 2 - 150))

        # Piirrä Damagea tehty-teksti
        WIN.blit(results2_label, (0, HEIGHT / 2 - 250))

        # Piirrä Highscore-teksti
        WIN.blit(results3_label, (0, HEIGHT / 2 - 350))

        # Piirrä Isoin Level-teksti
        WIN.blit(results4_label, (0, HEIGHT / 2 - 450))

        # Piirrä "paina m laittaaksesi musiikin pois päältä" teksti
        WIN.blit(update_current_sound(), (WIDTH/2 - update_current_sound().get_width()/2, HEIGHT - 30))
        
        # Piirrä Poistu pelistä (exit)-nappi
        exit = Button((WIDTH / 2 - (EXIT_SAVE.get_width())), (HEIGHT / 2 + 30), EXIT_SAVE)

        # Piirrä Poista Save (highscore jne..)-nappi
        delete = Button((WIDTH / 2  + Button_Space), (HEIGHT / 2 + 30), DELETE)

        # Jos exit-nappia painaa, niin tallenna score tiedostoon.
        if exit.draw():
            save_score()
            title_label_text = "Tallennettu."
            game.quit()
        
        # Jos delete-nappia painaa, niin poista score tiedosto.
        if delete.draw():
            os.remove("save.txt")
            title_label_text = "Save Poistettu!"
            game.quit()
        
        # Päivitä ikkuna
        game.display.update()

        # Saa kaikki eventit
        for event in game.event.get():

            # Jos eventti on game.QUIT, sulje run-loop
            if(event.type == game.QUIT):
                    run = False
    game.quit()

# Päävalikko
def main_menu():
    global firstTime2
    Button_Space = 10

    # Määritä Title-tekstin fontti Main-Menuun
    title_font = game.font.SysFont("comicsans", 50)
    run = True
    
    # Kun run on päällä-looppi
    while run:
        global music

        Play_MenuMusic(1)

        audio_toggle(music, 1)
        # Piirrä taustakuva
        WIN.blit(BACKGROUND, (0,0))

        # Jos fps counter-bool on päällä, piirrä fps teksti näytölle ja laita otsikoksi nimi & fps
        if (showCounter):
            fps = str(int(clock.get_fps()))
            game.display.set_caption("Testipeli - FPS: " + fps)
            WIN.blit(update_fps(), (10, 10))
        else:
            game.display.set_caption("Testipeli")

        # Piirrä kello-teksti näytölle
        rectClock = update_clock().get_rect()
        WIN.blit(update_clock(), ((WIDTH - rectClock.width -(BORDERTHICKNESS * 5)), 10))     

        # Määritä titlen teksti
        title_label = title_font.render(' Paina "Play" aloittaaksesi... ', 1, CYAN, BLACK)

        # Piirrä title
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT / 2 - 50))
        
        # Piirrä "Paina M laittaaksesi musiikin pois päältä ja päälle pelissä"- teksti
        WIN.blit(update_current_sound(), (WIDTH/2 - update_current_sound().get_width()/2, HEIGHT - 30))

    

        # Piirrä play-nappi
        settings = Button((WIDTH / 2 - SETTINGS.get_width() * 1.5 - Button_Space), (HEIGHT / 2 + 30), SETTINGS)

        # Piirrä settings-nappi
        play = Button((WIDTH / 2 - PLAY.get_width() / 2), (HEIGHT / 2 + 30), PLAY)

        # Piirrä exit-nappi
        exit = Button((WIDTH / 2 + EXIT.get_width() / 2 + Button_Space), (HEIGHT / 2 + 30), EXIT)
        
        # Jos play-nappia painetaan:
        if play.draw():
            firstTime2 = False
            main()
        
        # Jos exit-nappia painetaan:
        if exit.draw():
            game.quit()

        # Jos settings-nappia painetaan:
        if settings.draw():
            firstTime2 = False
            settings_menu()

        # Päivitä ikkuna
        game.display.update()

        # Saa kaikki eventit
        for event in game.event.get():
            if(event.type == game.KEYDOWN):
                 if (event.key == game.K_m):
                    MUSIC_TOGGLE()
            
            # Jos eventti on game.QUIT, sulje loop
            if(event.type == game.QUIT):
                run = False
            

    # Poistu pelistä
    game.quit()

# Asetukset
def settings_menu():
    Button_Space = 10
    # Määritä Title-tekstin fontti Main-Menuun
    title_font = game.font.SysFont("comicsans", 50)
    
    run = True
    
    # Kun run on päällä-looppi
    while run:
        global music
        audio_toggle(music, 1)

        # Piirrä taustakuva
        WIN.blit(BACKGROUND, (0,0))

        # Jos fps counter-bool on päällä, piirrä fps teksti näytölle ja laita otsikoksi nimi & fps
        if (showCounter):
            fps = str(int(clock.get_fps()))
            game.display.set_caption("Testipeli - FPS: " + fps)
            WIN.blit(update_fps(), (10, 10))
        else:
            game.display.set_caption("Testipeli")

        # Piirrä kello-teksti näytölle
        rectClock = update_clock().get_rect()
        WIN.blit(update_clock(), ((WIDTH - rectClock.width -(BORDERTHICKNESS * 5)), 10))

        # Määritä titlen teksti
        title_label = title_font.render('ASETUKSET:', 1, CYAN, BLACK)

        # Piirrä title
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT / 2 - 50))

        
        # Piirrä "Paina M laittaaksesi musiikin pois päältä ja päälle pelissä"- teksti
        WIN.blit(update_current_sound(), (WIDTH/2 - update_current_sound().get_width()/2, HEIGHT - 30))

        # Piirrä settings-nappi
        UltimateFPS = Button((WIDTH / 2 - ULTIMATEFPS.get_width() * 1.5 - Button_Space), (HEIGHT / 2 + 30), ULTIMATEFPS)

        # Piirrä play-nappi
        Fps_Bg = Button((WIDTH / 2 - FPS_BG_BTN.get_width() / 2), (HEIGHT / 2 + 30), FPS_BG_BTN)

        # Piirrä takaisin-nappi
        Back_Bg = Button((WIDTH / 2 - BACK.get_width() / 2), (HEIGHT / 2 + 130), BACK)

        # Piirrä exit-nappi
        Fps = Button((WIDTH / 2 + FPSS.get_width() / 2 + Button_Space), (HEIGHT / 2 + 30), FPSS)
        
        # Jos Musiikki-nappia painetaan:
        if UltimateFPS.draw():
            global FPS
            if(FPS != 60):
                FPS = 60
            else:
                FPS = math.inf
        
        # Jos Fps-BG-nappia painetaan:
        if Fps_Bg.draw():
            FPS_BG()

        # Jos Takaisin-nappia painetaan:
        if Back_Bg.draw():
            main_menu()

        # Jos Fps-toggle-nappia painetaan:
        if Fps.draw():
            FPS_Toggle()

        # Päivitä ikkuna
        game.display.update()

        # Saa kaikki eventit
        for event in game.event.get():
            # Jos eventti on game.QUIT, sulje loop
            if(event.type == game.QUIT):
                run = False
            # Jos even taas on (napin painallus):
            if(event.type == game.KEYDOWN):
                if(event.key == game.K_m):
                    MUSIC_TOGGLE()
    # Poistu pelistä
    game.quit()

# Jos päävalikko-muuttuja on päällä, se menee päävalikkoon, muuten peliin (mulle vaan ku teen tätä peliä niin voin suoraan mennä peliin ilman että pitää poistaa tuo main_menu():n koodi.)
if mainMenu:
    main_menu()
else:
    main()