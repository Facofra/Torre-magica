import pygame
from classes import Vector2, screenWidth, screenHeight, tile_size, tile_quantity, Jugador, Block, Caja, Coin, Game, Enemigo


pygame.init()

# SETTING
WINDOW = pygame.display.set_mode((screenWidth+200,screenHeight))
SCREEN = pygame.Surface([screenWidth,screenHeight])
pygame.display.set_caption("Test game")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont('papyrus',20,True)


# SONIDOS
cristalSound = pygame.mixer.Sound('Sounds/cristal.mp3')
cristalSound.set_volume(0.09)
caminarSound = pygame.mixer.Sound('Sounds/caminar.mp3')
coinSound = pygame.mixer.Sound('Sounds/coin.mp3')


jugador = Jugador(1,1)
game = Game()

bloques =[]
cajas =[]
coins= []
enemigos = []

mapa = [
    [0,0,0,0,0,0,0,0,0,0,0,4],
    [4,0,0,0,2,2,2,0,0,0,0,0],
    [4,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,4,0,4],
    [4,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,5,0,0,0,0],
    [0,0,0,2,0,0,0,0,3,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,0,4,0,0,0],
    [0,0,0,0,3,0,0,0,0,0,0,5]
]

for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        if mapa[i][j] == 2:
            x=j
            y=i
            bloques.append(Block(x,y))
        elif mapa[i][j] == 3:
            x=j
            y=i
            cajas.append(Caja(x,y))
        elif mapa[i][j] == 4:
            x=j
            y=i
            coins.append(Coin(x,y))
        elif mapa[i][j] == 5:
            x=j
            y=i
            enemigos.append(Enemigo(x,y))
        



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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                x=posicion[0]-200
                y=posicion[1]
                x= int(x/tile_size)
                y= int(y/tile_size)
                
                if event.button ==1:
                    bloques.append(Block(x,y)) 
                elif event.button==3:
                    for i in range(len(bloques)):
                        if bloques[i].cords == Vector2(x,y):
                            cristalSound.play()
                            bloques.pop(i)
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.pause=not game.pause



       
        if keys[pygame.K_ESCAPE]:
            print("Juego terminado")
            run = False
        
        # if keys[pygame.K_RETURN]:
        #     game.pause= not game.pause

        

#------------- inputs ----------------------------------------------------
        if not game.pause:   
            if movementAvailable==0:
                movementAvailable=5
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                    # if jugador.facing == "left":
                    direction = "left"
                    dontMove=False
                    for caja in cajas:
                        if jugador.collides(caja,direction):
                            if  ( caja.collides([bloques,cajas,coins,enemigos],direction) or caja.position.x < tile_size ):
                                dontMove = True
                            else:
                                caja.move(direction)
                    if not dontMove:
                        dontMove = enemyCollitions(direction)
                    if not (jugador.position.x < tile_size or  jugador.collides(bloques,direction) or dontMove):
                        coinCollitions(direction)
                        jugador.move(direction)
                        caminarSound.play()
                    # else:
                    
                    jugador.facing=direction
                    
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                    # if jugador.facing=="right":
                    direction = "right"
                    dontMove=False
                    for caja in cajas:
                        if jugador.collides(caja,direction):
                            if  (caja.position.x + caja.width + tile_size  > screenWidth  or caja.collides([bloques,cajas,coins,enemigos],direction) ):
                                dontMove=True
                            else:
                                caja.move(direction)
                    if not dontMove:
                        dontMove = enemyCollitions(direction)
                    if not (jugador.position.x + jugador.width + tile_size  > screenWidth  or  jugador.collides(bloques,direction)  or dontMove): 
                        coinCollitions(direction)
                        jugador.move(direction)
                        caminarSound.play()

                    # else:
                    jugador.facing=direction
                    
                if (keys[pygame.K_UP] or keys[pygame.K_w]):
                    # if jugador.facing=="up":
                    direction = "up"
                    dontMove=False
                    for caja in cajas:
                        if jugador.collides(caja,direction):
                            if  (caja.position.y - tile_size < jugador.offset  or  caja.collides([bloques,cajas,coins,enemigos],direction) ):
                                dontMove=True
                            else:
                                caja.move(direction)
                    if not dontMove:
                        dontMove = enemyCollitions(direction)
                    if not (jugador.position.y - tile_size < jugador.offset  or  jugador.collides(bloques,direction)  or dontMove):
                        coinCollitions(direction)
                        jugador.move(direction)
                        caminarSound.play()
                    # else:
                    jugador.facing=direction
                    
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                    # if jugador.facing=="down":
                    direction = "down"
                    dontMove=False

                    for caja in cajas:
                        if jugador.collides(caja,direction):
                            if  (caja.position.y + tile_size >= screenHeight or  caja.collides([bloques,cajas,coins,enemigos],direction) ):
                                dontMove=True
                            else:
                                caja.move(direction)

                    if not dontMove:
                        dontMove = enemyCollitions(direction)
                    if not (jugador.position.y + tile_size >= screenHeight or  jugador.collides(bloques,direction)  or dontMove):
                        coinCollitions(direction)
                        jugador.move(direction)
                        caminarSound.play()
                    # else:
                    jugador.facing=direction
            else:
                movementAvailable-=1
        

        
        updateWindow()

    pygame.quit()


def coinCollitions(direction):
    for i in range(len(coins)):
        if jugador.collides(coins[i],direction):
            coins.pop(i)
            coinSound.play()
            jugador.gold += 1
            return True
    return False
def enemyCollitions(direction):
    for i in range(len(enemigos)):
        if jugador.collides(enemigos[i],direction):
            jugador.health-= enemigos[i].attack - jugador.defense
            enemigos[i].health-= jugador.attack - enemigos[i].defense
            if enemigos[i].health <=0:
                jugador.gold+= enemigos[i].gold
                enemigos.pop(i)
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

        for block in bloques:
            block.draw(SCREEN)
        for caja in cajas:
            caja.draw(SCREEN)
        for coin in coins:
            coin.draw(SCREEN)
        for enemigo in enemigos:
            enemigo.draw(SCREEN)

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


