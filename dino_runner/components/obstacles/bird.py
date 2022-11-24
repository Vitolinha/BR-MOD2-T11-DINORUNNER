import random

from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self):
        self.bird_image = BIRD[0]
        self.bird_rect = self.bird_image.get_rect()
        self.bird_anim_index = 0

        



