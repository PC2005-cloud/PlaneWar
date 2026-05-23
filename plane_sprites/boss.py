import random
import math
import pygame
from .game_config import *
from .base import GameSprite
from .constants import SCREEN_RECT
from .enemies import BulletE

class Boss(GameSprite):
    class_number = 0
    _music_die = None
    _NORMAL_FRAMES = None
    _IK_SURFACES = None

    @classmethod
    def _get_music_die(cls):
        if cls._music_die is None:
            cls._music_die = pygame.mixer.Sound('./music/boom.wav')
            cls._music_die.set_volume(0.9)
        return cls._music_die

    @classmethod
    def _get_normal_frames(cls):
        if cls._NORMAL_FRAMES is None:
            cls._NORMAL_FRAMES = [pygame.image.load("./images/enemy/enemy3_n1.png").convert_alpha(),
                                  pygame.image.load("./images/enemy/enemy3_n2.png").convert_alpha()]
        return cls._NORMAL_FRAMES

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/enemy/enemy3_down1.png", "./images/enemy/enemy3_down2.png",
                                 "./images/enemy/enemy3_down3.png", "./images/enemy/enemy3_down4.png"]]
        return cls._IK_SURFACES

    def __init__(self, point):
        super().__init__("./images/enemy/enemy3_n1.png")
        if point < 9500:
            self.point = point
        else:
            self.point = 9500
        self.speed_y = 13
        self.rect.bottom = 0
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.blood = I_BOSS_BLOOD * self.point / 500
        self.blood_max = self.blood
        self.hit = 1000000
        self.score = 50
        self.fire_signal = random.randint(1, 3)
        self.fire_space = 15
        self.fire_time_y = random.randint(50, 150)
        self.fire_time = self.fire_time_y
        self.bullete_group = pygame.sprite.Group()
        self.bullete_fire_group = pygame.sprite.Group()

        self.normal_frames = self._get_normal_frames()
        self.image_signal = 0

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

        self.move_signal = 0

        self.sprint_signal = 0

        self.numbering = Boss.class_number
        Boss.class_number += 10

        self.shield_time = 0
        self.boom_signal = 0
        self.boll_signal = 0
        self.boll_time = 0
        self.trace_signal = 0
        self.hot_signal = 0
        self.gatling_signal = 0
        self.gatling_time = 0
        self.gatling_total = 0
        self.meteor_signal = 0
        self.split_signal = 0
        self.rail_signal = 0
        self.cycle_signal = 0
        self.gather_signal = 0

    def update(self, hero, shield_group, boom_group, boll_group, trace_group, hot_group,
               gatling_group, meteor_group, split_group, rail_group, cycle_group, gather_group,
               bullet_e_group=None):
        if self.speed_x == 0 and self.speed_y == 0 and self.blood >= 0:
            self.move_signal = random.randint(1, int(I_BOSS_MOVE * (2 - 1 / (0.5 + self.point))))
            self.sprint_signal = random.randint(1, int(I_BOSS_MOVE * (2 - 1 / (0.5 + self.point))))

        if self.move_signal == 1:
            self.speed_x = random.randint(-20, 20)
            self.move_signal = 0

        if self.sprint_signal == 1:
            self.speed_y = 25.25
            self.sprint_signal = 0

        if self.speed_y != 0:
            self.rect.y += self.speed_y
            self.speed_y -= 0.25
        elif self.speed_y == 0:
            self.rect.y = 88

        if self.speed_x != 0:
            self.rect.x += self.speed_x
            if self.speed_x > 0:
                self.speed_x -= 0.25
            elif self.speed_x < 0:
                self.speed_x += 0.25

        if self.blood >= 0:
            self.image_signal += 1
            self.image = self.normal_frames[int(self.image_signal / 10) % 2]
        elif self.blood < 0:
            self.die_2(hero)


        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        if self.rect.y < -self.rect.height:
            self.rect.y = SCREEN_RECT.height
        if self.rect.x > SCREEN_RECT.width:
            self.rect.x = -self.rect.width
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.width

        self.fire(bullet_e_group)
        self.shield(shield_group)
        self.boom(boom_group)
        self.boll(boll_group)
        self.trace(trace_group)
        self.hot(hot_group)
        self.gatling(hero, gatling_group)
        self.meteor(meteor_group)
        self.split(split_group)
        self.rail(hero, rail_group)
        self.cycle(cycle_group)
        self.gather(gather_group)

    def fire(self, bullet_e_group):
        if self.fire_time == 0:
            self.fire_space -= 1
            if self.fire_space in (0, 5, 10):
                bullete = BulletE()
                bullete.rect.x = self.rect.centerx
                bullete.rect.y = self.rect.y
                bullet_e_group.add(bullete)
                if self.fire_space == 0:
                    self.fire_time = self.fire_time_y
                    self.fire_space = 15
        else:
            self.fire_time -= 1

    def die_2(self, hero):
        if self.collided_signal != 1:
            Boss._get_music_die().play()
        self.collided_signal = 1
        self.speed_x = 0
        self.speed_y = 0
        if self.ik_signal / 37 < 4:
            self.image = self.ik_surfaces[int(self.ik_signal / 37)]
            self.ik_signal += 1
        elif self.ik_signal / 37 == 4:
            hero.point.point += self.score
            self.kill()

    def shield(self, shield_group):
        self.shield_signal = random.randint(1, I_BOSS_SHIELD_CYCLE)
        if self.shield_signal == 1:
            self.shield_time = I_BOSS_SHIELD_TIME
        if self.shield_time >= 0:
            shield = Shield()
            shield_group.add(shield)
            shield.rect.center = self.rect.center
            self.shield_time -= 1

    def boom(self, boom_group):
        self.boom_signal = random.randint(1, int(I_BOSS_BOOM_CYCLE - self.point / 5))
        if self.boom_signal == 1 and self.blood > 0:
            for i in range(0, I_BOSS_BOOM_D):
                boom = Boom()
                boom.rect.center = self.rect.center
                boom_group.add(boom)

    def boll(self, boll_group):
        if self.boll_signal in range(1, 3):
            if self.boll_signal == 1:
                if self.boll_time / I_BOSS_BOLL_FIRE in range(0, I_BOSS_BOLL_NUM):
                    boll = Boll()
                    boll.rect.center = self.rect.center
                    boll.speed_x = int(
                        math.cos(math.pi / I_BOSS_BOLL_NUM * 2 * self.boll_time / I_BOSS_BOLL_FIRE) * I_BOSS_BOLL_SPEED)
                    boll.speed_y = int(
                        math.sin(math.pi / I_BOSS_BOLL_NUM * 2 * self.boll_time / I_BOSS_BOLL_FIRE) * I_BOSS_BOLL_SPEED)
                    boll_group.add(boll)
                    self.boll_time += 1
                elif self.boll_time / I_BOSS_BOLL_FIRE >= I_BOSS_BOLL_NUM:
                    self.boll_signal = 0
                    self.boll_time = 0
                else:
                    self.boll_time += 1
            elif self.boll_signal == 2:
                for i in range(0, I_BOSS_BOLL_NUM):
                    boll = Boll()
                    boll.rect.center = self.rect.center
                    boll.speed_x = int(math.cos(math.pi / I_BOSS_BOLL_NUM * 2 * i) * I_BOSS_BOLL_SPEED)
                    boll.speed_y = int(math.sin(math.pi / I_BOSS_BOLL_NUM * 2 * i) * I_BOSS_BOLL_SPEED)
                    boll_group.add(boll)
                    self.boll_signal = 0
        else:
            self.boll_signal = random.randint(1, int(I_BOSS_BOLL_CYCLE - self.point / 5) * 2)

    def trace(self, trace_group):
        self.trace_signal = random.randint(0, int(I_BOSS_TRACE_CYCLE - self.point / 5))
        if self.trace_signal == 1 and self.blood > 0:
            trace = Trace()
            trace.rect.center = self.rect.center
            trace_group.add(trace)

    def hot(self, hot_group):
        self.hot_signal = random.randint(0, int(I_BOSS_HOT_CYCLE - self.point / 10))
        if self.hot_signal == 1 and self.blood > 0:
            hot = Hot()
            hot.rect.center = self.rect.center
            hot_group.add(hot)

    def gatling(self, hero, gatling_group):
        if self.gatling_signal == 1 and self.blood > 0:
            if self.gatling_time == 0:
                self.gatling_total = random.choice(I_BOSS_S_NUM)
            if self.gatling_time / I_BOSS_S_FIRE in range(0, self.gatling_total):
                gatling = Gatling()
                gatling.rect.centerx = self.rect.centerx
                gatling.rect.centery = self.rect.centery + self.rect.height / 2 - 25
                if gatling.blood > 0 and gatling.trace_signal == 0:
                    gatling.trace_signal += 1
                    x = gatling.rect.centerx - hero.rect.centerx
                    y = gatling.rect.centery - hero.rect.centery
                    l = int(pow(x ** 2 + y ** 2, 0.5))
                    if l != 0:
                        gatling.speed_x = -I_BOSS_S_SPEED * x / l
                        gatling.speed_y = -I_BOSS_S_SPEED * y / l
                gatling_group.add(gatling)
                self.gatling_time += 1
            elif self.gatling_time / I_BOSS_S_FIRE >= self.gatling_total:
                self.gatling_signal = 0
                self.gatling_time = 0
            else:
                self.gatling_time += 1
        else:
            self.gatling_signal = random.randint(0, int(I_BOSS_S_CYCLE - self.point / 5))

    def meteor(self, meteor_group):
        self.meteor_signal = random.randint(0, int(I_BOSS_METEOR_CYCLE - self.point / 5))
        if self.meteor_signal == 1 and self.blood > 0:
            for i in range(0, I_BOSS_METEOR_SUM):
                meteor = Meteor()
                meteor_group.add(meteor)

    def split(self, split_group):
        self.split_signal = random.randint(0, int(I_BOSS_SPLIT_CYCLE - self.point / 5))
        if self.split_signal == 1 and self.blood > 0:
            split = Split()
            split.rect.center = self.rect.center
            split_group.add(split)

    def rail(self, hero, rail_group):
        self.rail_signal = random.randint(0, int(I_BOSS_RAIL_CYCLE - self.point / 5))
        if self.rail_signal == 0 and self.blood > 0:
            rail = Rail()
            rail.rect.center = self.rect.center
            x = rail.rect.centerx - hero.rect.centerx
            y = rail.rect.centery - hero.rect.centery
            l = int(pow(x ** 2 + y ** 2, 0.5))
            if l != 0:
                rail.speed_x = -random.choice(I_BOSS_RAIL_SPEED) * x / l
                rail.speed_y = -random.choice(I_BOSS_RAIL_SPEED) * y / l
            rail_group.add(rail)

    def cycle(self, cycle_group):
        self.cycle_signal = random.randint(0, int(I_BOSS_CYCLE_CYCLE - self.point / 15))
        if self.cycle_signal == 1 and self.blood > 0:
            cycle = Cycle()
            cycle.number = self.numbering
            cycle.rect.center = self.rect.center
            cycle.speed_x = random.randint(-I_BOSS_CYCLE_SPEED, I_BOSS_CYCLE_SPEED)
            cycle.speed_y = random.randint(-I_BOSS_CYCLE_SPEED, I_BOSS_CYCLE_SPEED)
            cycle_group.add(cycle)

    def gather(self, gathering_group):
        self.gather_signal = random.randint(0, int(I_BOSS_GATHER_CYCLE - self.point / 4))
        if self.gather_signal == 1 and self.blood > 0:
            for i in range(0, I_BOSS_GATHER_NUM):
                gather = Gather()
                gather.rect.center = self.rect.center
                a = random.randint(0, 24)
                speed = random.choice(I_BOSS_GATHER_SPEED)
                gather.speed_x = speed * math.sin(math.pi * a / 12)
                gather.speed_y = speed * math.cos(math.pi * a / 12)
                gathering_group.add(gather)


class Boom(GameSprite):
    _IK_SURFACES = None

    @classmethod
    def _get_ik_surfaces(cls):
        if cls._IK_SURFACES is None:
            cls._IK_SURFACES = [pygame.image.load(p).convert_alpha() for p in
                                ["./images/boss/boom_1.png", "./images/boss/boom_2.png", "./images/boss/boom_3.png",
                                 "./images/boss/boom_4.png", "./images/boss/boom_5.png"]]
        return cls._IK_SURFACES

    def __init__(self):
        super().__init__("./images/boss/boom.png")
        self.hit = random.choice(I_BOSS_BOOM) / 10

        self.blood = random.choice(I_BOSS_BOOM_BLOOD)

        self.speed_x = random.choice(I_BOSS_BOOM_SPEED_X)
        self.speed_y = random.randint(-I_BOSS_BOOM_SPEED_Y, I_BOSS_BOOM_SPEED_Y)

        self.speed_d = I_BOSS_BOOM_A

        self.ik_surfaces = self._get_ik_surfaces()
        self.ik_signal = 0

    def update(self, bullet_h_group, bullet_t_group, bullet_group):
        super().update()
        self.speed_y += self.speed_d

        list_bullet = [bullet_h_group, bullet_t_group, bullet_group]
        for bullet_group in list_bullet:
            for bullet in bullet_group:
                if (abs(self.rect.centerx - bullet.rect.centerx) <= I_BOSS_BOOM_RANGE
                        and abs(self.rect.centery - bullet.rect.centery) <= I_BOSS_BOOM_RANGE
                        and self.blood <= 0):
                    bullet.blood = 0

    def die(self):
        self.collided_signal = 1
        self.speed_x = 0
        self.speed_y = 0
        self.speed_d = 0
        if self.ik_signal / 5 in range(0, 5):
            self.image = self.ik_surfaces[int(self.ik_signal / 5)]
        elif self.ik_signal / 5 == 5:
            self.kill()
        self.ik_signal += 1


class Boll(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_1.png")
        self.blood = I_BOSS_BOLL_BLOOD
        self.hit = I_BOSS_BOLL_HIT

        self.speed_x = 1
        self.speed_y = 1

    def update(self):
        super().update()


class Trace(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_5.png")

        self.blood = random.choice(I_BOSS_TRACE_BLOOD)
        self.hit = random.choice(I_BOSS_TRACE_HIT)

        self.speed_x = random.randint(-I_BOSS_TRACE_FIRE, I_BOSS_TRACE_FIRE)
        self.speed_y = random.randint(-I_BOSS_TRACE_FIRE, I_BOSS_TRACE_FIRE)

        self.trace_signal = 0

        self.trace_target = 1

    def update(self, hero):
        super().update()

        self.trace_signal += 1

        if self.blood > 0 and self.trace_signal > I_BOSS_TRACE_TIME:
            x = self.rect.centerx - hero.rect.centerx
            y = self.rect.centery - hero.rect.centery
            l = int(pow(x ** 2 + y ** 2, 0.5))
            if l != 0:
                self.speed_x = -I_BOSS_TRACE_SPEED * x / l
                self.speed_y = -I_BOSS_TRACE_SPEED * y / l


class Hot(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_9.png")

        self.hit = I_BOSS_HOT_HIT
        self.blood = 10000

        self.speed_x = random.randint(-I_BOSS_HOT_SPEED, I_BOSS_HOT_SPEED)
        self.speed_y = random.randint(-I_BOSS_HOT_SPEED, I_BOSS_HOT_SPEED)
        if self.speed_x == 0:
            self.speed_x = 1
        if self.speed_y == 0:
            self.speed_y = 1

        self.trace_signal = 0

    def update(self):
        super().update()


class Gatling(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_3.png")

        self.hit = I_BOSS_S_HIT
        self.blood = I_BOSS_S_BLOOD

        self.speed_x = 0
        self.speed_y = 0

        self.trace_signal = 0

        self.trace_target = 1


class Meteor(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_8.png")

        self.hit = random.choice(I_BOSS_METEOR_HIT)
        self.blood = random.choice(I_BOSS_METEOR_BLOOD)

        self.speed_x = random.choice(I_BOSS_METEOR_X)
        self.speed_y = random.choice(I_BOSS_METEOR_Y)

        self.rect.bottom = 0
        max_x = SCREEN_RECT.width
        self.rect.x = random.randint(0, max_x - 50)

    def update(self):
        super().update()


class Split(GameSprite):
    _BOLL7_SIZES = [100, 75, 50, 35, 20, 10]
    _SKIN_SURFACES = None

    @classmethod
    def _get_skins(cls):
        if cls._SKIN_SURFACES is None:
            base = pygame.image.load("./images/boss/boll_7_100.png").convert_alpha()
            w, h = base.get_size()
            cls._SKIN_SURFACES = [base] + [
                pygame.transform.smoothscale(base, (max(1, int(w * s / 100)), max(1, int(h * s / 100))))
                for s in cls._BOLL7_SIZES[1:]
            ]
        return cls._SKIN_SURFACES

    def __init__(self):
        super().__init__("./images/boss/boll_7_100.png")
        self._get_skins()

        self.ik_signal = 0

        self.hit = random.choice(I_BOSS_SPLIT_HIT)
        self.blood = random.choice(I_BOSS_SPLIT_BLOOD)
        self.blood_temp = self.blood

        self.speed_x = random.choice(I_BOSS_SPLIT)
        self.speed_y = random.choice(I_BOSS_SPLIT)

        self.split_signal = 1
        self.time = random.choice(I_BOSS_SPLIT_TIME)

    def update(self, split_group):
        super().update()

        self.split_signal += 1

        if ((self.blood <= 0 or self.split_signal > self.time)
                and self.ik_signal < len(Split._get_skins()) - 1):
            if self.blood <= 0:
                temp = 2
            else:
                temp = 1
            for i in range(0, int(random.choice(I_BOSS_SPLIT_SUM) / temp)):
                split = Split()
                split.time = self.time * 0.8
                split.blood = self.blood_temp * 0.8
                split.hit = self.hit * 0.8
                split.speed_x = random.choice(I_BOSS_SPLIT) - self.speed_x
                split.speed_y = random.choice(I_BOSS_SPLIT) - self.speed_y
                split.rect.center = self.rect.center
                split.ik_signal = self.ik_signal + 1
                split.image = Split._get_skins()[split.ik_signal]
                split_group.add(split)
            self.kill()
        if self.blood <= 0 and self.ik_signal == len(Split._get_skins()) - 1:
            self.kill()


class Rail(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_4.png")

        self.blood = random.choice(I_BOSS_RAIL_BLOOD)
        self.hit = random.choice(I_BOSS_RAIL_HIT)

        self.speed_x = 0
        self.speed_y = 0
        self.way = random.choice([1, 2, 3])
        self.fire_time = 0

    def update(self, gatling_group):
        super().update()
        self.fire_time += 1
        if self.way == 1:
            if self.fire_time % I_BOSS_RAIL_CYCLE_S_1 == 0:
                for i in range(2):
                    gatling = Gatling()
                    gatling.rect.center = self.rect.center
                    speed = int(pow(self.speed_x ** 2 + self.speed_y ** 2, 0.5))
                    gatling.speed_x = self.speed_y * (-1) ** (i + 1) / speed * I_BOSS_RAIL_SPEED_S
                    gatling.speed_y = self.speed_x * (-1) ** i / speed * I_BOSS_RAIL_SPEED_S
                    gatling_group.add(gatling)
        elif self.way == 2:
            if self.fire_time % I_BOSS_RAIL_CYCLE_S_2 == 0:
                gatling = Gatling()
                gatling.rect.center = self.rect.center
                gatling.speed_x = random.randint(-I_BOSS_RAIL_SPEED_S, I_BOSS_RAIL_SPEED_S) + self.speed_x
                gatling.speed_y = random.randint(-I_BOSS_RAIL_SPEED_S, I_BOSS_RAIL_SPEED_S) + self.speed_y
                gatling_group.add(gatling)
        elif self.way == 3:
            if self.fire_time % I_BOSS_RAIL_CYCLE_S_3 == 0:
                for i in range(0, I_BOSS_RAIL_NUM_S_3):
                    gatling = Gatling()
                    gatling.rect.center = self.rect.center
                    gatling.speed_x = int(math.cos(math.pi / I_BOSS_RAIL_NUM_S_3 * 2 * i) * I_BOSS_RAIL_SPEED_S) + self.speed_x
                    gatling.speed_y = int(math.sin(math.pi / I_BOSS_RAIL_NUM_S_3 * 2 * i) * I_BOSS_RAIL_SPEED_S) + self.speed_y
                    gatling_group.add(gatling)


class Cycle(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_6.png")
        self.blood = I_BOSS_CYCLE_BLOOD
        self.hit = I_BOSS_CYCLE_HIT
        self.speed = I_BOSS_CYCLE_SPEED
        self.number = 0
        self.return_time = 0
        self.time = 0
        self.cycle_speed = 0

    def update(self, boss_group):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.return_time += 1
        if self.return_time >= I_BOSS_CYCLE_DELAY:
            for boss in boss_group:
                if self.number == boss.numbering:
                    if self.speed > 0:
                        x = self.rect.centerx - boss.rect.centerx - I_BOSS_CYCLE_R
                        y = self.rect.centery - boss.rect.centery
                        l = int(pow(x ** 2 + y ** 2, 0.5))
                        self.speed = int(l / I_BOSS_CYCLE_RETURN_SPEED)
                        if l != 0:
                            self.speed_x = -self.speed * x / l
                            self.speed_y = -self.speed * y / l
                    if self.speed <= 0:
                        self.speed_x = 0
                        self.speed_y = 0
                        self.time += 1
                        self.rect.centerx = (int(math.cos(self.time / I_BOSS_CYCLE_CYCLE_SPEED)
                                             * I_BOSS_CYCLE_R + boss.rect.centerx))
                        self.rect.centery = (int(math.sin(self.time / I_BOSS_CYCLE_CYCLE_SPEED)
                                             * I_BOSS_CYCLE_R + boss.rect.centery))

        if self.time == I_BOSS_CYCLE_TIME or self.blood <= 0:
            self.die()


class Gather(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/boll_2.png")
        self.blood = I_BOSS_GATHER_BLOOD
        self.hit = I_BOSS_GATHER_HIT
        self.return_time = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.return_time += 1
        if  self.return_time == I_BOSS_GATHER_TIME:
            x = self.rect.centerx - SCREEN_RECT.centerx
            y = self.rect.centery - SCREEN_RECT.centery
            l = int(pow(x ** 2 + y ** 2, 0.5))
            self.speed = int(l / I_BOSS_CYCLE_RETURN_SPEED)
            if l != 0:
                self.speed_x = -I_BOSS_GATHER_SPEED_R * x / l
                self.speed_y = -I_BOSS_GATHER_SPEED_R * y / l
        if self.return_time == I_BOSS_GATHER_TIME * 2 or self.blood <= 0:
            self.die()


class Shield(GameSprite):
    def __init__(self):
        super().__init__("./images/boss/shield.png")
        self.blood = 10000
        self.hit = 10000

    def update(self):
        super().update()
        self.blood = 0


