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
littleFont = pygame.font.SysFont('papyrus',12,True)


# SONIDOS
caminarSound = pygame.mixer.Sound('Sounds/caminar.mp3')
coinSound = pygame.mixer.Sound('Sounds/coin.mp3')
golpeSound = pygame.mixer.Sound('Sounds/golpe.mp3')
deadEnemySound = pygame.mixer.Sound('Sounds/deadEnemy.mp3')




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
                if event.key == pygame.K_RETURN and not menu.active:
                    game.pause.isPaused = not game.pause.isPaused



       
        if keys[pygame.K_ESCAPE]:
            print("Juego terminado")
            run = False

        

#------------- inputs ----------------------------------------------------
        if not game.pause.isPaused:   
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
                                    jugador.health+=20
                                    jugador.gold -= 10
                                if menu.arrowPosition ==menu.textHeight *2:
                                    jugador.attack+=1
                                    jugador.gold -= 10
                                if menu.arrowPosition ==menu.textHeight *4:
                                    jugador.defense+=1
                                    jugador.gold -= 10
                            if menu.arrowPosition ==menu.textHeight *6:
                                menu.active=False
                                menu.arrowPosition=0


            else:
                if movementAvailable==0:
                    movementAvailable=5
                    moving = False

                    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                        direction = "left"
                        moveAndCollitions(direction)
                        moving=True
                        
                    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                        direction = "right"
                        moveAndCollitions(direction)
                        moving=True
                        
                    if (keys[pygame.K_UP] or keys[pygame.K_w]):
                        direction = "up"
                        moveAndCollitions(direction)
                        moving=True
                        
                        
                    if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                        direction = "down"
                        moveAndCollitions(direction)
                        moving=True
                    if not moving:
                        jugador.moving=0
                        
                        
                else:
                    movementAvailable-=1
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        if game.pause.arrowPosition == 3:
                            game.pause.arrowPosition=0
                        else:
                            game.pause.arrowPosition+=1
                    if  ( event.key == pygame.K_UP or event.key == pygame.K_w):
                        if game.pause.arrowPosition == 0:
                            game.pause.arrowPosition = 3
                        else:
                            game.pause.arrowPosition-= 1
                    if event.key == pygame.K_SPACE:
                        if game.pause.arrowPosition == 0:
                            # continue
                            game.pause.isPaused = False
                        if game.pause.arrowPosition == 1:
                            # reset level
                            game.resetLevel()
                            game.pause.isPaused = False
                            
                        if game.pause.arrowPosition == 2:
                            # restart game
                            game.restart()
                            actualizarJugador()
                            game.pause.isPaused = False
                        if game.pause.arrowPosition == 3:
                            # exit
                            run = False
                            

        if jugador.health<=0:
            jugador.health=0
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
def moveAndCollitions(direction):
    global jugador
    dontMove=False
    dontMove = cajaCollitions(direction)


    if not dontMove:
        dontMove= escaleraCollitions(direction)

    if jugador.collides(game.gameObjects["tiendas"],direction):
        dontMove=True
        menu.active=True

    if not dontMove:
        dontMove = enemyCollitions(direction)

    # collide with walls
    if (jugador.position.x < tile_size and direction=="left") or (jugador.position.x + jugador.width + tile_size  > screenWidth and direction=="right") or (jugador.position.y - tile_size < jugador.offset and direction=="up")  or (jugador.position.y + tile_size >= screenHeight and direction== "down"):
        dontMove=True

    if not (jugador.collides(game.gameObjects["bloques"],direction) or jugador.collides(game.gameObjects["agujeros"],direction) or dontMove):
        
        coinCollitions(direction)
        jugador.move(direction)
        caminarSound.play()
        if jugador.moving == 0 or jugador.moving== 2:
            jugador.moving=1
        else:
            jugador.moving = 2

    
    
    jugador.facing=direction

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
            golpeSound.play()
            jugador.health-= game.gameObjects["enemigos"][i].attack - jugador.defense
            game.gameObjects["enemigos"][i].health-= jugador.attack - game.gameObjects["enemigos"][i].defense
            if game.gameObjects["enemigos"][i].health <=0:

                if(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo0'>" ):
                    game.killedEnemies[0] = game.gameObjects["enemigos"][i]
                elif(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo1'>" ):
                    game.killedEnemies[1] = game.gameObjects["enemigos"][i]
                elif(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo2'>" ):
                    game.killedEnemies[2] = game.gameObjects["enemigos"][i]
                elif(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo3'>" ):
                    game.killedEnemies[3] = game.gameObjects["enemigos"][i]
                elif(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo4'>" ):
                    game.killedEnemies[4] = game.gameObjects["enemigos"][i]
                elif(str(type(game.gameObjects["enemigos"][i])) == "<class 'classes.Enemigo5'>" ):
                    game.killedEnemies[5] = game.gameObjects["enemigos"][i]
                    

                cords=game.gameObjects["enemigos"][i].cords
                x= int(cords.x)
                y= int(cords.y)
                game.niveles[game.nivel][y][x]=0
                jugador.gold+= game.gameObjects["enemigos"][i].gold
                game.gameObjects["enemigos"].pop(i)
                deadEnemySound.play()
            return True
    return False
def updateWindow():
    WINDOW.fill(( 172, 78, 0 ))
    WINDOW.blit(SCREEN,(200,0))
    SCREEN.blit(game.bg,(0,0))


    for i in range(len(game.killedEnemies)):
        if game.killedEnemies[i] is not None:
            enemy = game.killedEnemies[i]
            WINDOW.blit(enemy.sprite,(0,225 + i*40 ))
            # damage = (enemy.attack - jugador.defense) * ( enemy.hp // (jugador.attack - enemy.defense) + enemy.hp % (jugador.attack - enemy.defense > 0)  )
            # damage = damage * (damage > 0)
            # statsText = littleFont.render( 'Dmg: '+str(damage) + '  G: ' + str(enemy.gold) , 1 , (255,255,255))
            statsText = littleFont.render('    ' + str(enemy.hp) + '       ' + str(enemy.attack) + '         ' + str(enemy.defense) + '        ' + str(enemy.gold) , 1 , (255,255,255))
            WINDOW.blit(statsText,(40,225 + i*42 ))

            heart = pygame.transform.scale(game.heart,(17,17))
            WINDOW.blit(heart,(35,225+ i*42))

            sword = pygame.transform.scale(game.sword,(17,17))
            WINDOW.blit(sword,(75,225+ i*42))

            shield = pygame.transform.scale(game.shield,(17,17))
            WINDOW.blit(shield,(115,225+ i*42))

            gold = pygame.transform.scale(game.gold,(17,17))
            WINDOW.blit(gold,(155,225+ i*42))


    if not game.pause.isPaused:
        
        
        # for i in range(1,tile_quantity):
        #     pygame.draw.line(SCREEN,(0,0,0),(0,i*50),(screenWidth,i*50))
        #     pygame.draw.line(SCREEN,(0,0,0),(i*50,0),(i*50,screenHeight))

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
        game.pause.draw(SCREEN)

# Textos en el costado
    goldText = font.render('        ' + str(jugador.gold) , 1 , (255,255,255))
    healthText = font.render('       ' + str(jugador.health) , 1 , (255,255,255))
    attackText = font.render('       ' + str(jugador.attack) , 1 , (255,255,255))
    defenseText = font.render('      ' + str(jugador.defense) , 1 , (255,255,255))

    WINDOW.blit(game.gold,(10,10))
    WINDOW.blit(game.heart,(10,50))
    WINDOW.blit(game.sword,(10,90))
    WINDOW.blit(game.shield,(10,130))

    


    WINDOW.blit(goldText,(10,10))
    WINDOW.blit(healthText,(10,50))
    WINDOW.blit(attackText,(10,90))
    WINDOW.blit(defenseText,(10,130))


    pygame.display.update()
if __name__ == "__main__":
    main()


