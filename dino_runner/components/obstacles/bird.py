import random

from dino_runner.utils.constants import BIRD, SCREEN_WIDTH
from dino_runner.components.obstacles.obstacle import Obstacle

BIRD_POSITION = [220, 250, 280]


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(BIRD_POSITION)
        self.bird_anim_index = 0

    def draw(self, screen):
        screen.blit(self.image[self.bird_anim_index // 5], self.rect)
        self.bird_anim_index += 1

        if self.bird_anim_index >= 9:
            self.bird_anim_index = 0

        

        



