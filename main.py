import pygame
from sys import exit

from player import Player

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
# Title Screen Logo
# TODO implement sizing to match resolution and have logo centered no matter aspect ratio
logo_surface = pygame.image.load('Graphics/logo.png').convert_alpha()
# It's a-me Ground!
ground_surface = pygame.image.load('Graphics/groundBlock.png').convert()
ground_surface = pygame.transform.scale(ground_surface, (sprite_size, sprite_size))
# TODO not used, need to figure out how to implement rect in for loop for ground without making code messier
ground_rect = ground_surface.get_rect(topleft=(0, hScreen - (sprite_size*2)))
# TODO Drawing Font to Screen
text_surface = test_font.render('Super Mario Bros.', False, 'Black')
text_rect = text_surface.get_rect(center=(wScreen/2, hScreen/3))

player1 = Player(sprite_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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
    player1.player_movement(ground_rect, jump_sound)

    player1.player_jump_gravity(ground_rect)
    player1.player_animation(ground_rect, sprite_size)
    screen.blit(player1.player_surf, player1.player_rect)

    screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(60)
