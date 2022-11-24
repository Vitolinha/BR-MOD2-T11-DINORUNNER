import pygame
import random ## escolha aleatória dos Cactus

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS ## importação da lista
from dino_runner.components.obstacles.cactus import Cactus


class ObstacleManager:
    def __init__(self):
        self.obstacles =  []

    def update (self, game):
        cactus_index = random.randint(0, 1) ## index aleatório
        if len(self.obstacles) == 0:
            if cactus_index == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            if cactus_index == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))
        
             
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                game.death_count += 1
                break

    def reset_obstacles(self):
        self.obstacles = []

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)