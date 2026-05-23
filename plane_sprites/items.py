import random
import pygame
from .game_config import *
from .base import GameSprite

class Point:
    def __init__(self):
        self.write = pygame.font.Font(None, 50)
        self.color = 255, 255, 255

        self.point = I_POINT
        self.bomb = I_HERO_BOMB
        self.missile = I_HERO_MISSILE
        self.weapons = 1
        self.gatling_num = 0
        self.trace_num = 0

    def generate(self, blood, energy):
        self.image_point = self.write.render(f"point: {round(self.point, 1)}", True, self.color)
        self.image_blood = self.write.render(f"blood: {round(blood, 1)}", True, self.color)
        self.image_energy = self.write.render(f"energy {round(energy, 1)}", True, self.color)
        self.image_bomb = self.write.render(f"bomb: {self.bomb}", True, self.color)
        self.image_missile = self.write.render(f"missile: {self.missile}", True, self.color)

        if self.weapons == 1:
            self.image_weapons = self.write.render("weapon-Normal: oo", True, self.color)
        elif self.weapons == 2:
            self.image_weapons = self.write.render(f"weapon-Gatling: {round(self.gatling_num, 1)}", True, self.color)
        elif self.weapons == 3:
            self.image_weapons = self.write.render(f"weapon-Trace: {round(self.trace_num, 1)}", True, self.color)


class Blood(GameSprite):
    def __init__(self):
        super().__init__("./images/item/blood.png")
        self.speed_y = random.randint(1, 5)


class Energy(GameSprite):
    _VARIANT_SURFACES = None

    @classmethod
    def _get_variants(cls):
        if cls._VARIANT_SURFACES is None:
            cls._VARIANT_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                     ["./images/item/energy_1.png", "./images/item/energy_2.png",
                                      "./images/item/energy_3.png", "./images/item/energy_4.png",
                                      "./images/item/energy_5.png"]]
        return cls._VARIANT_SURFACES

    def __init__(self):
        super().__init__("./images/item/energy_1.png")
        self.speed_y = random.randint(1, 5)

        self.image_signal = random.randint(0, 4)
        self.image = Energy._get_variants()[self.image_signal]


class BombSupply(GameSprite):
    def __init__(self):
        super().__init__("./images/item/bomb_supply.png")
        self.speed_y = random.randint(1, 5)


class Ammunition(GameSprite):
    def __init__(self):
        super().__init__("./images/item/ammunition.png")
        self.speed_y = random.randint(1, 5)


