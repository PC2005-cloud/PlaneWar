import random
import math
import pygame
from .game_config import *
from .base import GameSprite
from .constants import SCREEN_RECT, get_dir_images, ANGLE_TO_DIR
from .hero import Explode

class Enemy(GameSprite):
    _music_die = None
    _IK_SURFACES = None

    @classmethod
    def _get_music_die(cls):
        if cls._music_die is None:
            cls._music_die = pygame.mixer.Sound('./music/enemyDie.wav')
            cls._music_die.set_volume(0.5)
        return cls._music_die

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/enemy/enemy1_down1.png", "./images/enemy/enemy1_down2.png",
                                 "./images/enemy/enemy1_down3.png", "./images/enemy/enemy1_down4.png"]]
        return cls._IK_SURFACES

    def __init__(self):
        image_list = ["./images/enemy/enemy1_1.png", "./images/enemy/enemy1_2.png",
                      "./images/enemy/enemy1_3.png", "./images/enemy/enemy1_4.png", "./images/enemy/enemy1_5.png"]
        super().__init__(random.choice(image_list))
        self.speed_y = random.choice(I_ENEMY_SPEED)
        self.blood = random.choice(I_ENEMY_BLOOD)
        self.hit = I_ENEMY_HIT
        self.score = self.blood
        self.fire_signal = random.choice(I_ENEMY_FIRE_SIGNAL)
        self.fire_space = 15
        self.fire_time_y = random.randint(50, 150)
        self.fire_time = self.fire_time_y

        self.numbering = 1

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

        self.start_signal = random.randint(1,3)
        self.start_speed = random.randint(15, 20)
        self.speed_temp = self.speed_y

    def update(self, hero, bullet_e_group):
        super().update_2(hero)

        if self.start_signal == 1:
            self.speed_y = self.start_speed
            self.start_signal = 2
        if self.speed_y > self.speed_temp:
            self.speed_y -= 0.25

        if self.fire_signal == 1 and self.blood > 0:
            self.fire(bullet_e_group)

    def fire(self, bullet_e_group):
        if self.fire_time == 0:
            self.fire_space -= 1
            if self.fire_space in (0, 5, 10):
                bullet_e = BulletE()
                bullet_e.rect.x = self.rect.centerx
                bullet_e.rect.y = self.rect.y
                bullet_e_group.add(bullet_e)
                if self.fire_space == 0:
                    self.fire_time = self.fire_time_y
                    self.fire_space = 15

        else:
            self.fire_time -= 1

    def die_2(self, hero):
        self.collided_signal = 1
        self.speed_y = 0
        if self.ik_signal / 5 < 4:
            self.image = self.ik_surfaces[int(self.ik_signal / 5)]
            self.ik_signal += 1
        elif self.ik_signal / 5 == 4:
            Enemy._get_music_die().play()
            self.kill()
            hero.point.point += self.score


class EnemyR(GameSprite):
    _music_boom = None
    _music_rush = None

    @classmethod
    def _get_music_boom(cls):
        if cls._music_boom is None:
            cls._music_boom = pygame.mixer.Sound('./music/boom.wav')
            cls._music_boom.set_volume(0.5)
        return cls._music_boom

    @classmethod
    def _get_music_rush(cls):
        if cls._music_rush is None:
            cls._music_rush = pygame.mixer.Sound('./music/rush.wav')
            cls._music_rush.set_volume(0.5)
        return cls._music_rush

    def __init__(self):
        super().__init__("./images/enemy/enemy_r.png")
        self.image_template = self.image
        self.direction = random.randint(0, 2)
        self.blood = 0.1
        self.score = 1.5

        self.numbering = 3

        if self.direction == 0:
            self.rect.bottom = 0
            max_x = SCREEN_RECT.width
            self.rect.x = random.randint(0, max_x - self.rect.width)
            self.speed_y = I_ENEMY_RED_SPEED
            self.image = pygame.transform.rotate(self.image_template, 0)
        elif self.direction == 1:
            self.rect.right = 0
            max_y = SCREEN_RECT.height
            self.rect.y = random.randint(0, max_y - self.rect.height)
            self.speed_x = int(I_ENEMY_RED_SPEED * 1.25)
            self.image = pygame.transform.rotate(self.image_template, 90)
        elif self.direction == 2:
            self.rect.left = SCREEN_RECT.width
            max_y = SCREEN_RECT.height
            self.rect.y = random.randint(0, max_y - self.rect.height)
            self.speed_x = -int(I_ENEMY_RED_SPEED * 1.25)
            self.image = pygame.transform.rotate(self.image_template, 270)

        EnemyR._get_music_rush().play()


    def update(self, hero, explode_e_group):
        super().update_2(hero)
        if self.blood < 0:
            EnemyR._get_music_boom().play()
            explode = Explode()
            explode.hit = I_ENEMY_RED_HIT
            explode.rect.center = self.rect.center
            explode_e_group.add(explode)


class EnemyB(GameSprite):
    _music_die = None

    @classmethod
    def _get_music_die(cls):
        if cls._music_die is None:
            cls._music_die = pygame.mixer.Sound('./music/enemyDie.wav')
            cls._music_die.set_volume(0.5)
        return cls._music_die

    def __init__(self):
        super().__init__("./images/enemy/enemy_b.png")
        self.blood = 0.1
        self.score = 1.5
        self.speed_y = random.choice(I_BLUE_SPEED)
        self.numbering = 4

        self.fire_signal = 0

    def update(self, hero, bullet_e_group):
        super().update_2(hero)
        if self.blood >= 0:
            self.fire(bullet_e_group)
        if self.blood < 0:
            EnemyB._get_music_die().play()
            for i in range(I_BLUE_NUM):
                bullet_e = BulletE()
                bullet_e.rect.center = self.rect.center
                bullet_e.speed_x = int(math.cos(2 * math.pi * i / I_BLUE_NUM) * I_BLUE_BULLET_SPEED)
                bullet_e.speed_y = int(math.sin(2 * math.pi * i / I_BLUE_NUM) * I_BLUE_BULLET_SPEED)
                bullet_e_group.add(bullet_e)

    def fire(self, bullet_e_group):
        self.fire_signal += 1
        for i in range(I_BLUE_BULLET_D):
            if self.fire_signal % I_BLUE_BULLET_CYCLE == 0:
                bullet_e = BulletE()
                bullet_e.hit = I_BLUE_BULLET_HIT
                bullet_e.rect.center = self.rect.center
                bullet_e.speed_x = random.choice(I_BLUE_BULLET_SPEED_X)
                bullet_e.speed_y = random.choice(I_BLUE_BULLET_SPEED_Y) + self.speed_y
                bullet_e_group.add(bullet_e)


class BigEnemy(GameSprite):
    _music_die = None
    _IK_SURFACES = None
    _HIT_SURFACE = None

    @classmethod
    def _get_music_die(cls):
        if cls._music_die is None:
            cls._music_die = pygame.mixer.Sound('./music/boom.wav')
            cls._music_die.set_volume(0.5)
        return cls._music_die

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/enemy/enemy2_down1.png", "./images/enemy/enemy2_down2.png",
                                 "./images/enemy/enemy2_down3.png", "./images/enemy/enemy2_down4.png"]]
        return cls._IK_SURFACES

    @classmethod
    def _get_hit_surface(cls):
        if cls._HIT_SURFACE is None:
            cls._HIT_SURFACE = pygame.image.load("./images/enemy/enemy2_hit.png").convert_alpha()
        return cls._HIT_SURFACE

    def __init__(self):
        super().__init__("./images/enemy/enemy2.png")
        self.speed_y = random.choice(I_BIG_BLOOD_SPEED)
        self.blood = random.choice(I_BIG_BLOOD)
        self.hit = I_BIG_HIT
        self.score = int(self.blood / 3)
        self.fire_signal = random.choice(I_BIG_FIRE_SIGNAL)
        self.bulletb_group = pygame.sprite.Group()
        self.bulletb_fire_group = pygame.sprite.Group()
        self.update_signal = 0
        self.fire_time_y = random.randint(100, 200)
        self.fire_time = self.fire_time_y

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

        self.hit_image = self._get_hit_surface()
        self.normal_image = self.image

        self.start_signal = random.randint(1, 2)
        self.start_speed = random.randint(5, 10)
        self.speed_temp = self.speed_y

        self.numbering = 2

    def update(self, hero, bullet_b_group):
        if self.update_signal == 0:
            self.update_signal = 1
        elif self.update_signal == 1:
            self.update_signal = 0
            super().update_2(hero)

        if self.start_signal == 1:
            self.speed_y = self.start_speed
            self.start_signal = 2
        if self.speed_y > self.speed_temp:
            self.speed_y -= 0.1

        if self.fire_signal == 1 and self.blood > 0:
            self.fire(bullet_b_group)

    def fire(self, bullet_b_group):
        if self.fire_time == 5:
            self.image = self.hit_image
        elif self.fire_time == self.fire_time_y - 10:
            self.image = self.normal_image

        if self.fire_time == 0:
            bullet_b = BulletB()
            bullet_b.rect.x = self.rect.centerx - 6
            bullet_b.rect.y = self.rect.y + 20
            bullet_b_group.add(bullet_b)
            self.fire_time = self.fire_time_y
        else:
            self.fire_time -= 1

    def die_2(self, hero):
        if self.collided_signal != 1:
            BigEnemy._get_music_die().play()
        self.collided_signal = 1
        self.speed_y = 0
        if self.ik_signal / 5 < 4:
            self.image = self.ik_surfaces[int(self.ik_signal / 5)]
            self.ik_signal += 1
        elif self.ik_signal / 5 == 4:
            hero.point.point += self.score
            self.kill()


class BigEnemyP(GameSprite):
    _IK_SURFACES = None

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/enemy/enemy2_down1.png", "./images/enemy/enemy2_down2.png",
                                 "./images/enemy/enemy2_down3.png", "./images/enemy/enemy2_down4.png"]]
        return cls._IK_SURFACES

    def __init__(self, point):
        super().__init__("./images/enemy/enemy2p.png")
        self.cached_dir_images = get_dir_images("./images/enemy/enemy2p.png")
        self.blood = random.choice(I_PURPLE_BLOOD)
        self.hit = I_PURPLE_HIT
        self.score = 5
        self.speed_y = 10
        self.numbering = 5
        self.point = point

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

        self.call_signal = 0

        self.trace_signal = 0

    def update(self, hero, enemy_group, red_group, blue_group,
               big_enemy_group, purple_group):
        super().update_2(hero)

        if self.blood <= 0:
            return

        if self.trace_signal < 45:
            self.trace_signal += 1
            self.speed_y -= 0.2
        else:
            temp_x = hero.rect.centerx - self.rect.centerx
            temp_y = hero.rect.centery - self.rect.centery
            if abs(temp_x) > abs(temp_y):
                if temp_x < 0:
                    self.speed_x = -I_PURPLE_SPEED
                    self.speed_y = 0
                    self.image = self.cached_dir_images[3][0]
                else:
                    self.speed_x = I_PURPLE_SPEED
                    self.speed_y = 0
                    self.image = self.cached_dir_images[2][0]
            else:
                if temp_y < 0:
                    self.speed_y = -I_PURPLE_SPEED
                    self.speed_x = 0
                    self.image = self.cached_dir_images[1][0]
                else:
                    self.speed_y = I_PURPLE_SPEED
                    self.speed_x = 0
                    self.image = self.cached_dir_images[0][0]

            if abs(temp_x - temp_y) <= I_PURPLE_SPEED:
                if temp_x > 0:
                    self.speed_y = I_PURPLE_SPEED
                    self.speed_x = I_PURPLE_SPEED
                    self.image = self.cached_dir_images[4][0]
                elif temp_x < 0:
                    self.speed_y = -I_PURPLE_SPEED
                    self.speed_x = -I_PURPLE_SPEED
                    self.image = self.cached_dir_images[7][0]
            elif abs(temp_x + temp_y) <= I_PURPLE_SPEED:
                if temp_x > 0:
                    self.speed_y = -I_PURPLE_SPEED
                    self.speed_x = I_PURPLE_SPEED
                    self.image = self.cached_dir_images[6][0]
                elif temp_x < 0:
                    self.speed_y = I_PURPLE_SPEED
                    self.speed_x = -I_PURPLE_SPEED
                    self.image = self.cached_dir_images[5][0]

        self.call(enemy_group, red_group, blue_group, big_enemy_group, purple_group)

    def die_2(self, hero):
        self.collided_signal = 1
        self.speed_x = 0
        self.speed_y = 0
        if self.ik_signal / 5 < 4:
            self.image = self.ik_surfaces[int(self.ik_signal / 5)]
            self.ik_signal += 1
        elif self.ik_signal / 5 == 4:
            hero.point.point += self.score
            self.kill()

    def call(self, enemy_group, red_group, blue_group, big_enemy_group, purple_group):
        self.call_signal = random.randint(0, max(0, 1200 - int(self.point / 10)))
        if self.call_signal < 12:
            if self.call_signal % 4 == 0:
                enemy = Enemy()
                enemy.rect.center = self.rect.center
                enemy_group.add(enemy)
            elif self.call_signal % 4 == 1:
                big_enemy = BigEnemy()
                big_enemy.rect.center = self.rect.center
                big_enemy_group.add(big_enemy)
            elif self.call_signal % 4 == 2:
                red = EnemyR()
                red.rect.center = self.rect.center
                red_group.add(red)
            elif self.call_signal % 4 == 3:
                blue = EnemyB()
                blue.rect.center = self.rect.center
                blue_group.add(blue)
        elif self.call_signal == 13:
            purple = BigEnemyP(self.point)
            purple.rect.center = self.rect.center
            purple_group.add(purple)


class BulletE(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet/bullet2.png")
        self.blood = I_ENEMY_BULLET_BLOOD
        self.hit = I_ENEMY_BULLET_HIT
        self.speed_y = random.choice(I_ENEMY_BULLET_SPEED)


class BulletB(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet/bullet3.png")
        self.speed_y = 10
        self.blood = 3
        self.hit = I_BIG_BULLET_HIT


