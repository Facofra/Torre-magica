import pygame, copy
from pygame.math import Vector2
from levels import LEVELS
from testLevels import TEST_LEVELS

tile_size=50
tile_quantity=12

screenWidth = tile_size * tile_quantity
screenHeight = tile_size * tile_quantity


class Game:
    def __init__(self):
        self.jugador=Jugador(20,20)
        self.pause=Pause()
        self.menu = Menu()
        self.gameObjects = {
            "bloques": [],
            "cajas":[],
            "coins":[],
            "enemigos":[],
            "agujeros":[],
            "tiendas": [Tienda(21,21)],
            "escaleras":[Escalera(20,20,"up"), Escalera(20,20,"down")]
        }
        self.nivel = 0
        self.niveles=LEVELS
        self.nivelesIntactos = copy.deepcopy(self.niveles)
        self.killedEnemies=[None] * 6
        self.actualLevel = copy.deepcopy(self.niveles[self.nivel])
        self.actualLevelJugador = {
            "health":self.jugador.health,
            "attack":self.jugador.attack,
            "defense":self.jugador.defense,
            "gold":self.jugador.gold,
        }
        self.bg = pygame.image.load('images/bg.png')
        self.heart = pygame.image.load('images/heart.png')
        self.sword = pygame.image.load('images/attack.png')
        self.shield = pygame.image.load('images/defense.png')
        self.gold = pygame.image.load('images/gold.png')

    def crearNivel(self):
        nivel = self.niveles[self.nivel]
        for i in range(len(nivel)):
            for j in range(len(nivel[i])):
                if nivel[i][j] == 1:
                    x=j
                    y=i
                    self.jugador.cords =Vector2(x,y)
                    self.jugador.position =Vector2(x * tile_size  + self.jugador.offset, y * tile_size + self.jugador.offset)
                if nivel[i][j] == 2:
                    x=j
                    y=i
                    self.gameObjects["bloques"].append(Block(x,y))
                elif nivel[i][j] == 3:
                    x=j
                    y=i
                    self.gameObjects["cajas"].append(Caja(x,y))
                elif nivel[i][j] == 4:
                    x=j
                    y=i
                    self.gameObjects["coins"].append(Coin(x,y))
                elif nivel[i][j] == 50:
                    x=j
                    y=i
                    enemigo = Enemigo0(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 51:
                    x=j
                    y=i
                    enemigo = Enemigo1(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 52:
                    x=j
                    y=i
                    enemigo = Enemigo2(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 53:
                    x=j
                    y=i
                    enemigo = Enemigo3(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 54:
                    x=j
                    y=i
                    enemigo = Enemigo4(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 55:
                    x=j
                    y=i
                    enemigo = Enemigo5(x,y)
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 6:
                    x=j
                    y=i
                    self.gameObjects["escaleras"][0]=Escalera(x,y,"up")
                elif nivel[i][j] == 7:
                    x=j
                    y=i
                    self.gameObjects["escaleras"][1]=Escalera(x,y,"down")
                elif nivel[i][j] == 8:
                    x=j
                    y=i
                    self.gameObjects["tiendas"][0]=Tienda(x,y)
                elif nivel[i][j] == 9:
                    x=j
                    y=i
                    self.gameObjects["agujeros"].append(Agujero(x,y))

                if self.gameObjects["escaleras"][1]==None:
                    self.gameObjects["escaleras"][1] = Escalera(20,20,"down")
                if self.gameObjects["escaleras"][0]==None:
                    self.gameObjects["escaleras"][0] = Escalera(20,20,"up")

    def vaciarGameObjects(self):
        self.gameObjects["bloques"]=[]
        self.gameObjects["cajas"]=[]
        self.gameObjects["coins"]=[]
        self.gameObjects["enemigos"]=[]
        self.gameObjects["agujeros"]=[]
        self.gameObjects["escaleras"][0]=None
        self.gameObjects["escaleras"][1]=None
        self.gameObjects["tiendas"][0] = Tienda(21,21)

    def subir(self):
        self.nivel+=1
        self.vaciarGameObjects()
        self.crearNivel()
        self.backUpReset()
        
    def bajar(self):
        self.nivel-=1
        self.vaciarGameObjects()
        self.crearNivel()
        self.backUpReset()
        
    def restart(self):
        self.niveles= copy.deepcopy(self.nivelesIntactos)
        self.vaciarGameObjects()
        self.killedEnemies=[None] * 6
        self.jugador=Jugador(20,20)
        self.nivel=0
        self.crearNivel()
        self.backUpReset()

    def backUpReset(self):
        self.actualLevel = copy.deepcopy(self.niveles[self.nivel])
        self.actualLevelJugador = {
            "health":self.jugador.health,
            "attack":self.jugador.attack,
            "defense":self.jugador.defense,
            "gold":self.jugador.gold,
        }

    def resetLevel(self):
        self.niveles[self.nivel] = copy.deepcopy(self.actualLevel)
        self.actualLevelJugador["gold"] -= 1
        self.jugador.health = self.actualLevelJugador["health"]
        self.jugador.attack = self.actualLevelJugador["attack"]
        self.jugador.defense = self.actualLevelJugador["defense"]
        self.jugador.gold = self.actualLevelJugador["gold"]
        self.vaciarGameObjects()
        self.crearNivel()

class Jugador:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=5
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.color =  (255, 101, 68)
        self.vel = tile_size
        self.facing = "right"
        self.health=50
        self.attack = 1
        self.defense = 1
        self.gold=0
        self.sprites = {
            "down": [pygame.image.load('images/knight/knight_01.png'),pygame.image.load('images/knight/knight_02.png'),pygame.image.load('images/knight/knight_03.png')],
            "up": [pygame.image.load('images/knight/knight_04.png'),pygame.image.load('images/knight/knight_05.png'),pygame.image.load('images/knight/knight_06.png')],
            "left": [pygame.image.load('images/knight/knight_07.png'), pygame.image.load('images/knight/knight_09.png'), pygame.image.load('images/knight/knight_11.png')],
            "right": [pygame.image.load('images/knight/knight_08.png'),pygame.image.load('images/knight/knight_10.png'),pygame.image.load('images/knight/knight_12.png')]
        }
        self.moving =0
        
        
    def draw(self,SCREEN):
        # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )

        if self.facing == "left":
            # pygame.draw.line(SCREEN,(0,0,0),(self.position.x,self.position.y + self.height/2),(self.position.x + self.width/2, self.position.y +self.height/2),2)
            SCREEN.blit(self.sprites["left"][self.moving],self.position)

        elif self.facing == "right":
            # pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2, self.position.y + self.height/2),( self.position.x + self.width, self.position.y +self.height/2),2)
            SCREEN.blit(self.sprites["right"][self.moving],self.position)

        elif self.facing == "up":
            # pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2,self.position.y),(self.position.x + self.width/2,self.position.y + self.height/2),2)
            SCREEN.blit(self.sprites["up"][self.moving],self.position)

        elif self.facing == "down":
            # pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2,self.position.y + self.height/2),(self.position.x + self.width/2,self.position.y + self.height),2)
            SCREEN.blit(self.sprites["down"][self.moving],self.position)

    
    def collides(self,objetos,direction):
        if direction == "left":
            tupla = (-1,0)
        elif direction == "right":
            tupla = (1, 0)
        elif direction == "up":
            tupla = (0, -1)
        elif direction == "down":
            tupla = (0,1)

        if type(objetos) is list:
            for objeto in objetos:
                if self.cords + tupla == objeto.cords:
                    return True
            return False 
        else:
            return self.cords + tupla == objetos.cords

    def move(self,direction):
        if direction == "left":
            self.position.x -= tile_size
            self.cords += (-1,0)
        elif direction == "right":
            self.position.x += tile_size
            self.cords += (1, 0)
        elif direction == "up":
            self.position.y -= tile_size
            self.cords += (0, -1)
        elif direction == "down":
            self.position.y += tile_size
            self.cords += (0,1)            
      
class Block:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=0
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        # self.color =  ( 180, 180, 205 )
        self.sprite = pygame.image.load('images/wall.png')
        

    def draw(self,SCREEN):
        # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        SCREEN.blit(self.sprite,self.position)

class Caja(Block):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.offset=10
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        self.sprite = pygame.image.load('images/caja.png')

    def move(self,direction):
        if direction == "left":
            self.position.x -= tile_size
            self.cords += (-1,0)
        elif direction == "right":
            self.position.x += tile_size
            self.cords += (1, 0)
        elif direction == "up":
            self.position.y -= tile_size
            self.cords += (0, -1)
        elif direction == "down":
            self.position.y += tile_size
            self.cords += (0,1)

    def collides(self,objetos,direction):
        if direction == "left":
            tupla = (-1,0)
        elif direction == "right":
            tupla = (1, 0)
        elif direction == "up":
            tupla = (0, -1)
        elif direction == "down":
            tupla = (0,1)

        if type(objetos) is list:
            for objeto in objetos:
                if type(objeto) is list:
                    for subObjeto in objeto:
                        if self.cords + tupla == subObjeto.cords:
                            return True
                else:
                    if self.cords + tupla == objeto.cords:
                        return True
            return False 
        else:
            return self.cords + tupla == objetos.cords

    def draw(self,SCREEN):
        SCREEN.blit(self.sprite,(self.position.x, self.position.y)) 


class Coin:

    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset= 10 # tile_size/2
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - 20
        self.height=tile_size - 20
        self.color =  pygame.color.Color("gold")
        self.actualSprite=0
        self.sprites=[
            pygame.image.load('images/coins/coin0.png'),
            pygame.image.load('images/coins/coin1.png'),
            pygame.image.load('images/coins/coin2.png'),
            pygame.image.load('images/coins/coin3.png'),
            pygame.image.load('images/coins/coin4.png'),
            pygame.image.load('images/coins/coin5.png')
        ]
    def draw(self,SCREEN):
        # pygame.draw.circle(SCREEN,self.color, self.position, 10 )
        SCREEN.blit(self.sprites[self.actualSprite//7],(self.position.x, self.position.y)) 
        self.actualSprite+=1
        if self.actualSprite == 42:
            self.actualSprite=0




class Enemigo:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=9
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.health=0
        self.attack = 0
        self.defense = 0
        self.gold=0
        

    def draw(self,SCREEN):
        SCREEN.blit(self.sprite,self.position)

class Enemigo0(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health=3
        self.attack = 3
        self.defense = 0
        self.gold=1
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy0.png')
class Enemigo1(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health = 4
        self.attack = 3
        self.defense = 1
        self.gold = 2
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy1.png')
class Enemigo2(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health = 10
        self.attack = 4
        self.defense = 3
        self.gold = 3
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy2.png')
class Enemigo3(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health = 10
        self.attack = 5
        self.defense = 4
        self.gold = 4
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy3.png')
class Enemigo4(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health = 10
        self.attack = 6
        self.defense = 5
        self.gold = 5
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy4.png')
class Enemigo5(Enemigo):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.health = 15
        self.attack = 7
        self.defense = 5
        self.gold = 10
        self.hp = self.health
        self.sprite= pygame.image.load('images/enemy5.png')

class Escalera:
    def __init__(self,x,y,direction):
        self.cords =Vector2(x,y)
        self.offset=0
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.color =  ( 0, 203, 225 )
        self.direction=direction
        self.sprites=[
            pygame.image.load('images/stair0.png'),
            pygame.image.load('images/stair1.png')
        ]
    def draw(self,SCREEN):
        font = pygame.font.SysFont('papyrus',15,True)
        upText = font.render('up ', 1 , (255,255,255))
        downText = font.render('down ', 1 , (255,255,255))
        if self.direction == "up":
            # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
            # SCREEN.blit(upText,(self.position.x, self.position.y))
            SCREEN.blit(self.sprites[1],(self.position.x, self.position.y))
        elif self.direction == "down":
            # pygame.draw.rect(SCREEN,(203,0,222), (self.position.x,self.position.y,self.width,self.height) )
            # SCREEN.blit(downText,(self.position.x, self.position.y))
            SCREEN.blit(self.sprites[0],(self.position.x, self.position.y))

class Tienda:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=9
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        self.color =  (93, 194, 72)
        self.sprite= pygame.image.load('images/shop.png')

    def draw(self,SCREEN):
        # font = pygame.font.SysFont('papyrus',15,True)
        # shopText = font.render('shop ', 1 , (255,255,255))
        # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        # SCREEN.blit(shopText,(self.position.x, self.position.y)) 
        SCREEN.blit(self.sprite,(self.position.x, self.position.y)) 

class Agujero:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=10
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        self.color = ( 0, 0, 0 )
        

    def draw(self,SCREEN):
        pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        

class Menu:
    def __init__(self):
        self.cords =Vector2(3,3)
        self.offset=0
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size * 6
        self.height=tile_size * 6
        self.color =  ( 203, 203, 225 )
        self.arrowPosition=0
        self.active=False
        self.textHeight=0
        self.textWidth=0
        self.heart = pygame.image.load('images/heart.png')
        self.sword = pygame.image.load('images/attack.png')
        self.shield = pygame.image.load('images/defense.png')
        self.gold = pygame.image.load('images/gold.png')
        

    def draw(self,SCREEN):
        # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        MENU = pygame.Surface([self.width,self.height])
        font = pygame.font.SysFont('papyrus',20,True)
        hpText = font.render('+20 ', 1 , (255,255,255))
        attText = font.render('+1 ', 1 , (255,255,255))
        defText = font.render('+1 ', 1 , (255,255,255))
        exitText = font.render('Exit ', 1 , (255,255,255))
        costText = font.render('Cost: 10  ', 1 , (255,255,255))

        textHeight= hpText.get_height()
        textWidth= hpText.get_width()
        self.textHeight=textHeight
        self.textWidth=textWidth

    # iconos
        MENU.blit(self.gold,(115,10))
        MENU.blit(self.heart,(50,10 + textHeight *2))
        MENU.blit(self.sword,(35,10 + textHeight * 4))
        MENU.blit(self.shield,(35,10 + textHeight * 6))

    # textos 
        MENU.blit(costText,(10,10))
        MENU.blit(hpText,(10,10 + textHeight *2))
        MENU.blit(attText,(10,10 + textHeight * 4))
        MENU.blit(defText,(10,10 + textHeight * 6))
        MENU.blit(exitText,(10, self.height - textHeight))

        pygame.draw.polygon(MENU, (0,255,255), [
            [textWidth+60,textHeight* 2+ 20+ self.arrowPosition],
            [textWidth+50,textHeight* 2+ 25+ self.arrowPosition],
            [textWidth+60,textHeight* 2+ 30+ self.arrowPosition]
              ], 0)
        SCREEN.blit(MENU,(self.position.x, self.position.y))

class Pause:
    def __init__(self):
        self.arrowPosition=0
        self.isPaused=False
        self.x =screenWidth/2 - 100
        self.y = 150
        self.separacion = 50

    def draw(self,SCREEN):

        font = pygame.font.SysFont('papyrus',20,True)

        pauseText = font.render('Pause ', 1 , (255,255,255))
        continueText = font.render('Continue ', 1 , (255,255,255))
        resetText = font.render('Reset Floor (1 gold cost) ', 1 , (255,255,255))
        restartText = font.render('Restart ', 1 , (255,255,255))
        exitText = font.render('Exit Game', 1 , (255,255,255))

        textHeight= resetText.get_height()
        textWidth= resetText.get_width()

        pygame.draw.polygon(SCREEN, (0,255,255), [
            [self.x- 35,self.y+ 10+ self.arrowPosition * self.separacion],
            [self.x- 25,self.y+ 15+ self.arrowPosition * self.separacion],
            [self.x- 35,self.y+ 20+ self.arrowPosition * self.separacion]
            ], 0)

        # pygame.draw.rect(SCREEN,(122,11,21), (self.x,20,20,20) )
        
        
        SCREEN.blit(pauseText,(self.x,20))
        SCREEN.blit(continueText,(self.x,self.y))
        SCREEN.blit(resetText,(self.x,self.y + self.separacion ))
        SCREEN.blit(restartText,(self.x,self.y + self.separacion * 2))
        SCREEN.blit(exitText,(self.x,self.y + self.separacion * 3))