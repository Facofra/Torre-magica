import pygame, copy
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


game.crearNivel()
                
newLevel = [
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


jugador=game.jugador

def ponerObjeto(numObjeto,x,y):
    if numObjeto ==2:
        game.gameObjects["bloques"].append(Block(x,y)) 
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 3:
        game.gameObjects["cajas"].append(Caja(x,y))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 4:
        game.gameObjects["coins"].append(Coin(x,y))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 50:
        game.gameObjects["enemigos"].append(Enemigo(x,y,0))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 51:
        game.gameObjects["enemigos"].append(Enemigo(x,y,1))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 52:
        game.gameObjects["enemigos"].append(Enemigo(x,y,2))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 53:
        game.gameObjects["enemigos"].append(Enemigo(x,y,3))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 54:
        game.gameObjects["enemigos"].append(Enemigo(x,y,4))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 55:
        game.gameObjects["enemigos"].append(Enemigo(x,y,5))
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 6:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if game.niveles[game.nivel][i][j] == numObjeto:
                    game.niveles[game.nivel][i][j] = 0

        game.gameObjects["escaleras"][0]=Escalera(x,y,"up")
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 7:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if game.niveles[game.nivel][i][j] == numObjeto:
                    game.niveles[game.nivel][i][j] = 0

        game.gameObjects["escaleras"][1]=Escalera(x,y,"down")
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 8:
        for i in range(tile_quantity):
            for j in range(tile_quantity):
                if game.niveles[game.nivel][i][j] == numObjeto:
                    game.niveles[game.nivel][i][j] = 0

        game.gameObjects["tiendas"][0]=Tienda(x,y)
        game.niveles[game.nivel][y][x] = numObjeto
    elif numObjeto == 9:
        game.gameObjects["agujeros"].append(Agujero(x,y))
        game.niveles[game.nivel][y][x] = numObjeto


def quitarObjeto(x,y):
    numObjeto = game.niveles[game.nivel][y][x]
    if numObjeto ==2:

        for i in range(len(game.gameObjects["bloques"])):
            if game.gameObjects["bloques"][i].cords == Vector2(x,y):
                game.gameObjects["bloques"].pop(i)
                game.niveles[game.nivel][y][x] = 0
                break

    elif numObjeto == 3:

        for i in range(len(game.gameObjects["cajas"])):
            if game.gameObjects["cajas"][i].cords == Vector2(x,y):
                game.gameObjects["cajas"].pop(i)
                game.niveles[game.nivel][y][x] = 0
                break

    elif numObjeto == 4:

        for i in range(len(game.gameObjects["coins"])):
            if game.gameObjects["coins"][i].cords == Vector2(x,y):
                game.gameObjects["coins"].pop(i)
                game.niveles[game.nivel][y][x] = 0
                break

    elif numObjeto >= 50 and numObjeto <60:

        for i in range(len(game.gameObjects["enemigos"])):
            if game.gameObjects["enemigos"][i].cords == Vector2(x,y):
                game.gameObjects["enemigos"].pop(i)
                game.niveles[game.nivel][y][x] = 0
                break

    elif numObjeto == 6:
        if game.gameObjects["escaleras"][0] is not None and game.gameObjects["escaleras"][0].cords == Vector2(x,y):
            game.gameObjects["escaleras"][0]=None
            game.niveles[game.nivel][y][x] = 0
    elif numObjeto == 7:
        if game.gameObjects["escaleras"][1] is not None and game.gameObjects["escaleras"][1].cords == Vector2(x,y):
            game.gameObjects["escaleras"][1]=None
            game.niveles[game.nivel][y][x] = 0
    elif numObjeto == 8:
        if game.gameObjects["tiendas"][0] is not None and game.gameObjects["tiendas"][0].cords == Vector2(x,y):
            game.gameObjects["tiendas"][0] = None
            game.niveles[game.nivel][y][x] = 0

    elif numObjeto == 9:

        for i in range(len(game.gameObjects["agujeros"])):
            if game.gameObjects["agujeros"][i].cords == Vector2(x,y):
                game.gameObjects["agujeros"].pop(i)
                game.niveles[game.nivel][y][x] = 0
                break


def main():

    
    run = True
    numObjeto = 2
    nivelAnterior = game.nivel
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
                    if game.niveles[game.nivel][y][x]==0:
                        ponerObjeto(numObjeto,x,y)
                elif event.button==3:
                    quitarObjeto(x,y)
                elif event.button==4:

                    if numObjeto==4:
                        numObjeto+=1
                    if numObjeto==9:
                        numObjeto=49

                    if numObjeto < 55:
                        numObjeto+=1

                elif event.button==5:

                    if numObjeto== 6:
                        numObjeto-=1
                    if numObjeto== 50:
                        numObjeto=10
                    if numObjeto > 2:
                        numObjeto-= 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    print(" --------nivel: " , str(game.nivel) , "------------------")
                    print("[")
                    for i in range(tile_quantity):
                        print("\t[",end="")
                        for j in range(tile_quantity):
                            print(game.niveles[game.nivel][i][j],end="" )
                            if j < tile_quantity-1:
                                print(",",end="")
                                
                        print("]",end="")
                        if i < tile_quantity-1:
                            print(",")
                    print("\n]")

                elif event.key == pygame.K_RETURN:
                    print(" --------Todos los niveles: " , str(len(game.niveles)) , "------------------")
                    for nivel in game.niveles:
                        print("[")
                        for i in range(tile_quantity):
                            print("\t[",end="")
                            for j in range(tile_quantity):
                                print(nivel[i][j],end="" )
                                if j < tile_quantity-1:
                                    print(",",end="")
                                    
                            print("]",end="")
                            if i < tile_quantity-1:
                                print(",")
                        print("\n],")
                    print(" --------Fin de imprimir Todos los niveles------------------")



                elif event.key == pygame.K_w:
                    if numObjeto==4:
                        numObjeto+=1
                    if numObjeto==9:
                        numObjeto=49

                    if numObjeto < 55:
                        numObjeto+=1
                elif event.key == pygame.K_s:
                    if numObjeto== 6:
                        numObjeto-=1
                    if numObjeto== 50:
                        numObjeto=10
                    if numObjeto > 2:
                        numObjeto-= 1

                elif event.key == pygame.K_d:
                    if game.nivel < len(game.niveles)-1:
                        game.subir()
                        actualizarGameObjects()
                        
                elif event.key == pygame.K_a:
                    if game.nivel > 0:
                        game.bajar()
                        actualizarGameObjects()

                elif event.key == pygame.K_SPACE:
                    if game.nivel == len(game.niveles)-1:
                        game.niveles.append(copy.deepcopy(newLevel))
                        game.subir()
                        actualizarGameObjects()
                        
       
        if keys[pygame.K_ESCAPE]:
            print("Juego terminado")
            run = False

            
        updateWindow(numObjeto)

    pygame.quit()

def updateWindow(numObjeto):
    

    WINDOW.fill((0,0,0))
    WINDOW.blit(SCREEN,(200,0))
    SCREEN.fill((129, 129, 129))
    
    for i in range(1,tile_quantity):
        pygame.draw.line(SCREEN,(0,0,0),(0,i*50),(screenWidth,i*50))
        pygame.draw.line(SCREEN,(0,0,0),(i*50,0),(i*50,screenHeight))

    for key in game.gameObjects:
            for objeto in game.gameObjects[key]:
                try:
                    objeto.draw(SCREEN)
                except:
                    pass

    
    if numObjeto ==2:
        
        objeto= "bloques"
    elif numObjeto == 3:
        
        objeto= "cajas"
    elif numObjeto == 4:
        
        objeto= "coins"
    elif numObjeto == 50:
        
        objeto= "enemigo1"
    elif numObjeto == 51:
        
        objeto= "enemigo2"
    elif numObjeto == 52:
        
        objeto= "enemigo3"
    elif numObjeto == 53:
        
        objeto= "enemigo4"
    elif numObjeto == 54:
        
        objeto= "enemigo5"
    elif numObjeto == 55:
        
        objeto= "enemigo6"
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
    nivel = font.render("nivel: " + str(game.nivel) , 1 , (255,255,255))
    WINDOW.blit(nivel,(10,50))





    pygame.display.update()

def actualizarGameObjects():
    jugador=game.jugador


if __name__ == "__main__":
    main()


