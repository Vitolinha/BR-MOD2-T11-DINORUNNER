import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, HAMMER_TYPE, DUCKING_HAMMER, JUMPING_HAMMER, RUNNING_HAMMER

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('dino_runner/assets/Sounds/game_song.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False ## ANIMAÇÃO SETADA EM FALSO
        self.jump_vel = JUMP_VEL
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.show_text = False
        self.shield_time_up = 0
                
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck: #ELIF PRA SETAR
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump and not self.dino_duck:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
            pygame.mixer.music.load('dino_runner/assets/Sounds/jump.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        elif user_input[pygame.K_DOWN] and not self.dino_jump: ## CHECAGEM DE INPUT
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif user_input[pygame.K_DOWN] and self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.9
        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
        
        if self.step_index >= 9:
            self.step_index = 0

    def run (self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 3.5
            self.jump_vel -= 0.8
            
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS - 20
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
    
    def duck(self): ## ANIMAÇÃO, INDEX E POSIÇÃO DO DINO
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS + 40
        self.step_index += 1
        self.dino_duck = False

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))