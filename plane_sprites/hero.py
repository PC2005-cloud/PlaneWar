import random
import math
import pygame
from .game_config import *
from .base import GameSprite
from .constants import SCREEN_RECT, get_dir_images
from .items import Point

class Hero(GameSprite):
    _music_fire = None
    _music_laser = None
    _IK_SURFACES = None

    @classmethod
    def _get_music_fire(cls):
        if cls._music_fire is None:
            cls._music_fire = pygame.mixer.Sound('./music/gunFire.mp3')
            cls._music_fire.set_volume(0.05)
        return cls._music_fire

    @classmethod
    def _get_music_laser(cls):
        if cls._music_laser is None:
            cls._music_laser = pygame.mixer.Sound('./music/laser.wav')
            cls._music_laser.set_volume(0.1)
        return cls._music_laser

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/hero/me_destroy_1.png", "./images/hero/me_destroy_2.png",
                                 "./images/hero/me_destroy_3.png", "./images/hero/me_destroy_4.png"]]
        return cls._IK_SURFACES

    def __init__(self):
        super().__init__("./images/hero/me1_w.png")
        self.blood = I_HERO_BLOOD
        self.blood_max = 0
        self.energy = I_HERO_ENERGY
        self.hit = I_HERO_HIT

        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx

        self.speed = I_HERO_SPEED
        self.point = Point()

        self.fire_signal = 0
        self.bomb_signal = 0
        self.missile_signal = 1
        self.laser_signal = 0
        self.laser_long = 0
        self.laser_color = 0
        self.laser_increasing = 1

        self.cached_images = get_dir_images("./images/hero/me1_w.png", "./images/hero/me2_w.png")
        self.image_signal = 1

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

        self.direction = 0

        self.gatling_signal = 0
        self.trace_signal = 0
        self.blood_signal = 0

        self.numbering = 1

        self.point_fire = 0


    def update(self, mouse, bullet_h_group, bullet_t_group, bullet_m_group, missile_group,
               laser_group):
        if self.point.point > 1000:
            self.point_fire = 1000
        else:
            self.point_fire = self.point.point

        self.blood_max = I_HERO_BLOOD + int(self.point.point / 20) + 50 * int(self.point.point / 250)
        if self.point.point > 50:
            self.blood_signal = 1

        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        if self.rect.y < -self.rect.height:
            self.rect.y = SCREEN_RECT.height
        if self.rect.x > SCREEN_RECT.width:
            self.rect.x = -self.rect.width
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.width

        if self.blood >= 0:
            self.image_signal += 1
            frame_idx = int(self.image_signal / 10) % 2
            self.image = self.cached_images[self.direction][frame_idx]
            temp_x = self.rect.x
            temp_y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = temp_x
            self.rect.y = temp_y
        elif self.blood < 0:
            self.die()

        if self.blood_signal == 1 and self.blood >= 0:
            self.blood += I_HERO_BLOOD_SPEED * int((self.point.point + 250) / 250)

        self.fire(bullet_h_group)
        self.gatling(bullet_h_group)
        self.trace(bullet_t_group)
        self.bomb(bullet_m_group)
        self.missile(mouse, missile_group)
        self.laser(laser_group)

        self.point.gatling_num = round(self.point.gatling_num + I_HERO_GATLING_RELOAD + round(self.point.point / 1000, 1), 2)
        self.point.trace_num = round(self.point.trace_num + I_HERO_TRACE_RELOAD + round(self.point.point / 1250, 1), 2)

        if self.blood >= self.blood_max:
            self.blood = self.blood_max
        if self.energy >= I_HERO_ENERGY:
            self.energy = I_HERO_ENERGY

    def resurrection(self):
        self.point = Point()
        self.blood = I_HERO_BLOOD
        self.energy = I_HERO_ENERGY
        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx
        self.speed = I_HERO_SPEED
        self.ik_signal = 0
        self.collided_signal = 0
        self.blood_signal = 1

    def fire(self, bullet_h_group):
        if self.fire_signal % I_HERO_FIRE_interval == 0 and self.fire_signal >= I_HERO_FIRE_CYCLE - I_HERO_FIRE_TIME:
            bullet = Bullet()
            Hero._get_music_fire().play()
            self.__bullet(bullet_h_group, bullet, 0, I_HERO_FIRE_SPEED,
                          I_HERO_FIRE_SPEED, I_HERO_FIRE_SPEED, I_HERO_FIRE_SPEED)
        self.fire_signal -= 1

    def gatling(self, bullet_h_group):
        if self.point.gatling_num >= 1 and self.gatling_signal == 1:
            Hero._get_music_fire().play()
            self.point.gatling_num -= (I_HERO_GATLING_D + int( self.point_fire / 50))
            for i in range(0, I_HERO_GATLING_D + int( self.point_fire / 50)):
                bullet = Bullet()
                self.__bullet(bullet_h_group, bullet, I_HERO_GATLING_H, I_HERO_GATLING_S_MAX,
                              I_HERO_GATLING_S_MIN, I_HERO_GATLING_L_MAX, I_HERO_GATLING_L_MIN)
        self.gatling_signal -= 1

    def trace(self, bullet_t_group):
        if self.point.trace_num >= 1 and self.trace_signal == 1:
            Hero._get_music_fire().play()
            self.point.trace_num -= (I_HERO_TRACE_D + int( self.point_fire / 15))
            for i in range(0, I_HERO_TRACE_D + int( self.point_fire / 15)):
                bullet = BulletT()
                self.__bullet(bullet_t_group, bullet, I_HERO_TRACE_SPEED_H, I_HERO_TRACE_SPEED_MAX_S,
                              I_HERO_TRACE_SPEED_MIN_S, I_HERO_TRACE_SPEED_MAX_L, I_HERO_TRACE_SPEED_MIN_L)
        self.trace_signal -= 1

    def bomb(self, bullet_m_group):
        if self.bomb_signal == I_HERO_BOMB_INTERVAL:
            bomb = Bomb()
            self.__bullet(bullet_m_group, bomb, 0, I_HERO_BOMB_SPEED,
                          I_HERO_BOMB_SPEED, I_HERO_BOMB_SPEED, I_HERO_BOMB_SPEED)
            bullet_m_group.add(bomb)
        self.bomb_signal -= 1

    def missile(self, mouse, missile_group):
        if self.missile_signal == 1 and self.point.missile > 0:
            missile = Missile(self.direction)
            missile.mouse_centerx = mouse.rect.centerx
            missile.mouse_centery = mouse.rect.centery
            self.__bullet(missile_group, missile, 0, I_HERO_MISSILE_SPEED,
                          I_HERO_MISSILE_SPEED, I_HERO_MISSILE_SPEED, I_HERO_MISSILE_SPEED)
            missile_group.add(missile)
            self.point.missile -= 1

    def laser(self, laser_group):
        if self.laser_signal == 1 and self.energy >= 0 and self.point.point > 150:
            Hero._get_music_laser().play()
            self.laser_long += I_HERO_LASER_SPEED
            laser_o = Laser(-1, self.direction, self.laser_color)
            laser_o.rect.center = self.rect.center
            if self.laser_long > I_HERO_LASER_LONG:
                self.laser_long = I_HERO_LASER_LONG
            for i in range(0, int(self.laser_long / 105) + 1):
                self.energy -= I_HERO_LASER_WOOD
                laser = Laser(1, self.direction, self.laser_color)
                if self.direction == 0:
                    laser.rect.centerx = self.rect.centerx
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.bottom = self.rect.top + 105 - self.laser_long + i * 30
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.bottom = self.rect.top - i * (105 - 30)
                elif self.direction == 1:
                    laser.rect.centerx = self.rect.centerx
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.top = self.rect.bottom - 105 + self.laser_long - i * 30
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.top = self.rect.bottom + i * (105 - 30)
                elif self.direction == 2:
                    laser.rect.centery = self.rect.centery
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.right = self.rect.left + 105 - self.laser_long + i * 30
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.right = self.rect.left - i * (105 - 30)
                elif self.direction == 3:
                    laser.rect.centery = self.rect.centery
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.left = self.rect.right - 105 + self.laser_long - i * 30
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.left = self.rect.right + i * (105 - 30)
                elif self.direction == 4:
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.bottom = self.rect.top + 105 - self.laser_long + i * 50 + 50
                        laser.rect.right = self.rect.left + 105 - self.laser_long + i * 50 + 50
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.bottom = self.rect.top - i * (105 - 50) + 50
                        laser.rect.right = self.rect.left - i * (105 - 50) + 50
                elif self.direction == 5:
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.bottom = self.rect.top + 105 - self.laser_long + i * 50 + 50
                        laser.rect.left = self.rect.right - 105 + self.laser_long - i * 50 - 50
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.bottom = self.rect.top - i * (105 - 50) + 50
                        laser.rect.left = self.rect.right + i * (105 - 50) - 50
                elif self.direction == 6:
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.top = self.rect.bottom - 105 + self.laser_long - i * 50 - 50
                        laser.rect.right = self.rect.left + 105 - self.laser_long + i * 50 + 50
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.top = self.rect.bottom + i * (105 - 50) - 50
                        laser.rect.right = self.rect.left - i * (105 - 50) + 50
                elif self.direction == 7:
                    if self.laser_long < 105 * (i + 1):
                        laser.rect.top = self.rect.bottom - 105 + self.laser_long - i * 50 - 50
                        laser.rect.left = self.rect.right - 105 + self.laser_long - i * 50 - 50
                    elif self.laser_long >= 105 * (i + 1):
                        laser.rect.top = self.rect.bottom + i * (105 - 50) - 50
                        laser.rect.left = self.rect.right + i * (105 - 50) - 50
                x = self.rect.centerx - laser.rect.centerx
                y = self.rect.centery - laser.rect.centery
                laser.hit = I_HERO_LASER_FADE / pow(x ** 2 + y ** 2, 0.5) * I_HERO_LASER_HIT * self.laser_increasing
                laser_group.add(laser)
        else:
            Hero._get_music_laser().stop()
            self.laser_long = 0

    def die(self):
        self.collided_signal = 1
        self.speed = 0
        frame_idx = int(self.ik_signal / 5)
        if frame_idx < 4:
            self.image = self.ik_surfaces[frame_idx]
            self.ik_signal += 1
        elif frame_idx == 4:
            self.kill()

    def __bullet(self, bullet_group, bullet, h, s_max, s_min, l_max, l_min):
        bullet.image = bullet.cached_images[self.direction][0]
        if self.direction == 0:
            bullet.speed_y = random.randint(-s_max, -s_min)
            bullet.speed_x = random.randint(-h, h)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.centery - 55
        elif self.direction == 1:
            bullet.speed_y = random.randint(s_min, s_max)
            bullet.speed_x = random.randint(-h, h)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.centery + 55
        elif self.direction == 2:
            bullet.speed_x = random.randint(-s_max, -s_min)
            bullet.speed_y = random.randint(-h, h)
            bullet.rect.centerx = self.rect.centerx - 55
            bullet.rect.centery = self.rect.centery
        elif self.direction == 3:
            bullet.speed_x = random.randint(s_min, s_max)
            bullet.speed_y = random.randint(-h, h)
            bullet.rect.centerx = self.rect.centerx + 55
            bullet.rect.centery = self.rect.centery
        elif self.direction == 4:
            bullet.speed_x = random.randint(-l_max, -l_min)
            bullet.speed_y = random.randint(-l_max, -l_min)
            bullet.rect.centerx = self.rect.centerx - 55
            bullet.rect.centery = self.rect.centery - 55
        elif self.direction == 5:
            bullet.speed_x = random.randint(l_min, l_max)
            bullet.speed_y = random.randint(-l_max, -l_min)
            bullet.rect.centerx = self.rect.centerx + 55
            bullet.rect.centery = self.rect.centery - 55
        elif self.direction == 6:
            bullet.speed_x = random.randint(-l_max, -l_min)
            bullet.speed_y = random.randint(l_min, l_max)
            bullet.rect.centerx = self.rect.centerx - 55
            bullet.rect.centery = self.rect.centery + 55
        elif self.direction == 7:
            bullet.speed_x = random.randint(l_min, l_max)
            bullet.speed_y = random.randint(l_min, l_max)
            bullet.rect.centerx = self.rect.centerx + 55
            bullet.rect.centery = self.rect.centery + 55
        bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/hero/bullet1_w.png")
        self.cached_images = get_dir_images("./images/hero/bullet1_w.png")
        self.blood = I_HERO_FIRE_BLOOD
        self.hit = I_HERO_FIRE_HIT

class BulletT(GameSprite):
    def __init__(self):
        super().__init__("./images/hero/bullet1_w.png")
        self.cached_images = get_dir_images("./images/hero/bullet1_w.png")
        self.blood = I_HERO_FIRE_BLOOD
        self.hit = I_HERO_FIRE_HIT
        self.trace_target = -1
        self.s = 100000000
        self.trace_signal = 0

    def update(self):
        super().update()

        self.trace_signal += 1


class Bomb(GameSprite):
    _music_bomb = None

    @classmethod
    def _get_music_bomb(cls):
        if cls._music_bomb is None:
            cls._music_bomb = pygame.mixer.Sound('./music/bomb.mp3')
            cls._music_bomb.set_volume(0.5)
        return cls._music_bomb

    def __init__(self):
        super().__init__("./images/hero/bomb_w.png")
        self.cached_images = get_dir_images("./images/hero/bomb_w.png")
        self.blood = I_HERO_BOMB_BLOOD
        self.hit = random.randint(15, 25)
        self.speed_x = 0
        self.speed_y = 0

        Bomb._get_music_bomb().play()


class Missile(GameSprite):
    _music_fire = None

    @classmethod
    def _get_music_fire(cls):
        if cls._music_fire is None:
            cls._music_fire = pygame.mixer.Sound('./music/missileFire.mp3')
            cls._music_fire.set_volume(0.2)
        return cls._music_fire

    def __init__(self, direction):
        super().__init__("./images/hero/missile_1_w.png")
        self.speed = 10
        self.anim_images = get_dir_images(
            "./images/hero/missile_1_w.png", "./images/hero/missile_2_w.png",
            "./images/hero/missile_3_w.png", "./images/hero/missile_4_w.png")
        self.cached_images = self.anim_images
        self.image_signal = 0
        self.direction = direction

        self.mouse_centerx = 0
        self.mouse_centery = 0

        self.trace = 0

        Missile._get_music_fire().play()

    def update(self, explode_group):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.image_signal += 1
        self.image = self.anim_images[self.direction][int((self.image_signal / 5) % 4)]

        temp_x = self.mouse_centerx - self.rect.centerx
        temp_y = self.mouse_centery - self.rect.centery

        self.trace += 1
        if self.trace > I_HERO_MISSILE_TIME:
            if temp_y > 0 and temp_y > abs(temp_x):
                self.direction = 1
                self.speed_x = 0
                self.speed_y = I_HERO_MISSILE_SPEED
            elif temp_y < 0 and abs(temp_y) > abs(temp_x):
                self.direction = 0
                self.speed_x = 0
                self.speed_y = -I_HERO_MISSILE_SPEED
            elif temp_x > 0 and temp_x > abs(temp_y):
                self.direction = 3
                self.speed_x = I_HERO_MISSILE_SPEED
                self.speed_y = 0
            elif temp_x < 0 and abs(temp_x) > abs(temp_y):
                self.direction = 2
                self.speed_x = -I_HERO_MISSILE_SPEED
                self.speed_y = 0

            if abs(temp_x - temp_y) < I_HERO_MISSILE_SPEED:
                if temp_x > 0 and temp_y > 0:
                    self.direction = 7
                    self.speed_x = I_HERO_MISSILE_SPEED
                    self.speed_y = I_HERO_MISSILE_SPEED
                elif temp_x < 0 and temp_y < 0:
                    self.direction = 4
                    self.speed_x = -I_HERO_MISSILE_SPEED
                    self.speed_y = -I_HERO_MISSILE_SPEED
            elif abs(temp_x + temp_y) < I_HERO_MISSILE_SPEED:
                if temp_x < 0 and temp_y > 0:
                    self.direction = 6
                    self.speed_x = -I_HERO_MISSILE_SPEED
                    self.speed_y = I_HERO_MISSILE_SPEED
                if temp_x > 0 and temp_y < 0:
                    self.direction = 5
                    self.speed_x = I_HERO_MISSILE_SPEED
                    self.speed_y = -I_HERO_MISSILE_SPEED

        if abs(temp_x) < I_HERO_MISSILE_SPEED and abs(temp_y) < I_HERO_MISSILE_SPEED:
            self.die()
            explode = Explode()
            explode.rect.center = self.rect.center
            explode_group.add(explode)


class Laser(GameSprite):
    # Class-level pre-loaded surfaces: [direction][color_index]
    _ALL_SURFACES = None
    _BASE_COLORS = [
        (115, 95, 107),   # 0 - purple  (原 laser_1)
        (178, 166, 89),   # 1 - yellow  (原 laser_2)
        (179, 135, 82),   # 2 - golden  (原 laser_3)
        (123, 79, 125),   # 3 - pink    (原 laser_4)
        (164, 85, 80),    # 4 - red     (原 laser_5)
        (97, 122, 151),   # 5 - blue    (原 laser_6)
        (151, 167, 101),  # 6 - green   (原 laser_7)
    ]

    @classmethod
    def _init_surfaces(cls):
        if cls._ALL_SURFACES is not None:
            return
        variant_keys = ['s', 's', 'h', 'h', 'n', 'p', 'p', 'n']
        cls._ALL_SURFACES = []
        for key in variant_keys:
            base = pygame.image.load(f"./images/laser/laser_{key}_white.png").convert_alpha()
            colored = []
            for color in cls._BASE_COLORS:
                tinted = base.copy()
                if color != (255, 255, 255):
                    tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
                colored.append(tinted)
            cls._ALL_SURFACES.append(colored)

    def __init__(self, object, direction, color):
        super().__init__("./images/laser/laser_s_white.png")
        Laser._init_surfaces()
        self.fade = object
        self.image_signal = 0
        self.direction = direction
        self.color = color

        self.image = Laser._ALL_SURFACES[self.direction][self.color % 7]
        temp_x = self.rect.x
        temp_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = temp_x
        self.rect.y = temp_y



    def update(self):
        self.blood = 1
        super().update()

        if self.fade == 0:
            self.die()
        self.fade -= 1


class Explode(GameSprite):
    _FRAMES = None
    _music_boom = None

    @classmethod
    def _get_frames(cls):
        if cls._FRAMES is None:
            cls._FRAMES = [pygame.image.load(f"./images/explode/{i}.png").convert_alpha() for i in range(1, 29)]
        return cls._FRAMES

    @classmethod
    def _get_music_boom(cls):
        if cls._music_boom is None:
            cls._music_boom = pygame.mixer.Sound('./music/boom.wav')
            cls._music_boom.set_volume(0.5)
        return cls._music_boom

    def __init__(self):
        super().__init__("./images/explode/1.png")
        self.blood = 10000
        self.hit = I_HERO_MISSILE_HIT
        self.image_signal = 0

        Explode._get_music_boom().play()

    def update(self):
        self.image_signal += 1
        self.image = Explode._get_frames()[int(self.image_signal / I_HERO_MISSILE_AV) % 28]
        if self.image_signal / I_HERO_MISSILE_AV == 28:
            self.die()
        if self.image_signal == 2:
            self.hit = I_HERO_MISSILE_HOT


