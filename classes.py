import pygame, copy
from pygame.math import Vector2

tile_size=50
tile_quantity=12

screenWidth = tile_size * tile_quantity
screenHeight = tile_size * tile_quantity

enemy1 = pygame.image.load('images/enemy1.png')

class Game:
    def __init__(self):
        self.pause=False
        self.bloques=[]
        self.cajas=[]
        self.coins=[]
        self.enemigos=[]
        self.tienda = Tienda(21,21)
        self.jugador=Jugador(20,20)
        self.escaleraArriba=Escalera(20,20,"up")
        self.escaleraAbajo=Escalera(20,20,"down")
        self.menu = Menu()
        self.nivel = 0
        self.niveles=[
[
    [0,0,0,0,0,0,6,0,0,0,0,4],
    [4,0,0,0,2,2,2,0,0,0,0,0],
    [4,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,4,0,4],
    [4,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,5,0,0,0,0],
    [0,0,0,2,0,0,0,0,3,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0,5],
    [0,0,4,0,0,0,0,0,4,0,5,8],
    [0,0,0,0,3,0,0,0,1,0,0,5]
],
[
    [0,0,0,0,0,0,7,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0,0,0,0],
    [0,0,0,2,5,2,0,0,0,0,0,0],
    [0,0,0,2,0,2,0,0,0,0,0,0],
    [2,2,2,2,0,2,2,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,0,0,0,0]
]

        ]
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
                    self.bloques.append(Block(x,y))
                elif nivel[i][j] == 3:
                    x=j
                    y=i
                    self.cajas.append(Caja(x,y))
                elif nivel[i][j] == 4:
                    x=j
                    y=i
                    self.coins.append(Coin(x,y))
                elif nivel[i][j] == 5:
                    x=j
                    y=i
                    self.enemigos.append(Enemigo(x,y))
                elif nivel[i][j] == 6:
                    x=j
                    y=i
                    self.escaleraArriba=Escalera(x,y,"up")
                elif nivel[i][j] == 7:
                    x=j
                    y=i
                    self.escaleraAbajo=Escalera(x,y,"down")
                elif nivel[i][j] == 8:
                    x=j
                    y=i
                    self.tienda=Tienda(x,y)

                if self.escaleraAbajo==None:
                    self.escaleraAbajo = Escalera(20,20,"down")
                if self.escaleraArriba==None:
                    self.escaleraArriba = Escalera(20,20,"up")

    def vaciarGameObjects(self):
        self.bloques=[]
        self.cajas=[]
        self.coins=[]
        self.enemigos=[]
        self.escaleraArriba=None
        self.escaleraAbajo=None
        self.tienda = Tienda(21,21)

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
        self.niveles=self.nivelesIntactos
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
        self.health=10
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
    def __init__(self,x,y):
        self.cords =Vector2(x,y)
        self.offset=9
        self.position = Vector2(self.cords.x * tile_size  + self.offset,self.cords.y * tile_size + self.offset)
        self.width= tile_size - self.offset*2
        self.height= tile_size - self.offset*2
        self.color =  (255, 101, 68)
        self.vel = tile_size
        self.health=5
        self.attack = 2
        self.defense = 0
        self.gold=1
        
    def draw(self,SCREEN):
        SCREEN.blit(enemy1,self.position)

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


