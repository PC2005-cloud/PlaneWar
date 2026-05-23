import sys

import pygame.sprite

from plane_sprites import *

pygame.init()


class PlayGame(object):
    _music_back = None
    _music_tool = None

    @classmethod
    def _get_music_back(cls):
        if cls._music_back is None:
            cls._music_back = pygame.mixer.Sound('./music/play.mp3')
        return cls._music_back

    @classmethod
    def _get_music_tool(cls):
        if cls._music_tool is None:
            cls._music_tool = pygame.mixer.Sound('./music/getTool.wav')
            cls._music_tool.set_volume(0.2)
        return cls._music_tool

    def __init__(self):
        print("游戏初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("飞机大战 1.6 / Plane War（作者：p'c）")
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREAT_ENEMY_EVENT, I_CREAT_ENEMY_EVENT)
        pygame.time.set_timer(CREAT_RED_EVENT, I_CREAT_RED_EVENT)
        pygame.time.set_timer(CREAT_BLUE_EVENT, I_CREAT_BLUE_EVENT)
        pygame.time.set_timer(CREAT_BIG_ENEMY_EVENT, I_CREAT_BIG_ENEMY_EVENT)
        pygame.time.set_timer(CREAT_PURPLE_EVENT, I_CREAT_PURPLE_EVENT)
        pygame.time.set_timer(BLOOD, I_BLOOD)
        pygame.time.set_timer(BOMB, I_BOMB)
        pygame.time.set_timer(AMMUNITION, I_AMMUNITION)
        pygame.time.set_timer(ENERGY, I_ENERGY)
        self.boss_num = 1
        self.numbering = 0
        self.blood_signal = 0
        self.energy_signal = 0
        self.blood_time = 1
        self.energy_time = 1
        self.frame = 0
        self.time = FRAME_PER_SEC

        pygame.mixer.set_num_channels(64)

        PlayGame._get_music_back().play(-1)

        self._paused = False

    def __create_sprites(self):
        self.bg_group = pygame.sprite.Group()
        for i in range(4):
            for j in range(3):
                bg = Background(i, j)
                self.bg_group.add(bg)

        self.enemy_group = pygame.sprite.Group()
        self.red_group = pygame.sprite.Group()
        self.blue_group = pygame.sprite.Group()
        self.big_enemy_group = pygame.sprite.Group()
        self.purple_group = pygame.sprite.Group()
        self.bullet_e_group = pygame.sprite.Group()
        self.bullet_b_group = pygame.sprite.Group()
        self.explode_e_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.bullet_h_group = pygame.sprite.Group()
        self.bullet_t_group = pygame.sprite.Group()
        self.bullet_m_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.explode_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()

        self.new_game = NewGame()
        self.game_over = Quit()
        self.new_game_group = pygame.sprite.Group(self.new_game, self.game_over)
        self.resume = Resume()
        self.resume_group = pygame.sprite.Group(self.resume)

        self.mouse = Mouse()
        self.mouse_group = pygame.sprite.Group(self.mouse)

        self.blood_group = pygame.sprite.Group()
        self.energy_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.ammunition_group = pygame.sprite.Group()

        self.boss_group = pygame.sprite.Group()
        self.bullet_r_group = pygame.sprite.Group()
        self.shield_group = pygame.sprite.Group()
        self.boom_group = pygame.sprite.Group()
        self.boll_group = pygame.sprite.Group()
        self.trace_group = pygame.sprite.Group()
        self.hot_group = pygame.sprite.Group()
        self.gatling_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.split_group = pygame.sprite.Group()
        self.rail_group = pygame.sprite.Group()
        self.cycle_group = pygame.sprite.Group()
        self.gather_group = pygame.sprite.Group()

    def play(self):
        while True:
            keys = pygame.key.get_pressed()
            self.clock.tick(self.time)

            if self._paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        PlayGame.__game_over(self)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self._paused = False
                        elif event.key == pygame.K_t:
                            self.__game_over()
                if keys[pygame.K_t]:
                    self.__game_over()
                self.resume_group.update()
                self.resume_group.draw(self.screen)
                pygame.display.update()
            else:
                self.__event_handler()
                self.__check_collide()
                self.__update_sprites()
                pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlayGame.__game_over(self)
            if event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                enemy.numbering = self.numbering
                self.numbering += 10
                self.enemy_group.add(enemy)
            if event.type == CREAT_RED_EVENT and self.hero.point.point > 60:
                enemy_r = EnemyR()
                enemy_r.numbering = self.numbering
                self.numbering += 10
                self.red_group.add(enemy_r)
            if event.type == CREAT_BLUE_EVENT and self.hero.point.point > 100:
                enemy_b = EnemyB()
                enemy_b.numbering = self.numbering
                self.numbering += 10
                self.blue_group.add(enemy_b)
            if event.type == CREAT_BIG_ENEMY_EVENT and self.hero.point.point > 25:
                big_enemy = BigEnemy()
                big_enemy.numbering = self.numbering
                self.numbering += 10
                self.big_enemy_group.add(big_enemy)
            if event.type == CREAT_PURPLE_EVENT and self.hero.point.point > 150:
                enemy_p = BigEnemyP(self.hero.point.point)
                enemy_p.numbering = self.numbering
                self.numbering += 10
                self.purple_group.add(enemy_p)

            if event.type == BLOOD:
                blood = Blood()
                self.blood_group.add(blood)
            if event.type == ENERGY:
                energy = Energy()
                self.energy_group.add(energy)
            if event.type == BOMB:
                bomb = BombSupply()
                self.bomb_group.add(bomb)
            if event.type == AMMUNITION:
                ammunition = Ammunition()
                self.ammunition_group.add(ammunition)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and self.hero.blood >= 0:
                    boss = Boss(self.hero.point.point)
                    self.boss_group.add(boss)
                if event.key == pygame.K_p:
                    self._paused = True
            if event.type == pygame.MOUSEWHEEL:
                self.hero.laser_increasing *= I_HERO_LASER_HIT_MAGNIFICATION
                if event.y > 0:
                    self.hero.laser_color += 1
                elif event.y < 0:
                    self.hero.laser_color -= 1
            else:
                self.hero.laser_increasing = 1

        keys = pygame.key.get_pressed()
        q = e = w = s = a = d = 0

        self.time = FRAME_PER_SEC
        if keys[pygame.K_c]:
            self.time = FRAME_PER_SEC / 2.5

        if keys[pygame.K_w]:
            w = 1
            self.hero.rect.y -= self.hero.speed
            self.hero.direction = 0
        if keys[pygame.K_s]:
            s = 1
            self.hero.rect.y += self.hero.speed
            self.hero.direction = 1
        if keys[pygame.K_a]:
            a = 1
            self.hero.rect.x -= self.hero.speed
            self.hero.direction = 2
        if keys[pygame.K_d]:
            d = 1
            self.hero.rect.x += self.hero.speed
            self.hero.direction = 3
        if keys[pygame.K_q]:
            q = 1
        if keys[pygame.K_e]:
            e = 1

        if q == 1 or (w == 1 and a == 1):
            self.hero.direction = 4
        if e == 1 or (w == 1 and d == 1):
            self.hero.direction = 5
        if s == 1 and a == 1:
            self.hero.direction = 6
        if s == 1 and d == 1:
            self.hero.direction = 7

        if keys[pygame.K_1]:
            self.hero.point.weapons = 1
        if keys[pygame.K_2]:
            self.hero.point.weapons = 2
        if keys[pygame.K_3]:
            self.hero.point.weapons = 3

        if keys[pygame.K_SPACE] and self.hero.point.weapons == 1 and self.hero.blood >= 0:
            if self.hero.fire_signal <= 0:
                self.hero.fire_signal = I_HERO_FIRE_CYCLE
        elif keys[pygame.K_SPACE] and self.hero.point.weapons == 2 and self.hero.blood >= 0:
            if self.hero.gatling_signal <= 0:
                self.hero.gatling_signal = int(I_HERO_GATLING_CYCLE * 1000 / (1000 + self.hero.point_fire))
        elif keys[pygame.K_SPACE] and self.hero.point.weapons == 3 and self.hero.blood >= 0:
            if self.hero.trace_signal <= 0:
                self.hero.trace_signal = int(I_HERO_TRACE_CYCLE * 500 / (500 + self.hero.point_fire))
        if keys[pygame.K_LSHIFT] and self.hero.point.bomb > 0 and self.hero.blood >= 0:
            if self.hero.bomb_signal <= 0:
                self.hero.bomb_signal = I_HERO_BOMB_INTERVAL
                self.hero.point.bomb -= 1

        if keys[pygame.K_r] and self.hero.blood < 0:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()
            self.hero_group.add(self.hero)
            self.__clear_enemies()
            self.boss_num = 1
            Boss.class_number = 0

        if keys[pygame.K_t] and self.hero.point.blood < 0:
            PlayGame.__game_over(self)

        if len(self.boss_group) == 0 and self.hero.point.point >= I_BOSS_POINT * self.boss_num:
            self.boss_num += 2
            boss = Boss(self.hero.point.point)
            self.boss_group.add(boss)

        self.blood_signal += 1
        self.energy_signal += 1
        if keys[pygame.K_b]:
            self.blood_signal = 0
        if keys[pygame.K_v]:
            self.energy_signal = 0
        if self.blood_signal == 1:
            self.blood_time += 1
        if self.energy_signal == 1:
            self.energy_time += 1

        mouse_right = pygame.mouse.get_pressed()[2]
        self.hero.missile_signal += 1
        if mouse_right:
            self.hero.missile_signal = 0
        mouse_left = pygame.mouse.get_pressed()[0]

        self.hero.laser_signal = 0
        if mouse_left:
            self.hero.laser_signal = 1

    def __check_collide(self):
        list_1 = [self.enemy_group, self.bullet_e_group, self.big_enemy_group, self.bullet_b_group,
                  self.boss_group, self.boom_group, self.boll_group, self.trace_group, self.hot_group,
                  self.gatling_group, self.meteor_group, self.split_group, self.rail_group,
                  self.cycle_group, self.gather_group, self.explode_e_group, self.red_group,
                  self.blue_group, self.purple_group]
        list_2 = [self.hero_group, self.bullet_h_group, self.bullet_t_group, self.bullet_m_group,
                  self.explode_group, self.laser_group]
        for group_1 in list_1:
            for group_2 in list_2:
                self.__collided(group_1, group_2)

        self.__collided(self.bullet_r_group, self.hero_group)
        self.__collided(self.bullet_r_group, self.laser_group)

        self.__collided(self.shield_group, self.bullet_m_group)
        self.__shield(self.shield_group, self.bullet_h_group)
        self.__shield(self.shield_group, self.bullet_t_group)

        self.__trace(self.bullet_t_group, self.enemy_group, I_HERO_TRACE_SPEED)
        self.__trace(self.bullet_t_group, self.big_enemy_group, I_HERO_TRACE_SPEED)
        self.__trace(self.bullet_t_group, self.boss_group, I_HERO_TRACE_SPEED)
        self.__trace(self.bullet_t_group, self.red_group, I_HERO_TRACE_SPEED)
        self.__trace(self.bullet_t_group, self.blue_group, I_HERO_TRACE_SPEED)
        self.__trace(self.bullet_t_group, self.purple_group, I_HERO_TRACE_SPEED)

        mouse_left = pygame.mouse.get_pressed()[0]
        if pygame.sprite.collide_mask(self.mouse, self.new_game) and mouse_left:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()
            self.hero_group.add(self.hero)
            self.__clear_enemies()
            self.boss_num = 1
            Boss.class_number = 0

        if pygame.sprite.collide_mask(self.mouse, self.game_over) and mouse_left:
            self.__game_over()

        for blood in self.blood_group:
            hero_blood = pygame.sprite.collide_mask(self.hero, blood)
            if hero_blood:
                PlayGame._get_music_tool().play()
                self.hero.blood += random.randint(1, 8)
                blood.remove(self.blood_group)

        for bomb in self.bomb_group:
            hero_bomb = pygame.sprite.collide_mask(self.hero, bomb)
            if hero_bomb:
                PlayGame._get_music_tool().play()
                self.hero.point.bomb += random.randint(1, 5)
                bomb.remove(self.bomb_group)

        for energy in self.energy_group:
            hero_energy = pygame.sprite.collide_mask(self.hero, energy)
            if hero_energy:
                PlayGame._get_music_tool().play()
                self.hero.energy += ((6 - energy.image_signal) / len(Energy._get_variants()) / 2
                                     * I_HERO_ENERGY * random.randint(1, 10) / 5)
                energy.remove(self.energy_group)

        for ammunition in self.ammunition_group:
            hero_ammunition = pygame.sprite.collide_mask(self.hero, ammunition)
            if hero_ammunition:
                PlayGame._get_music_tool().play()
                self.hero.point.missile += random.randint(1, 5)
                ammunition.remove(self.ammunition_group)

    def __update_sprites(self):
        self.mouse_group.update()
        self.mouse_group.draw(self.screen)

        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.bullet_h_group.update()
        self.bullet_h_group.draw(self.screen)

        self.bullet_t_group.update()
        self.bullet_t_group.draw(self.screen)

        self.bullet_m_group.update()
        self.bullet_m_group.draw(self.screen)

        self.missile_group.update(self.explode_group)
        self.missile_group.draw(self.screen)

        self.laser_group.update()
        self.laser_group.draw(self.screen)

        self.hero_group.update(self.mouse, self.bullet_h_group, self.bullet_t_group,
                               self.bullet_m_group, self.missile_group, self.laser_group)
        self.hero_group.draw(self.screen)

        self.enemy_group.update(self.hero, self.bullet_e_group)
        self.enemy_group.draw(self.screen)

        self.red_group.update(self.hero, self.explode_e_group)
        self.red_group.draw(self.screen)

        self.blue_group.update(self.hero, self.bullet_e_group)
        self.blue_group.draw(self.screen)

        self.big_enemy_group.update(self.hero, self.bullet_b_group)
        self.big_enemy_group.draw(self.screen)

        self.purple_group.update(self.hero, self.enemy_group, self.red_group, self.blue_group,
                                 self.big_enemy_group, self.purple_group)
        self.purple_group.draw(self.screen)

        self.bullet_e_group.update()
        self.bullet_e_group.draw(self.screen)

        self.bullet_b_group.update()
        self.bullet_b_group.draw(self.screen)

        self.blood_group.update()
        self.blood_group.draw(self.screen)

        self.bomb_group.update()
        self.bomb_group.draw(self.screen)

        self.energy_group.update()
        self.energy_group.draw(self.screen)

        self.ammunition_group.update()
        self.ammunition_group.draw(self.screen)

        self.bullet_r_group.update()
        self.bullet_r_group.draw(self.screen)

        self.shield_group.update()
        self.shield_group.draw(self.screen)

        self.boom_group.update(self.bullet_h_group, self.bullet_t_group, self.bullet_m_group)
        self.boom_group.draw(self.screen)

        self.boll_group.update()
        self.boll_group.draw(self.screen)

        self.trace_group.update(self.hero)
        self.trace_group.draw(self.screen)

        self.hot_group.update()
        self.hot_group.draw(self.screen)

        self.gatling_group.update()
        self.gatling_group.draw(self.screen)

        self.meteor_group.update()
        self.meteor_group.draw(self.screen)

        self.split_group.update(self.split_group)
        self.split_group.draw(self.screen)

        self.rail_group.update(self.gatling_group)
        self.rail_group.draw(self.screen)

        self.cycle_group.update(self.boss_group)
        self.cycle_group.draw(self.screen)

        self.gather_group.update()
        self.gather_group.draw(self.screen)

        self.boss_group.update(self.hero, self.shield_group, self.boom_group, self.boll_group,
                               self.trace_group, self.hot_group, self.gatling_group, self.meteor_group,
                               self.split_group, self.rail_group, self.cycle_group, self.gather_group,
                               self.bullet_e_group)
        self.boss_group.draw(self.screen)

        if self.blood_time % 2 == 0:
            hero_rect_blood_0 = pygame.Rect(self.hero.rect.centerx - self.hero.rect.width / 2,
                                            self.hero.rect.centery - I_HERO_BAR_Y_OFFSET,
                                            I_HERO_BAR_W * self.hero.blood / self.hero.blood_max, I_HERO_BAR_H)
            hero_rect_blood_1 = pygame.Rect(self.hero.rect.centerx - self.hero.rect.width / 2 - 1,
                                            self.hero.rect.centery - I_HERO_BAR_Y_OFFSET - 1,
                                            I_HERO_BAR_BORDER_W, I_HERO_BAR_BORDER_H)
            pygame.draw.rect(self.screen, (0, 0, 0), hero_rect_blood_1)
            pygame.draw.rect(self.screen, (255, 0, 0), hero_rect_blood_0)

        if self.energy_time % 2 == 0:
            hero_rect_energy_0 = pygame.Rect(self.hero.rect.centerx - self.hero.rect.width / 2,
                                             self.hero.rect.centery - I_ENERGY_BAR_Y_OFFSET,
                                             I_HERO_BAR_W * self.hero.energy / I_HERO_ENERGY, I_HERO_BAR_H)
            hero_rect_energy_1 = pygame.Rect(self.hero.rect.centerx - self.hero.rect.width / 2 - 1,
                                             self.hero.rect.centery - I_ENERGY_BAR_Y_OFFSET - 1,
                                             I_HERO_BAR_BORDER_W, I_HERO_BAR_BORDER_H)
            pygame.draw.rect(self.screen, (0, 0, 0), hero_rect_energy_1)
            pygame.draw.rect(self.screen, (0, 255, 0), hero_rect_energy_0)

        self.explode_group.update()
        self.explode_group.draw(self.screen)

        self.explode_e_group.update()
        self.explode_e_group.draw(self.screen)

        boss_num = 0
        for boss in self.boss_group:
            if boss.blood >= boss.blood_max:
                boss.blood = boss.blood_max
            boss_rect_0 = pygame.Rect(I_BOSS_BAR_X, I_BOSS_BAR_Y + boss_num * I_BOSS_BAR_Y_STEP,
                                      I_BOSS_BAR_W, I_BOSS_BAR_H)
            boss_rect_1 = pygame.Rect(I_BOSS_BAR_X - 2, I_BOSS_BAR_Y - 2 + boss_num * I_BOSS_BAR_Y_STEP,
                                      I_BOSS_BAR_BORDER_W, I_BOSS_BAR_BORDER_H)
            boss_rect_0.width = int(boss.blood / boss.blood_max * I_BOSS_BAR_W)
            if boss.blood >= 0 and len(self.boss_group) > 0:
                pygame.draw.rect(self.screen, (0, 0, 0), boss_rect_1)
                pygame.draw.rect(self.screen, (255, 0, 0), boss_rect_0)
            boss_num += 1

        self.hero.point.generate(self.hero.blood, self.hero.energy)
        self.screen.blit(self.hero.point.image_point, (I_HUD_X, I_HUD_Y_START))
        self.screen.blit(self.hero.point.image_blood, (I_HUD_X, I_HUD_Y_START + I_HUD_Y_STEP))
        self.screen.blit(self.hero.point.image_energy, (I_HUD_X, I_HUD_Y_START + I_HUD_Y_STEP * 2))
        self.screen.blit(self.hero.point.image_bomb, (I_HUD_X, I_HUD_Y_START + I_HUD_Y_STEP * 3))
        self.screen.blit(self.hero.point.image_missile, (I_HUD_X, I_HUD_Y_START + I_HUD_Y_STEP * 4))
        self.screen.blit(self.hero.point.image_weapons, (I_HUD_X, I_HUD_Y_START + I_HUD_Y_STEP * 5))

        if len(self.hero_group) == 0:
            self.hero.rect.center = (10000, 10000)
            self.new_game_group.update()
            self.new_game_group.draw(self.screen)
            self.hero.blood_signal = 0

        if len(self.boss_group) != 0 and self.frame == 0:
            self.frame = 1
            pygame.time.set_timer(CREAT_ENEMY_EVENT, I_CREAT_ENEMY_EVENT_B)
            pygame.time.set_timer(CREAT_BIG_ENEMY_EVENT, I_CREAT_BIG_ENEMY_EVENT_B)
            pygame.time.set_timer(CREAT_RED_EVENT, I_CREAT_RED_EVENT_B)
            pygame.time.set_timer(CREAT_BLUE_EVENT, I_CREAT_BLUE_EVENT_B)
            pygame.time.set_timer(CREAT_PURPLE_EVENT, I_CREAT_PURPLE_EVENT_B)
        elif len(self.boss_group) == 0 and self.frame == 1:
            self.frame = 0
            pygame.time.set_timer(CREAT_ENEMY_EVENT, I_CREAT_ENEMY_EVENT)
            pygame.time.set_timer(CREAT_BIG_ENEMY_EVENT, I_CREAT_BIG_ENEMY_EVENT)
            pygame.time.set_timer(CREAT_RED_EVENT, I_CREAT_RED_EVENT)
            pygame.time.set_timer(CREAT_BLUE_EVENT, I_CREAT_BLUE_EVENT)
            pygame.time.set_timer(CREAT_PURPLE_EVENT, I_CREAT_PURPLE_EVENT)

    def __game_over(self):
        pygame.quit()
        sys.exit()

    def __clear_enemies(self):
        """清空所有敌方单位及子弹，用于复活/新游戏"""
        self.enemy_group.empty()
        self.red_group.empty()
        self.blue_group.empty()
        self.big_enemy_group.empty()
        self.purple_group.empty()
        self.bullet_e_group.empty()
        self.bullet_b_group.empty()
        self.bullet_r_group.empty()
        self.explode_e_group.empty()
        self.shield_group.empty()
        self.boom_group.empty()
        self.boll_group.empty()
        self.trace_group.empty()
        self.hot_group.empty()
        self.gatling_group.empty()
        self.meteor_group.empty()
        self.split_group.empty()
        self.rail_group.empty()
        self.cycle_group.empty()
        self.gather_group.empty()
        for boss in self.boss_group:
            boss.kill()
        self.boss_group.empty()

    def __trace(self, trace_group, target_group, speed):
        for target in target_group:
            for trace in trace_group:
                temp = ((trace.rect.centerx - target.rect.centerx) * (trace.rect.centerx - target.rect.centerx)
                        + (trace.rect.centery - target.rect.centery) * (trace.rect.centery - target.rect.centery))
                if temp <= trace.s:
                    trace.s = temp
                    trace.trace_target = target.numbering

                if target.numbering == trace.trace_target and trace.trace_signal >= I_HERO_TRACE_TIME:
                    x = trace.rect.centerx - target.rect.centerx
                    y = trace.rect.centery - target.rect.centery
                    l = int(pow(x ** 2 + y ** 2, 0.5))
                    if l != 0:
                        trace.speed_x = -speed * x / l
                        trace.speed_y = -speed * y / l

    def __shield(self, shield_group, bullet_group):
        for shield in shield_group:
            for bullet in bullet_group:
                if (abs(bullet.rect.centerx - shield.rect.centerx) <= 150
                        and abs(bullet.rect.centery - shield.rect.centery) <= 150):
                    collide_shield_bullet = pygame.sprite.collide_mask(bullet, shield)
                    if collide_shield_bullet:
                        bullet_r = BulletE()
                        bullet_r.rect.center = bullet.rect.center
                        bullet_r.speed_x = -bullet.speed_x
                        bullet_r.speed_y = -bullet.speed_y
                        self.bullet_r_group.add(bullet_r)
                        bullet.blood = -1

    def __collided(self, group_1, group_2):
        for unit_1 in group_1:
            for unit_2 in group_2:
                if (abs(unit_1.rect.centerx - unit_2.rect.centerx) <= unit_1.rect.width / 2 + unit_2.rect.width / 2
                        and abs(
                            unit_1.rect.centery - unit_2.rect.centery) <= unit_1.rect.height / 2 + unit_2.rect.height / 2
                        and unit_1.collided_signal == 0 and unit_2.collided_signal == 0):
                    collide = pygame.sprite.collide_mask(unit_1, unit_2)
                    if collide:
                        unit_1.blood -= unit_2.hit
                        unit_2.blood -= unit_1.hit


if __name__ == '__main__':
    game = PlayGame()

    game.play()
