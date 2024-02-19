import random

import pygame as pg

WSIZE = (720, 480)

screen = pg.display.set_mode(WSIZE)

TSIDE = 30
MSIZE = WSIZE[0] // TSIDE, WSIZE[1] // TSIDE

start_pos = MSIZE[0] // 2, MSIZE[1] // 2
snake = [start_pos]
alive = True

direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

apple = random.randint(0, MSIZE[0]-1), random.randint(0, MSIZE[1]-1)

fps = 5
clock = pg.time.Clock()

pg.font.init()
font_score = pg.font.SysFont("Arial", 25)
font_gameover = pg.font.SysFont("Arial", 45)
font_space = pg.font.SysFont("Arial", 18)

running = True
while running:
    clock.tick(fps)
    screen.fill("black")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if alive:
                if event.key == pg.K_RIGHT and direction != 2:
                    direction = 0
                if event.key == pg.K_DOWN and direction != 3:
                    direction = 1
                if event.key == pg.K_LEFT and direction != 0:
                    direction = 2
                if event.key == pg.K_UP and direction != 1:
                    direction = 3
            else:
                if event.key == pg.K_SPACE:
                    alive = True
                    snake = [start_pos]
                    apple = random.randint(0, MSIZE[0]-1), random.randint(0, MSIZE[1]-1)
                    fps = 5

    [pg.draw.rect(screen, "green", (x * TSIDE, y * TSIDE, TSIDE - 1, TSIDE - 1)) for x, y in snake]
    pg.draw.rect(screen, "red", (apple[0] * TSIDE, apple[1] * TSIDE, TSIDE - 1, TSIDE - 1))

    if alive:
        new_pos = snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][1]
        if not (0 <= new_pos[0] < MSIZE[0] and 0 <= new_pos[1] < MSIZE[1]) or \
                new_pos in snake:
            alive = False
        else:
            snake.insert(0, new_pos)
            if new_pos == apple:
                fps += 1
                apple = random.randint(0, MSIZE[0]-1), random.randint(0, MSIZE[1]-1)
            else:
                snake.pop(-1)
    else:
        text = font_gameover.render(f"GAME OVER", True, "white")
        screen.blit(text, (WSIZE[0] // 2 - text.get_width()//2, WSIZE[1] // 2 - 50))
        text = font_space.render(f"Press SPACE for restart", True, "white")
        screen.blit(text, (WSIZE[0] // 2 - text.get_width() // 2, WSIZE[1] // 2 + 10))
    screen.blit(font_score.render(f"Score: {len(snake)}", True, "yellow"), (5, 5))

    pg.display.flip()
