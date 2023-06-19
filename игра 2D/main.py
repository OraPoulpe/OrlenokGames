import pygame                                      #-Импортируем игру

image_path = '/data/data/ghost hunting.myapp/files/app/'

clock = pygame.time.Clock()                        # - создание переменной clock для замедления времени или ускорения

pygame.init()                                      #- Инитируем игру
screen = pygame.display.set_mode(( 618, 359))      # - Если не надо кнопки на экране при запуске то нужно добавить Flags=pygame,NOFRAME)# - Переманная экран
pygame.display.set_caption("ItPtogerGame")         # - Название проекта
icon = pygame.image.load( 'images/game_icon.png').convert_alpha()   # - Команда для создания иконки игры указывая картинку на картинку из определенной папки
pygame.display.set_icon(icon)                      # - указываем дисплею нашу иконку

bg = pygame.image.load('images/bg.png').convert_alpha()  # - установление фона
walk_left = [ # - анимация влево через картинки
    pygame.image.load('images/player_left/left1.png').convert_alpha(),
    pygame.image.load('images/player_left/left2.png').convert_alpha(),
    pygame.image.load('images/player_left/left3.png').convert_alpha(),
    pygame.image.load('images/player_left/left4.png').convert_alpha(),
]

walk_right = [ # - анимация вправо  через картинки                                                
    pygame.image.load('images/player_right/right1.png').convert_alpha(),
    pygame.image.load('images/player_right/right2.png').convert_alpha(),
    pygame.image.load('images/player_right/right3.png').convert_alpha(),
    pygame.image.load('images/player_right/right4.png').convert_alpha(),
]

ghost = pygame.image.load('images/ghost.png').convert_alpha() # - подключение картинки приведения к коду .convert_alpha() - для того чтобы конвертировать картинки

ghost = pygame.transform.scale( ghost, (ghost.get_width() // 16, ghost.get_height() // 16)) # - размеры приведения

ghost_list_in_game = []

player_anim_count = 0                              # - счетчик анимаций персонажа
bg_x = 0                                           # - координаты фона

player_speed = 5                                   # - скорость персонажа
player_x = 150                                     # - координаты x персонажа
player_y = 250                                     # - координаты Y персонажа

is_jump = False                                    # - переменная для прыжка
jump_count =  8                                    # - сила отталкивания прыжка персонажа

bg_sound = pygame.mixer.Sound('sounds/bg.mp3')     # - музыка на фоне  то есть при включении игры музыка сразу же включается
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)           # - количество секунд между поевлением след. приведения

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (154, 160, 166))
restart_label = label.render('Начать заново', False, (41, 255, 105  ))
restart_label_rect =  restart_label.get_rect(topleft=(180, 200))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = [ ]

bullet = pygame.transform.scale( bullet, (bullet.get_width() // 16, bullet.get_height() // 16)) # - размеры патрона

gameplay = True

running = True                                     # - Команда при запуске
while running:                                     # - Типо когда при запуске и мы хотим отключить программу 

    screen.blit(bg, (bg_x, 0))                     # - координаты изображения
    screen.blit(bg, (bg_x + 618, 0))               # - координаты фона при изменении координатов персонажа  - действие фона

    if gameplay:        
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y)) # - отслеживание прикосновений то есть  создание квадрата возле перснонажа и врага
        
        if ghost_list_in_game:
            for (i, el)  in enumerate  (ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
        
        keys = pygame.key.get_pressed() # - переменная через кнопки которые мы будем анжимать чтобы двигаться
        if keys [pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y)) # - анимация влево
        else:
            screen.blit(walk_right[player_anim_count], (player_x , player_y)) # - анимация вправо


        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 250:                         # - границы персонажа чтобы не выходил за фон
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:                   # - прыжок на пробел
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:                                  # - чтобы прыжок был не таким высоким и чтобы не таким низким и чтобы координаты y персонажа не изменяли при опускании на землю
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8                         # - высота прыжка

        if player_anim_count == 3:
            player_anim_count = 0                      # - повторение анимаций персонажа
        else:
            player_anim_count +=1

        bg_x -= 2
        if bg_x == -618:                               # - если фон заканчивается чтобы начинался новый
            bg_x = 0    

        if bullets:                             
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))       
                el.x += 4 

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in  enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((24, 25, 26))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label,restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse)  and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
        
    pygame.display.update()                        # - Загрузка дисплея, Обновления которые мы показываем пользователю

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                        # - Эти 4 строчки значят конец программы
            pygame.quit()
        if event.type == ghost_timer: 
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))             # - отслеживание нажатия стрельбы 
            bullets_left -=1
    
    clock.tick(10)                                 # - время замедления анимаций 
        
          

