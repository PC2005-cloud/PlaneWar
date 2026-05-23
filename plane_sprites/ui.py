import pygame
from .base import GameSprite
from .constants import SCREEN_RECT

class NewGame(GameSprite):
    def __init__(self):
        super().__init__("./images/ui/again.png")
        self.rect.center = (10000, 10000)

    def update(self):
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery + self.rect.height / 2


class Quit(GameSprite):
    def __init__(self):
        super().__init__("./images/ui/gameover.png")
        self.rect.center = (10000, 10000)

    def update(self):
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery - self.rect.height / 2


class Mouse(GameSprite):
    def __init__(self):
        super().__init__("./images/ui/mouse.png")
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Resume(GameSprite):
    def __init__(self):
        super().__init__("./images/ui/resume_pressed.png")
        self.rect.center = SCREEN_RECT.center
