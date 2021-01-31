import pygame
from classes import Vector2, screenWidth, screenHeight, tile_size, tile_quantity, Game


pygame.init()

# SETTING
WINDOW = pygame.display.set_mode((screenWidth+200,screenHeight))
SCREEN = pygame.Surface([screenWidth,screenHeight])
pygame.display.set_caption("Test game")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont('papyrus',20,True)


# SONIDOS
caminarSound = pygame.mixer.Sound('Sounds/caminar.mp3')
coinSound = pygame.mixer.Sound('Sounds/coin.mp3')


game = Game()
game.crearNivel()

menu = game.menu
jugador=game.jugador



def main():

    movementAvailable=0
    run = True
    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.pause=not game.pause



       
        if keys[pygame.K_ESCAPE]:
            print("Juego terminado")
            run = False

        

#------------- inputs ----------------------------------------------------
        if not game.pause:   
            if menu.active:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                            if menu.arrowPosition == menu.textHeight*6:
                                menu.arrowPosition=0
                            else:
                                menu.arrowPosition+= menu.textHeight *2
                        if  ( event.key == pygame.K_UP or event.key == pygame.K_w):
                            if menu.arrowPosition == 0:
                                menu.arrowPosition = menu.textHeight * 6
                            else:
                                menu.arrowPosition-= menu.textHeight *2
                        if event.key == pygame.K_SPACE:
                            if jugador.gold >= 10:
                                if menu.arrowPosition ==0:
                                    jugador.health+=10
                                if menu.arrowPosition ==menu.textHeight *2:
                                    jugador.attack+=1
                                if menu.arrowPosition ==menu.textHeight *4:
                                    jugador.defense+=1
                                jugador.gold -= 10
                            if menu.arrowPosition ==menu.textHeight *6:
                                menu.active=False
                                menu.arrowPosition=0


            else:
                if movementAvailable==0:
                    movementAvailable=5
                    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                        # if jugador.facing == "left":
                        direction = "left"
                        dontMove=False
                        dontMove = cajaCollitions(direction)


                        if not dontMove:
                            dontMove= escaleraCollitions(direction)

                        if jugador.collides(game.gameObjects["tiendas"],direction):
                            dontMove=True
                            menu.active=True

                        if not dontMove:
                            dontMove = enemyCollitions(direction)
                        if not (jugador.position.x < tile_size or  jugador.collides(game.gameObjects["bloques"],direction) or jugador.collides(game.gameObjects["agujeros"],direction) or dontMove):
                            coinCollitions(direction)
                            jugador.move(direction)
                            caminarSound.play()
                        # else:
                        
                        jugador.facing=direction
                        
                    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                        # if jugador.facing=="right":
                        direction = "right"
                        dontMove=False
                        dontMove = cajaCollitions(direction)

                        if not dontMove:
                            dontMove= escaleraCollitions(direction)
                            

                        if jugador.collides(game.gameObjects["tiendas"],direction):
                            dontMove=True
                            menu.active=True

                        if not dontMove:
                            dontMove = enemyCollitions(direction)
                        if not (jugador.position.x + jugador.width + tile_size  > screenWidth  or  jugador.collides(game.gameObjects["bloques"],direction) or jugador.collides(game.gameObjects["agujeros"],direction)  or dontMove): 
                            coinCollitions(direction)
                            jugador.move(direction)
                            caminarSound.play()

                        # else:
                        jugador.facing=direction
                        
                    if (keys[pygame.K_UP] or keys[pygame.K_w]):
                        # if jugador.facing=="up":
                        direction = "up"
                        dontMove=False
                        dontMove = cajaCollitions(direction)

                        if not dontMove:
                            dontMove= escaleraCollitions(direction)

                        if jugador.collides(game.gameObjects["tiendas"],direction):
                            dontMove=True
                            menu.active=True

                        if not dontMove:
                            dontMove = enemyCollitions(direction)
                        if not (jugador.position.y - tile_size < jugador.offset  or  jugador.collides(game.gameObjects["bloques"],direction) or jugador.collides(game.gameObjects["agujeros"],direction)  or dontMove):
                            coinCollitions(direction)
                            jugador.move(direction)
                            caminarSound.play()
                        # else:
                        jugador.facing=direction
                        
                    if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                        # if jugador.facing=="down":
                        direction = "down"
                        dontMove=False
                        dontMove = cajaCollitions(direction)

                        if not dontMove:
                            dontMove= escaleraCollitions(direction)

                        if jugador.collides(game.gameObjects["tiendas"],direction):
                            dontMove=True
                            menu.active=True

                        if not dontMove:
                            dontMove = enemyCollitions(direction)
                        if not (jugador.position.y + tile_size >= screenHeight or  jugador.collides(game.gameObjects["bloques"],direction) or jugador.collides(game.gameObjects["agujeros"],direction)  or dontMove):
                            coinCollitions(direction)
                            jugador.move(direction)
                            caminarSound.play()
                        # else:
                        jugador.facing=direction
                else:
                    movementAvailable-=1
        

        if jugador.health<=0:
            updateWindow()
            deadText = font.render('You Dead ', 1 ,(0,0,0) , (255,255,255))
            WINDOW.blit(deadText,((screenWidth+300)/2 ,screenHeight/2 ))

            pygame.display.update()
            pygame.time.delay(3000)

            game.restart()
            actualizarJugador()
            
            
        updateWindow()

    pygame.quit()

def actualizarJugador():
    global jugador
    jugador=game.jugador


def cajaCollitions(direction):
    for i, caja in enumerate(game.gameObjects["cajas"]):
        if jugador.collides(caja,direction):
            
            for key in game.gameObjects:
                if key == "agujeros":
                    continue
                if caja.collides(game.gameObjects[key],direction):
                    return True

            if  (caja.position.x + caja.width + tile_size  > screenWidth  and direction =="right"  ):
                return True
            if  (caja.position.y - tile_size < jugador.offset  and direction =="up"   ):
                return True
            if  (caja.position.y + tile_size >= screenHeight and direction =="down"   ):
                return True
            if  ( caja.position.x < tile_size and direction =="left"  ):
                return True

            else:
                cords=caja.cords
                x= int(cords.x)
                y= int(cords.y)
                game.niveles[game.nivel][y][x]=0

                if direction == "left":
                    x-=1
                if direction == "right":
                    x+=1
                if direction == "up":
                    y-=1
                if direction == "down":
                    y+=1

                if caja.collides(game.gameObjects["agujeros"],direction):
                    game.gameObjects["cajas"].pop(i)
                    game.niveles[game.nivel][y][x]=0
                    for i, agujero in enumerate(game.gameObjects["agujeros"]):
                        if agujero.cords == Vector2(x,y):
                            game.gameObjects["agujeros"].pop(i)
                            break
                else:
                    game.niveles[game.nivel][y][x]=3
                    caja.move(direction)

def escaleraCollitions(direction):
    for escalera in game.gameObjects["escaleras"]:
        if escalera is not None and jugador.collides(escalera,direction):
            cords=jugador.cords
            x= int(cords.x)
            y= int(cords.y)
            for i in range(tile_quantity):
                for j in range(tile_quantity):
                    if game.niveles[game.nivel][j][i]==1:
                        game.niveles[game.nivel][j][i]=0
            if escalera.direction == "up":
                game.niveles[game.nivel+1][y][x]=1
                game.subir()
                actualizarJugador()

                deadText = font.render('Subiendo ', 1 ,(0,0,0) , (200,200,200))
                WINDOW.blit(deadText,((screenWidth+300)/2 ,screenHeight/2 ))

                pygame.display.update()
                pygame.time.delay(1000)
                return True
            else:
                game.niveles[game.nivel-1][y][x]=1
                game.bajar()
                actualizarJugador()

                deadText = font.render('Bajando ', 1 ,(0,0,0) , (200,200,200))
                WINDOW.blit(deadText,((screenWidth+300)/2 ,screenHeight/2 ))
                
                pygame.display.update()
                pygame.time.delay(1000)
                return True
    return False
def coinCollitions(direction):
    for i in range(len(game.gameObjects["coins"])):
        if jugador.collides(game.gameObjects["coins"][i],direction):
            cords=game.gameObjects["coins"][i].cords
            x= int(cords.x)
            y= int(cords.y)
            game.niveles[game.nivel][y][x]=0
            game.gameObjects["coins"].pop(i)
            coinSound.play()
            jugador.gold += 1
            return True
    return False
def enemyCollitions(direction):
    for i in range(len(game.gameObjects["enemigos"])):
        if jugador.collides(game.gameObjects["enemigos"][i],direction):
            jugador.health-= game.gameObjects["enemigos"][i].attack - jugador.defense
            game.gameObjects["enemigos"][i].health-= jugador.attack - game.gameObjects["enemigos"][i].defense
            if game.gameObjects["enemigos"][i].health <=0:
                cords=game.gameObjects["enemigos"][i].cords
                x= int(cords.x)
                y= int(cords.y)
                game.niveles[game.nivel][y][x]=0
                jugador.gold+= game.gameObjects["enemigos"][i].gold
                game.gameObjects["enemigos"].pop(i)
            return True
    return False
def updateWindow():
    WINDOW.fill((0,0,0))
    WINDOW.blit(SCREEN,(200,0))
    SCREEN.fill((100,0,100))

    if not game.pause:
        
        
        for i in range(1,tile_quantity):
            pygame.draw.line(SCREEN,(0,0,0),(0,i*50),(screenWidth,i*50))
            pygame.draw.line(SCREEN,(0,0,0),(i*50,0),(i*50,screenHeight))

        for key in game.gameObjects:
            for objeto in game.gameObjects[key]:
                try:
                    objeto.draw(SCREEN)
                except:
                    pass

        if menu.active:
            menu.draw(SCREEN)
        
        jugador.draw(SCREEN)
    else:
        pauseText = font.render('Pause ', 1 , (255,255,255))
        
        SCREEN.blit(pauseText,(screenWidth/2 - 20,screenHeight/2 - 20))

# Textos en el costado
    goldText = font.render('Gold: ' + str(jugador.gold) , 1 , (255,255,255))
    healthText = font.render('Hp: ' + str(jugador.health) , 1 , (255,255,255))
    attackText = font.render('Att: ' + str(jugador.attack) , 1 , (255,255,255))
    defenseText = font.render('Def: ' + str(jugador.defense) , 1 , (255,255,255))
    WINDOW.blit(goldText,(10,10))
    WINDOW.blit(healthText,(10,50))
    WINDOW.blit(attackText,(10,90))
    WINDOW.blit(defenseText,(10,130))


    pygame.display.update()
if __name__ == "__main__":
    main()


