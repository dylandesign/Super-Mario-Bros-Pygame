import pygame
from sys import exit


def player_animation():
    global player_surf, player_index, player_speed, player_direction
    if player_rect.bottom < ground_rect.top:
        player_surf = player_jump
        player_surf = pygame.transform.scale(player_surf, (sprite_size, sprite_size))
        if player_direction == 1:
            player_surf = pygame.transform.flip(player_surf, True, False)
    elif player_speed > 0:
        player_index += 0.2
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]
        player_surf = pygame.transform.scale(player_surf, (sprite_size, sprite_size))
        player_direction = 0
    elif player_speed < 0:
        player_index += 0.2
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
        player_surf = pygame.transform.scale(player_surf, (sprite_size, sprite_size))
        player_surf = pygame.transform.flip(player_surf, True, False)
        player_direction = 1
    else:
        player_surf = player_stand
        player_surf = pygame.transform.scale(player_surf, (sprite_size, sprite_size))
        if player_direction == 1:
            player_surf = pygame.transform.flip(player_surf, True, False)

pygame.init()

# Native Original NES Resolution for context
nes_wResolution = 256
nes_hResolution = 240

# Wide Screen Super Mario Bros. current implementation.
wScreen = 1280
# hScreen will always be a multiple of the native nes_hResolution for consistency
hScreen = nes_hResolution*3

sprite_size = hScreen/15

wGrid = wScreen/sprite_size
hGrid = hScreen/sprite_size

print(wGrid)
print(hGrid)

# Canvas to draw on passing in as parameters of screen resolution
screen = pygame.display.set_mode((wScreen, hScreen))
# Sets Window Caption
pygame.display.set_caption('Super Mario Bros. Alpha 0.1')
# Variable for Clock in order to have the game run
clock = pygame.time.Clock()

# Parameters of Font Location and Font Size
test_font = pygame.font.Font('Font/NES.otf', 50)
bg_music = pygame.mixer.Sound('Audio/overworld_theme.ogg')
bg_music.play(loops = -1)

jump_sound = pygame.mixer.Sound('Audio/small_jump.ogg')
jump_sound.set_volume(0.5)

# Drawing Sky on Canvas
sky_surface = pygame.image.load('Graphics/background.png').convert()
sky_surface = pygame.transform.scale(sky_surface, (wScreen, hScreen))

# It's a-me Mario!
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_walk_1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
player_walk_3 = pygame.image.load('Graphics/Player/player_walk_slide.png').convert_alpha()
player_jump = pygame.image.load('Graphics/Player/player_jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_direction = 0
player_surf = player_stand
player_surf = pygame.transform.scale(player_surf, (sprite_size, sprite_size))
player_rect = player_surf.get_rect(bottomleft=(96, 624))
player_gravity = 0
player_speed = 0

# Title Screen Logo
# TODO implement sizing to match resolution and have logo centered no matter aspect ratio
logo_surface = pygame.image.load('Graphics/logo.png').convert_alpha()

# It's a-me Ground!
ground_surface = pygame.image.load('Graphics/groundBlock.png').convert()
ground_surface = pygame.transform.scale(ground_surface, (sprite_size, sprite_size))
# TODO not used, need to figure out how to implement rect in for loop for ground without making code messier
ground_rect = ground_surface.get_rect(topleft=(0, hScreen - (sprite_size*2)))

# Goomba
goomba_surface = pygame.image.load('Graphics/Enemy/Goomba.png').convert_alpha()
goomba_surface = pygame.transform.scale(goomba_surface, (sprite_size, sprite_size))
goomba_rect = goomba_surface.get_rect(bottomleft=(288, 624))
goomba_speed = -2
goomba_collision = True

# TODO Drawing Font to Screen
text_surface = test_font.render('Super Mario Bros.', False, 'Black')
text_rect = text_surface.get_rect(center=(wScreen/2, hScreen/3))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == ground_rect.top:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20
        if event.type == pygame.KEYDOWN and player_rect.bottom == ground_rect.top:
            if event.key == pygame.K_SPACE:
                player_gravity = -20
                jump_sound.play()
        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_LEFT:
        #        player_rect.x -= 1
        #    if event.key == pygame.K_RIGHT:
        #        player_rect.x += 1

    screen.blit(sky_surface, (0, 0))
    # wGround starts at 0
    wGround = 0
    # hGround top left corner is the pixel location
    # hGround is subtracted by two grid sizes initially to draw the first row
    hGround = hScreen - (sprite_size*2)
    # for loop for drawing the grid 2 rows
    for i in range(0, 2):
        # Nested for loop that will draw the number of ground tiles given the width of the grid
        for j in range(0, round(wGrid)):
            screen.blit(ground_surface, (wGround, hGround))
            wGround += sprite_size
        wGround = 0
        hGround = hScreen - sprite_size

    # Goomba MOVES!!!!
    goomba_rect.x += goomba_speed

    # TODO Mario Player Movement
    key_down = pygame.key.get_pressed()
    if key_down[pygame.K_LEFT]:
        if player_speed > -4:
            player_speed += -0.4

    player_rect.x += player_speed
    if key_down[pygame.K_RIGHT]:
        if player_speed < 4:
            player_speed += 0.4
    player_rect.x += player_speed
    if key_down[pygame.K_RIGHT] is False and key_down[pygame.K_LEFT] is False:
        if player_speed > 0:
            player_speed = 0
        if player_speed < 0:
            player_speed = 0


    # Goomba position reset
    if goomba_rect.right <= 0:
        goomba_rect.left = wScreen

    # TODO figure out what the heck this is lol
    if player_rect.colliderect(goomba_rect):
        if goomba_collision:
            goomba_speed *= -1
            print(goomba_speed)
            goomba_collision = False

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= ground_rect.top:
        player_rect.bottom = ground_rect.top
    player_animation()
    screen.blit(player_surf, player_rect)

    screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(60)
