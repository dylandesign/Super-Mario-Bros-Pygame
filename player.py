import pygame


class Player:
    def __init__(self, sprite_size):
        super().__init__()
        # TODO Utilize Sprite Class to encompass images and transform scale beforehand
        self.sprite_size = sprite_size
        self.player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.scale(self.player_stand, (self.sprite_size, self.sprite_size))
        self.player_walk_1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        self.player_walk_1 = pygame.transform.scale(self.player_walk_1, (self.sprite_size, self.sprite_size))
        self.player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk_2 = pygame.transform.scale(self.player_walk_2, (self.sprite_size, self.sprite_size))
        self.player_walk_3 = pygame.image.load('Graphics/Player/player_walk_slide.png').convert_alpha()
        self.player_walk_3 = pygame.transform.scale(self.player_walk_3, (self.sprite_size, self.sprite_size))
        self.player_jump = pygame.image.load('Graphics/Player/player_jump.png').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (self.sprite_size, self.sprite_size))
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0
        self.player_direction = 0
        self.player_surf = self.player_stand
        self.player_surf = pygame.transform.scale(self.player_surf, (self.sprite_size, self.sprite_size))
        self.player_rect = self.player_surf.get_rect(bottomleft=(96, 624))
        self.player_gravity = 0
        self.player_speed = 0

    def player_animation(self, ground_rect, sprite_size):
        # Player is above ground
        if self.player_rect.bottom < ground_rect.top:
            self.player_surf = self.player_jump
            if self.player_direction == 1:
                self.player_surf = pygame.transform.flip(self.player_surf, True, False)
        # Player is moving forward
        elif self.player_speed > 0:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]
            self.player_direction = 0
        # Player is moving backward
        elif self.player_speed < 0:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]
            self.player_surf = pygame.transform.flip(self.player_surf, True, False)
            self.player_direction = 1
        # Player is Standing
        else:
            self.player_surf = self.player_stand
            if self.player_direction == 1:
                self.player_surf = pygame.transform.flip(self.player_surf, True, False)

    def player_movement(self, ground_rect, jump_sound):
        key_down = pygame.key.get_pressed()
        if key_down[pygame.K_LEFT]:
            if self.player_speed > -4:
                self.player_speed += -0.4
        self.player_rect.x += self.player_speed
        if key_down[pygame.K_RIGHT]:
            if self.player_speed < 4:
                self.player_speed += 0.4
        self.player_rect.x += self.player_speed
        if key_down[pygame.K_RIGHT] is False and key_down[pygame.K_LEFT] is False:
            if self.player_speed > 0:
                self.player_speed = 0
            if self.player_speed < 0:
                self.player_speed = 0
        if key_down[pygame.K_SPACE] and self.player_rect.bottom == ground_rect.top:
            self.player_gravity = -20
            jump_sound.play()

    def player_jump_gravity(self, ground_rect):
        self.player_gravity += 1
        self.player_rect.y += self.player_gravity
        if self.player_rect.bottom >= ground_rect.top:
            self.player_rect.bottom = ground_rect.top