import pygame
import random ## escolha aleatória dos Cactus

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD ## importação da lista
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.power_ups.hammer import HAMMER_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles =  []

    def update(self, game, player):
        enemy_index = random.randint(0, 2) ## index aleatório
        if len(self.obstacles) == 0:
            if enemy_index == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS, 325))
            elif enemy_index == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 300))
            elif enemy_index == 2:
                self.obstacles.append(Bird(BIRD))
        
             
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles, player) ##atualizando estado do player
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(1000) ## aumento do delay
                    game.playing = False
                    game.death_count += 1
                    pygame.mixer.music.load('dino_runner/assets/Sounds/die.wav')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                    break
                if player.type == HAMMER_TYPE: ## se for hammer...
                    self.obstacles.remove(obstacle)

    def reset_obstacles(self):
        self.obstacles = []

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)