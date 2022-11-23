import pygame

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING
from pygame.sprite import Sprite

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5


class Dinossaur(Sprite):
    def __init__(self):
        self.image = RUNNING[0]
        self.duck_animation = DUCKING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = 310
        self.step_index = 0
        self.duck_index = 0 ## INDEX SETADO
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False ## ANIMAÇÃO SETADA EM FALSO
        self.jump_vel = JUMP_VEL

    def run (self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

        if self.step_index >= 10:
            self.step_index = 0
                
    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck: #ELIF PRA SETAR
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump: ## CHECAGEM DE INPUT
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump or self.dino_duck:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
    
    def duck(self): ## ANIMAÇÃO, INDEX E POSIÇÃO DO DINO
        self.image = DUCKING[0] if self.duck_index < 5 else DUCKING[1]
        self.dino_rect = self.duck_animation.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS + 40
        self.duck_index += 1

        if self.duck_index >= 10:
            self.duck_index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))