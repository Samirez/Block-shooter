import pygame as pg
import random


pg.init()
# set dimensions
height = 500
width = 600
# variable for screen size
screen = pg.display.set_mode((height, width))
background = pg.image.load("space.jpg").convert()
font = "led.ttf"
FONT = pg.font.SysFont("Sans", 20)
TEXT_COLOR = (0, 0, 0)
highscore = 0


def run_game():
    global highscore
    # game title
    pg.display.set_caption("rain drops")
    start_time = pg.time.get_ticks()
    ship = pg.image.load("rocket.png").convert_alpha()
    square = pg.Surface((28, 28))
    square.fill((255, 0, 0))
    square.blit(ship, (0, 0))
    player_box = square.get_rect()
    player_box.center = (300, 400)
    drop = pg.image.load("drop.png").convert_alpha()
    enemy = pg.Surface((38, 44))
    enemy.fill((0, 0, 255))
    enemy.blit(drop, (0, 0))
    spawn_rate = 30
    enemies = []
    bullets = []
    bulletIcon = pg.image.load("bullet.png").convert_alpha()
    shot = pg.mixer.Sound("shot.wav")
    clock = pg.time.Clock()
    press = pg.event.get
    w = 100
    h = 100
    left = 0
    right = 0
    up = 0
    down = 0
# directions of player movement
    while True:
        if left:
            w += 2
        elif right:
            w -= 2
        elif up:
            h -= 2
        elif down:
            h += 2
        screen.blit(background, (0, 0))

        def player():
            screen.blit(square, (w, h))
        player()
        if press(pg.QUIT):
            break
        # Actions when pressing down keys
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    right = 0
                    left = 1
                if event.key == pg.K_LEFT:
                    left = 0
                    right = 1
                if event.key == pg.K_UP:
                    up = 1
                    down = 0
                if event.key == pg.K_DOWN:
                    down = 1
                    up = 0
                if event.type == pg.K_SPACE:
                    shot.play()
                    bullets.append([event.pos[0], 500])
            if event.type == pg.KEYUP:
                down = 0
                up = 0
                left = 0
                right = 0
        # bullet direction
        for b in range(len(bullets)):
            bullets[b][0] -= 10
        # bullet remove when out of bounds
        for bullet in bullets[:]:
            if bullet[0] < 0:
                bullets.remove(bullet)
        # spawn rate
        spawn_rate -= 1
        if spawn_rate <= 0:
            # Append an enemy rect
            enemies.append(enemy.get_rect(topleft=(random.randrange(600), 0)))
            spawn_rate = 30
        player_box.x = w
        player_box.y = h
        for enemy_rect in enemies:
            enemy_rect.y += 5
            # Collision detection with player
            if player_box.colliderect(enemy_rect):
                print('Game over')
                return main_menu()
        for enemy_rect in enemies:
            screen.blit(enemy, enemy_rect)
        if start_time:
            time_since_enter = pg.time.get_ticks() - start_time
            if time_since_enter > highscore:
                highscore = time_since_enter
            message = str(time_since_enter) + 'Milliseconds'
            font1 = pg.font.SysFont('led.ttf', 20)
            score = font1.render("Highscore:" + str(highscore), True, (0, 0, 0))
            scoreRect = score.get_rect()
            # setting center for the first text
            scoreRect.center = (250, 35)
            screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
            # adding bullet to game screen
            for bullet in bullets:
                screen.blit(bulletIcon, pg.Rect(bullet[0], bullet[1], 0, 0))
            # display score on screen
            screen.blit(score, scoreRect)
        clock.tick(60)
        pg.display.flip()
    pg.quit()


def text_format(message, textFont, textSize, textColor):
    newFont = pg.font.Font(textFont, textSize)
    newText = newFont.render(message, True, textColor)
    return newText


# menu selection function
def main_menu():
    menu = True
    selected = "start"
    while menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = "start"
                elif event.key == pg.K_DOWN:
                    selected = "quit"
                if event.key == pg.K_RETURN:
                    if selected == "start":
                        print("Start")
                        run_game()
                    if selected == "quit":
                        pg.quit()
                        quit()
        screen.fill("brown")
        title = text_format("Rain drops", font, 90, "yellow")
        if selected == "start":
            text_start = text_format("START", font, 75, "white")
        else:
            text_start = text_format("START", font, 75, "black")
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, "white")
        else:
            text_quit = text_format("QUIT", font, 75, "black")

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (width / 2 - (quit_rect[2] / 2), 360))
        pg.display.update()
        pg.time.Clock().tick(60)
        pg.display.set_caption("Python - Pygame Rain drops menu selection")


main_menu()
