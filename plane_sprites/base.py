import random
import pygame
from .constants import SCREEN_RECT
from .game_config import I_BG_W, I_BG_H

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width
        self.rect.x = random.randint(0, max_x - self.rect.width)
        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0
        self.blood = 1
        self.score = 0
        self.hit = 0
        self.collided_signal = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.y > SCREEN_RECT.height or
                self.rect.y < -self.rect.height or
                self.rect.x > SCREEN_RECT.width or
                self.rect.x < -self.rect.width or
                self.blood <= 0):
            self.die()

    def die(self):
        self.kill()

    def update_2(self, hero):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.y > SCREEN_RECT.height or
                self.rect.y < -self.rect.height or
                self.rect.x > SCREEN_RECT.width or
                self.rect.x < -self.rect.width):
            self.die()

        if self.blood <= 0:
            self.die_2(hero)

    def die_2(self, hero):
        hero.point.point += self.score
        self.kill()


class Background(GameSprite):
    def __init__(self, x, y):
        super().__init__("./images/background/background.png")
        self.rect.x = I_BG_W * x
        self.rect.y = I_BG_H * y
        self.speed_y = 1

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height


