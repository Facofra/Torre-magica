import pygame
from classes import Vector2, screenWidth, screenHeight, tile_size, tile_quantity, Block, Game, Enemigo, Escalera, Caja, Coin, Tienda, Agujero


pygame.init()

# SETTING
WINDOW = pygame.display.set_mode((screenWidth+200,screenHeight))
SCREEN = pygame.Surface([screenWidth,screenHeight])
pygame.display.set_caption("Test game")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont('papyrus',20,True)


game = Game()
game.niveles[0] =[
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0] 
                ]
game.crearNivel()
mapa = [
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0] 
                ]

bloques =game.bloques
cajas =game.cajas
coins= game.coins
enemigos = game.enemigos
escaleras = [game.escaleraArriba, game.escaleraAbajo]
agujeros = game.agujeros
tienda = game.tienda
menu = game.menu
jugador=game.jugador

def ponerObjeto(numObjeto,x,y):
    global tienda
    if numObjeto ==2:
        bloques.append(Block(x,y)) 
        mapa[y][x] = numObjeto
    elif numObjeto == 3:
        cajas.append(Caja(x,y))
        mapa[y][x] = numObjeto
    elif numObjeto == 4:
        coins.append(Coin(x,y))
        mapa[y][x] = numObjeto
    elif numObjeto == 5:
        enemigos.append(Enemigo(x,y))
        mapa[y][x] = numObjeto
    elif numObjeto == 6:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if mapa[i][j] == numObjeto:
                    mapa[i][j] = 0

        escaleras[0]=Escalera(x,y,"up")
        mapa[y][x] = numObjeto
    elif numObjeto == 7:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if mapa[i][j] == numObjeto:
                    mapa[i][j] = 0

        escaleras[1]=Escalera(x,y,"down")
        mapa[y][x] = numObjeto
    elif numObjeto == 8:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if mapa[i][j] == numObjeto:
                    mapa[i][j] = 0

        tienda=Tienda(x,y)
        mapa[y][x] = numObjeto
    elif numObjeto == 9:
        agujeros.append(Agujero(x,y))
        mapa[y][x] = numObjeto


def quitarObjeto(x,y):
    global tienda
    numObjeto = mapa[y][x]
    if numObjeto ==2:

        for i in range(len(bloques)):
            if bloques[i].cords == Vector2(x,y):
                bloques.pop(i)
                mapa[y][x] = 0
                break

    elif numObjeto == 3:

        for i in range(len(cajas)):
            if cajas[i].cords == Vector2(x,y):
                cajas.pop(i)
                mapa[y][x] = 0
                break

    elif numObjeto == 4:

        for i in range(len(coins)):
            if coins[i].cords == Vector2(x,y):
                coins.pop(i)
                mapa[y][x] = 0
                break

    elif numObjeto == 5:

        for i in range(len(enemigos)):
            if enemigos[i].cords == Vector2(x,y):
                enemigos.pop(i)
                mapa[y][x] = 0
                break

    elif numObjeto == 6:
        if escaleras[0] is not None and escaleras[0].cords == Vector2(x,y):
            escaleras[0]=None
            mapa[y][x] = 0
    elif numObjeto == 7:
        if escaleras[1] is not None and escaleras[1].cords == Vector2(x,y):
            escaleras[1]=None
            mapa[y][x] = 0
    elif numObjeto == 8:
        if tienda is not None and tienda.cords == Vector2(x,y):
            tienda = None
            mapa[y][x] = 0

    elif numObjeto == 9:

        for i in range(len(agujeros)):
            if agujeros[i].cords == Vector2(x,y):
                agujeros.pop(i)
                mapa[y][x] = 0
                break


def main():

    
    run = True
    numObjeto = 2
    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        events = pygame.event.get()


        for event in events:
            
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                x=posicion[0]-200
                y=posicion[1]
                x= int(x/tile_size)
                y= int(y/tile_size)
                
                if event.button ==1:
                    if mapa[y][x]==0:
                        ponerObjeto(numObjeto,x,y)
                elif event.button==3:
                    quitarObjeto(x,y)
                elif event.button==4:
                    if numObjeto < 9:
                        numObjeto+=1
                elif event.button==5:
                    if numObjeto > 2:
                        numObjeto-= 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("[")
                    for i in range(tile_quantity):
                        print("\t[",end="")
                        for j in range(tile_quantity):
                            print(mapa[i][j],end="" )
                            if j < tile_quantity-1:
                                print(",",end="")
                                
                        print("]",end="")
                        if i < tile_quantity-1:
                            print(",")
                    print("\n]")
                elif event.key == pygame.K_w:
                    if numObjeto < 9:
                        numObjeto+=1
                elif event.key == pygame.K_s:
                    if numObjeto > 2:
                        numObjeto-= 1

       
        if keys[pygame.K_ESCAPE]:
            print("Juego terminado")
            run = False

            
        updateWindow(numObjeto)

    pygame.quit()

def updateWindow(numObjeto):
    

    WINDOW.fill((0,0,0))
    WINDOW.blit(SCREEN,(200,0))
    SCREEN.fill((100,0,100))
    
    for i in range(1,tile_quantity):
        pygame.draw.line(SCREEN,(0,0,0),(0,i*50),(screenWidth,i*50))
        pygame.draw.line(SCREEN,(0,0,0),(i*50,0),(i*50,screenHeight))

    for block in bloques:
        block.draw(SCREEN)
    for caja in cajas:
        caja.draw(SCREEN)
    for coin in coins:
        coin.draw(SCREEN)
    for enemigo in enemigos:
        enemigo.draw(SCREEN)
    for agujero in agujeros:
        agujero.draw(SCREEN)

    for escalera in escaleras:
        try:
            escalera.draw(SCREEN)
        except:
            pass
    if tienda is not None:
        tienda.draw(SCREEN)

    
    if numObjeto ==2:
        
        objeto= "bloques"
    elif numObjeto == 3:
        
        objeto= "cajas"
    elif numObjeto == 4:
        
        objeto= "coins"
    elif numObjeto == 5:
        
        objeto= "enemigos"
    elif numObjeto == 6:
        
        objeto= "escalera Arriba"
    elif numObjeto == 7:
        
        objeto= "escalera Abajo"
    elif numObjeto == 8:
        
        objeto= "tienda"
    elif numObjeto == 9:
        
        objeto= "agujero"



    goldText = font.render(objeto , 1 , (255,255,255))

    WINDOW.blit(goldText,(10,10))




    pygame.display.update()

if __name__ == "__main__":
    main()


