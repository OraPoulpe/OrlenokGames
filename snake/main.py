import os
import pygame
import random
import pygame_menu

W, H = 800, 600
FPS = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ROCKS = 10
ROCKS_LIST=[]

x0, y0 = W//2, H//2
x0_change, y0_change = 0, 0
snake_block = 20

def message(msg, color):
    msg = font_style.render(msg, True, color)
    screen.blit(msg, (W//2 - msg.get_width()//2, H//2 - msg.get_height()//2))

def draw_score(score):
    score = font_style.render(str(score), True, BLACK)
    screen.blit(score, (0, 0))

def draw_sound(has_sound):
    sound = pygame.image.load('./assets/sound.svg')
    nosound = pygame.image.load('./assets/nosound.svg')
    if has_sound:
        screen.blit(sound, (W-30, 5))
    else:
        screen.blit(nosound, (W-30, 5))

def draw_snake(snake_list, color):
    for el in snake_list:
        pygame.draw.rect(screen, color, (el[0], el[1], snake_block, snake_block))

def generate_food():
    x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block

    while (x,y) in ROCKS_LIST:
        x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
        y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block

    return x, y

def generate_rock():
    x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block

    return x, y

def generate_rocks():
    for _ in range(ROCKS):
        coords = generate_rock()
        ROCKS_LIST.append((coords[0], coords[1]))

def get_all_sounds():
    path = r'./sounds'
 
    for _, _, files in os.walk(path):
        return files

if __name__ == "__main__":
    color = None
    pygame.init()
    pygame.mixer.music.load(f'./sounds/{get_all_sounds()[0]}')

    def start_the_game():
        global color
        menu.disable()
        pygame.mixer.music.play(-1)
        if color == None:
            color = RED

    def set_music(name, value):
        pygame.mixer.music.load(f'./sounds/{value}')

    def choose_color(_color):
        global color

        if _color != (-1, -1, -1):
            color = _color

    generate_rocks()

    running = True
    pause = False
    game_over = False
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Игра Змейка")
    clock = pygame.time.Clock()
    font_style = pygame.font.SysFont(None, 50)
    x_prev=0
    y_prev=0

    menu = pygame_menu.Menu('Добро пожаловать!', 600, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.selector('Музыка: ', list(map(lambda x: (x.split('.')[0], x), get_all_sounds())), onchange=set_music)
    menu.add.color_input('Цвет змейки', color_type='hex', default='ff0000', onchange=choose_color)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(screen)

    foodx, foody = generate_food()

    snake_list = []
    length_snake = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                    if not game_over:
                        if event.key == pygame.K_LEFT:
                            x0_change = -snake_block
                            y0_change = 0
                        elif event.key == pygame.K_RIGHT:
                            x0_change = snake_block
                            y0_change = 0
                        elif event.key == pygame.K_UP:
                            x0_change = 0
                            y0_change = -snake_block
                        elif event.key == pygame.K_DOWN:
                            x0_change = 0
                            y0_change = snake_block
                        elif event.key == pygame.K_SPACE:
                            pause = not pause
                            if (pause):
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()
                        elif event.key == pygame.K_m:
                            if pygame.mixer.music.get_volume() == 0:
                                pygame.mixer.music.set_volume(1)
                            else:
                                pygame.mixer.music.set_volume(0)
                    else:
                        if event.key == pygame.K_c:
                            pygame.mixer.music.play(-1)
                            x0, y0 = W//2, H//2
                            x0_change, y0_change = 0, 0
                            snake_list=[(x0, y0)]
                            length_snake=1
                            game_over=False
                            foodx, foody = generate_food()
                            ROCKS_LIST=[]
                            generate_rocks()

        if not game_over and not pause:
            if length_snake > 1:
                if (x0+x0_change, y0+y0_change) not in snake_list:
                    x0 += x0_change
                    y0 += y0_change
                    x_prev=x0_change
                    y_prev=y0_change
                else:
                    x0+=x_prev
                    y0+=y_prev
            else:
                x0 += x0_change
                y0 += y0_change
            snake_list.append((x0, y0))

            if len(snake_list) > length_snake:
                snake_list.pop(0)


        for el in snake_list[:-1]:
            if el == snake_list[-1]:
                game_over = True

        if x0 >= W or x0 <= 1 or y0 >= H or y0 <= 1:
            game_over = True

        if (x0, y0) in ROCKS_LIST:
            game_over = True 

        screen.fill(WHITE)

        if game_over:
            message("Вы проиграли", GREEN)
            pygame.mixer.music.stop()
            
        if pause:
            message("Пауза", GREEN)

        draw_score(len(snake_list))
        draw_sound(pygame.mixer.music.get_volume() != 0)
        # pygame.draw.rect(screen, RED, [x0, y0, snake_block, snake_block])
        draw_snake(snake_list, color)
        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])
        for rock in ROCKS_LIST:
            pygame.draw.rect(screen, BLACK, [rock[0], rock[1], snake_block, snake_block])

        pygame.display.update()


        if (x0, y0) == (foodx, foody):
            foodx, foody = generate_food()
            length_snake += 1

        clock.tick(FPS)


    pygame.quit()
    quit()
