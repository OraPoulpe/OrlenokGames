def mmenu():
    import pygame
    import pygame_menu
    from Snake.main import snake
    from Tetris.main import tetris
    from Game2D.main import platform
    from PingPong.main import pingpong
    from Arcanoid.main import arcanoid
    from FlappyBird.main import bird

    W, H = 600, 500

    print(__name__)


    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Сборник Игр")

    menu = pygame_menu.Menu('Добро пожаловать!', W, H,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Змейка', snake)
    menu.add.button('Тетрис', tetris)
    menu.add.button('Пинг-Понг', pingpong)
    menu.add.button('Арканоид', arcanoid)
    menu.add.button('Платформер', platform)
    menu.add.button('Летающая птица', bird)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(screen)


mmenu()
