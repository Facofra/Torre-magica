import pygame
from pygame.math import Vector2

tile_size=50
tile_quantity=12

screenWidth = tile_size * tile_quantity
screenHeight = tile_size * tile_quantity

enemy1 = pygame.image.load('images/enemy1.png')


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
        self.width=tile_size - 20
        self.height=tile_size - 20
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

class Game:
    def __init__(self):
        self.pause=False

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
        self.gold=0
        
    def draw(self,SCREEN):
        SCREEN.blit(enemy1,self.position)