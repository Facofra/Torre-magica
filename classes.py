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
        self.pause=False
        self.jugador=Jugador(20,20)
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
        self.niveles=TEST_LEVELS
        self.nivelesIntactos = copy.deepcopy(self.niveles)
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
                    enemigo = Enemigo(x,y,0)
                    enemigo.crearStats()
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 51:
                    x=j
                    y=i
                    enemigo = Enemigo(x,y,1)
                    enemigo.crearStats()
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 52:
                    x=j
                    y=i
                    enemigo = Enemigo(x,y,2)
                    enemigo.crearStats()
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 53:
                    x=j
                    y=i
                    enemigo = Enemigo(x,y,3)
                    enemigo.crearStats()
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 54:
                    x=j
                    y=i
                    enemigo = Enemigo(x,y,4)
                    enemigo.crearStats()
                    self.gameObjects["enemigos"].append(enemigo)
                    
                elif nivel[i][j] == 55:
                    x=j
                    y=i
                    enemigo = Enemigo(x,y,5)
                    enemigo.crearStats()
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
        pass

    def bajar(self):
        self.nivel-=1
        self.vaciarGameObjects()
        self.crearNivel()
        pass

    def restart(self):
        self.niveles= copy.deepcopy(self.nivelesIntactos)
        self.vaciarGameObjects()
        self.jugador=Jugador(20,20)
        self.nivel=0
        self.crearNivel()
        

class Jugador:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=10
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.color =  (255, 101, 68)
        self.vel = tile_size
        self.facing = "right"
        self.health=40
        self.attack = 1
        self.defense = 1
        self.gold=0
        
        
    def draw(self,SCREEN):
        pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        
        if self.facing == "left":
            pygame.draw.line(SCREEN,(0,0,0),(self.position.x,self.position.y + self.height/2),(self.position.x + self.width/2, self.position.y +self.height/2),2)
        elif self.facing == "right":
            pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2, self.position.y + self.height/2),( self.position.x + self.width, self.position.y +self.height/2),2)
        elif self.facing == "up":
            pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2,self.position.y),(self.position.x + self.width/2,self.position.y + self.height/2),2)
        elif self.facing == "down":
            pygame.draw.line(SCREEN,(0,0,0),(self.position.x + self.width/2,self.position.y + self.height/2),(self.position.x + self.width/2,self.position.y + self.height),2)
    
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
        self.offset=10
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        self.color =  ( 203, 203, 225 )
        

    def draw(self,SCREEN):
        pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )

class Caja(Block):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = (255,0,0)

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

class Coin:

    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=tile_size/2
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - 20
        self.height=tile_size - 20
        self.color =  pygame.color.Color("gold")
    def draw(self,SCREEN):
        pygame.draw.circle(SCREEN,self.color, self.position, 10 )

class Enemigo:
    def __init__(self,x,y,numEnemigo):
        self.cords =Vector2(x,y)
        self.offset=9
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.numEnemigo=numEnemigo
        self.health=3
        self.attack = 3
        self.defense = 0
        self.gold=1
        self.sprites=[
            pygame.image.load('images/enemy1.png'),
            pygame.image.load('images/enemy2.png'),
            pygame.image.load('images/enemy3.png'),
            pygame.image.load('images/enemy4.png'),
            pygame.image.load('images/enemy5.png'),
            pygame.image.load('images/enemy6.png')
        ]
        
    def crearStats(self):
        if self.numEnemigo==0:
            self.health = 3
            self.attack = 3
            self.defense = 0
            self.gold = 1
        elif self.numEnemigo==1:
            self.health = 4
            self.attack = 4
            self.defense = 1
            self.gold = 2
        elif self.numEnemigo==2:
            self.health = 10
            self.attack = 4
            self.defense = 3
            self.gold = 2
        elif self.numEnemigo==3:
            self.health = 10
            self.attack = 4
            self.defense = 4
            self.gold = 4
        elif self.numEnemigo==4:
            self.health = 15
            self.attack = 5
            self.defense = 5
            self.gold = 5
        elif self.numEnemigo==5:
            self.health = 5
            self.attack = 10
            self.defense = 5
            self.gold = 10

    def draw(self,SCREEN):
        SCREEN.blit(self.sprites[self.numEnemigo],self.position)

class Escalera:
    def __init__(self,x,y,direction):
        self.cords =Vector2(x,y)
        self.offset=5
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.color =  ( 0, 203, 225 )
        self.direction=direction
    def draw(self,SCREEN):
        font = pygame.font.SysFont('papyrus',15,True)
        upText = font.render('up ', 1 , (255,255,255))
        downText = font.render('down ', 1 , (255,255,255))
        if self.direction == "up":
            pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
            SCREEN.blit(upText,(self.position.x, self.position.y))
        elif self.direction == "down":
            pygame.draw.rect(SCREEN,(203,0,222), (self.position.x,self.position.y,self.width,self.height) )
            SCREEN.blit(downText,(self.position.x, self.position.y))

class Tienda:
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=1
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width=tile_size - self.offset*2
        self.height=tile_size - self.offset*2
        self.color =  (93, 194, 72)

    def draw(self,SCREEN):
        font = pygame.font.SysFont('papyrus',15,True)
        shopText = font.render('shop ', 1 , (255,255,255))
        pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        SCREEN.blit(shopText,(self.position.x, self.position.y))

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
        

    def draw(self,SCREEN):
        # pygame.draw.rect(SCREEN,self.color, (self.position.x,self.position.y,self.width,self.height) )
        MENU = pygame.Surface([self.width,self.height])
        font = pygame.font.SysFont('papyrus',20,True)
        hpText = font.render('+ Hp ', 1 , (255,255,255))
        attText = font.render('+ Att ', 1 , (255,255,255))
        defText = font.render('+ Def ', 1 , (255,255,255))
        exitText = font.render('Exit ', 1 , (255,255,255))
        costText = font.render('Cost: 10 Gold ', 1 , (255,255,255))

        textHeight= hpText.get_height()
        textWidth= hpText.get_width()
        self.textHeight=textHeight
        self.textWidth=textWidth

        pygame.draw.polygon(MENU, (0,255,255), [[textWidth+40,textHeight* 2+ 20+ self.arrowPosition], [textWidth+30,textHeight* 2+ 25+ self.arrowPosition], [textWidth+40,textHeight* 2+ 30+ self.arrowPosition]], 0)
        
        MENU.blit(costText,(10,10))
        MENU.blit(hpText,(10,10 + textHeight *2))
        MENU.blit(attText,(10,10 + textHeight * 4))
        MENU.blit(defText,(10,10 + textHeight * 6))

        MENU.blit(exitText,(10, self.height - textHeight))
        SCREEN.blit(MENU,(self.position.x, self.position.y))


