# 控制面版--这里储存这有戏的数据

# 注意：range(1, 3)只包含1，2两个数

# 游戏
I_CREAT_ENEMY_EVENT = 300  # 敌机生成周期
I_CREAT_RED_EVENT = 1000  # red生成周期
I_CREAT_BLUE_EVENT = 7500  # blue生成周期
I_CREAT_BIG_ENEMY_EVENT = 4000  # 精英生成周期
I_CREAT_PURPLE_EVENT = 10000  # purple生成周期
I_CREAT_ENEMY_EVENT_B = 2500  # boss出场时敌机生成周期
I_CREAT_BIG_ENEMY_EVENT_B = 20000  # 精英生成周期
I_CREAT_RED_EVENT_B = 10000  # RED生成周期
I_CREAT_BLUE_EVENT_B = 25000  # BLUE生成周期
I_CREAT_PURPLE_EVENT_B = 50000  # Purple生成周期
I_BLOOD = 10000  # 血条道具生成周期
I_ENERGY = 7000
I_AMMUNITION = 6000
I_BOMB = 7500  # 导弹道具生成周期
I_BOSS_POINT = 250  # 生成BOSS的分数


#                                               英雄
I_HERO_BLOOD = 10  # 血
I_HERO_ENERGY = 100  # 能量
I_HERO_HIT = 50
I_HERO_BLOOD_SPEED = 0.005  # 回血
I_HERO_BOMB = 10  # 导弹
I_HERO_MISSILE = 10  # 火箭
I_HERO_SPEED = 5  # 速度
I_POINT = 0  # 初始分数

# 普攻
I_HERO_FIRE_BLOOD = 0.1
I_HERO_FIRE_SPEED = 4
I_HERO_FIRE_HIT = 1
I_HERO_FIRE_TIME = 50  # 普攻发射时间
I_HERO_FIRE_interval = 10  # 普攻连发间隔
I_HERO_FIRE_CYCLE = 100  # 普攻发射周期

# 机枪
I_HERO_GATLING_CYCLE = 7  # 发射周期(只能为整数，数值越小，射速越快。最小为1)
I_HERO_GATLING_D = 2  # 单次发射子弹数
I_HERO_GATLING_RELOAD = 0.05  # 装填速度
I_HERO_GATLING_H = 2  # 子弹横向速度区间
I_HERO_GATLING_S_MAX = 15  # 子弹纵向速度(上限，可以为负数)
I_HERO_GATLING_S_MIN = 1  # 子弹纵向速度(下限，可以为负数)
I_HERO_GATLING_L_MAX = 15  # 子弹斜向速度(上限，可以为负数)
I_HERO_GATLING_L_MIN = 10  # 子弹斜向速度(下限，可以为负数)

# 追踪弹
I_HERO_TRACE_SPEED = 10  # 子弹追踪速度
I_HERO_TRACE_CYCLE = 50  # 追踪弹发射周期(只能为整数，数值越小，射速越快。最小为1)
I_HERO_TRACE_D = 2  # 追踪子弹单次发射子弹数
I_HERO_TRACE_RELOAD = 0.02  # 追踪子弹装填速度
I_HERO_TRACE_SPEED_H = 15  # 追踪子弹横向速度区间
I_HERO_TRACE_SPEED_MAX_S = 10  # 追踪子弹纵向速度(上限，可以为负数)
I_HERO_TRACE_SPEED_MIN_S = -1  # 追踪子弹纵向速度(下限，可以为负数)
I_HERO_TRACE_SPEED_MAX_L = 10  # 追踪子弹斜向速度(上限，可以为负数)
I_HERO_TRACE_SPEED_MIN_L = 1  # 追踪子弹斜向速度(下限，可以为负数)
I_HERO_TRACE_TIME = 20  # 子弹延迟追踪时间

I_HERO_BOMB_INTERVAL = 50  # 导弹发射间隔
I_HERO_BOMB_SPEED = 15  # 导弹速度
I_HERO_BOMB_BLOOD = 3  # 导弹血量

I_HERO_MISSILE_SPEED = 10
I_HERO_MISSILE_TIME = 5  # 延迟跟踪时间
I_HERO_MISSILE_HOT = 0.05
I_HERO_MISSILE_HIT = 10
I_HERO_MISSILE_AV = 5  # 动画播放速度(数值越小，速度越大， 最小为1)

I_HERO_LASER_SPEED = 100
I_HERO_LASER_HIT = 10.1
I_HERO_LASER_HIT_MAGNIFICATION = 3
I_HERO_LASER_FADE = 500  # 衰减系数
I_HERO_LASER_LONG = 105 * 25
I_HERO_LASER_WOOD = 0.01


#                                               敌机
I_ENEMY_BLOOD = range(1, 4)  # 血量区间
I_ENEMY_SPEED = range(1, 6)  # 速度区间
I_ENEMY_FIRE_SIGNAL = range(1, 3)  # 携带子弹的敌机占比
I_ENEMY_BULLET_SPEED = range(8, 12)  # 子弹速度
I_ENEMY_BULLET_BLOOD = 0.1
I_ENEMY_HIT = 1
I_ENEMY_BULLET_HIT = 0.5  # 子弹伤害

I_ENEMY_RED_SPEED = 25
I_ENEMY_RED_HIT = 2

I_BLUE_SPEED = range(2, 6)
I_BLUE_NUM = 48
I_BLUE_BULLET_SPEED = 10
I_BLUE_BULLET_D = 5
I_BLUE_BULLET_CYCLE = 10
I_BLUE_BULLET_HIT = 0.2
I_BLUE_BULLET_SPEED_X = range(-8, 9)
I_BLUE_BULLET_SPEED_Y = range(3, 5)


#                                               精英
I_BIG_BLOOD = range(15, 30)
I_BIG_BLOOD_SPEED = range(1, 3)
I_BIG_FIRE_SIGNAL = range(1, 3)  # 携带子弹的敌机占比
I_BIG_HIT = 2.5
I_BIG_BULLET_HIT = 2  # 子弹伤害

I_PURPLE_BLOOD = range(60, 120)
I_PURPLE_HIT = 7
I_PURPLE_SPEED = 1

#                                               boss
I_BOSS_BLOOD = 500  # 血量
I_BOSS_MOVE = 100  # 左右移动周期
I_BOSS_SPRINT = 200  # 冲刺周期
I_BOSS_SHIELD_CYCLE = 100  # 护盾
I_BOSS_SHIELD_TIME = 50

# 炸弹
I_BOSS_BOOM_CYCLE = 2000  # 炸弹发射周期
I_BOSS_BOOM_BLOOD = range(1, 2)  # 炸弹血量
I_BOSS_BOOM = range(10, 30)  # 炸弹伤害(需除10)
I_BOSS_BOOM_SPEED_X = range(-9, 10)
I_BOSS_BOOM_SPEED_Y = 8
I_BOSS_BOOM_A = 0.2  # 炸弹加速度
I_BOSS_BOOM_D = 25  # 单次发射炸弹数
I_BOSS_BOOM_RANGE = 75  # 炸弹爆炸范围

# 光球
I_BOSS_BOLL_SPEED = 10  # 光球速度
I_BOSS_BOLL_HIT = 2  # 光球伤害
I_BOSS_BOLL_BLOOD = 3  # 光球血量
I_BOSS_BOLL_CYCLE = 2000  # 光球发射周期
I_BOSS_BOLL_NUM = 24  # 一圈光球的个数
I_BOSS_BOLL_FIRE = 1  # 光球射速(数值越小，速度越大，最小为1)

# 跟踪光球
I_BOSS_TRACE_BLOOD = range(15, 25)  # 跟踪光球血量
I_BOSS_TRACE_HIT = range(5, 10)  # 跟踪光球伤害
I_BOSS_TRACE_CYCLE = 2000  # 跟踪光球发射周期
I_BOSS_TRACE_FIRE = 10  # 跟踪光球发射速度
I_BOSS_TRACE_SPEED = 3  # 光球跟踪速度
I_BOSS_TRACE_TIME = 40  # 子弹延迟追踪时间

# 火球
I_BOSS_HOT_HIT = 0.1  # 火球帧伤
I_BOSS_HOT_SPEED = 2  # 火球速度
I_BOSS_HOT_CYCLE = 1000  # 火球发射周期

# 小光求
I_BOSS_S_HIT = 0.5  # 小光球伤害
I_BOSS_S_BLOOD = 1  # 小光球血量
I_BOSS_S_SPEED = 20  # 小光球速度
I_BOSS_S_CYCLE = 2000  # 小光球发射周期
I_BOSS_S_FIRE = 1  # 小光球射速(数值越小，速度越大，最小为1)
I_BOSS_S_NUM = range(50, 150)  # 小光球发射个数

# 流星
I_BOSS_METEOR_CYCLE = 2000
I_BOSS_METEOR_SUM = 10
I_BOSS_METEOR_X = range(-2, 3)  # 流星的横向速度
I_BOSS_METEOR_Y = range(5, 10)  # 流星的纵向速度
I_BOSS_METEOR_BLOOD = range(5, 15)
I_BOSS_METEOR_HIT = range(2, 5)

# 分裂光球
I_BOSS_SPLIT_CYCLE = 2000
I_BOSS_SPLIT_SUM = range(2, 5)
I_BOSS_SPLIT = range(-5, 6)  # 分裂光球速度
I_BOSS_SPLIT_BLOOD = range(5, 10)
I_BOSS_SPLIT_HIT = range(2, 5)
I_BOSS_SPLIT_TIME = range(100, 200)  # 自动分裂时间

# 电磁光球
I_BOSS_RAIL_CYCLE = 2000
I_BOSS_RAIL_BLOOD = range(5, 10)
I_BOSS_RAIL_HIT = range(2, 5)
I_BOSS_RAIL_SPEED = range(4, 7)
I_BOSS_RAIL_SPEED_S = 5
I_BOSS_RAIL_CYCLE_S_1 = 5
I_BOSS_RAIL_CYCLE_S_2 = 5
I_BOSS_RAIL_CYCLE_S_3 = 50
I_BOSS_RAIL_NUM_S_3 = 24

# 环绕光球
I_BOSS_CYCLE_CYCLE = 750
I_BOSS_CYCLE_CYCLE_SPEED = 25  # 旋转速度(值越小，速度越大，最小为1)
I_BOSS_CYCLE_SPEED = 5
I_BOSS_CYCLE_BLOOD = 50
I_BOSS_CYCLE_HIT = 5
I_BOSS_CYCLE_R = 250  # 旋转半径
I_BOSS_CYCLE_DELAY = 50  # 回归延迟时间
I_BOSS_CYCLE_RETURN_SPEED = 25  # 回归速度(数值越小，速度越大，最小为1)
I_BOSS_CYCLE_TIME = 5000  # 旋转持续时间

# 回归光球
I_BOSS_GATHER_CYCLE = 2500
I_BOSS_GATHER_BLOOD = 5
I_BOSS_GATHER_HIT = 1
I_BOSS_GATHER_SPEED = range(15, 20)
I_BOSS_GATHER_SPEED_R = 30
I_BOSS_GATHER_TIME = 150
I_BOSS_GATHER_NUM = 20

#                                               布局常量
I_HUD_X = 0
I_HUD_Y_START = 0
I_HUD_Y_STEP = 50

I_BOSS_BAR_X = 500
I_BOSS_BAR_Y = 25
I_BOSS_BAR_W = 700
I_BOSS_BAR_H = 20
I_BOSS_BAR_Y_STEP = 30
I_BOSS_BAR_BORDER_W = 704
I_BOSS_BAR_BORDER_H = 24

I_HERO_BAR_W = 100
I_HERO_BAR_H = 2
I_HERO_BAR_Y_OFFSET = 75
I_HERO_BAR_BORDER_W = 102
I_HERO_BAR_BORDER_H = 4

I_ENERGY_BAR_Y_OFFSET = 70

I_BG_W = 479
I_BG_H = 699
# 操作
# W, S, A, D: 移动
# Q, E: 向左(右)前方
# B:血条
# 1, 2, 3: 切换武器(普通攻击, 加特林, 霰弹)
# R: 重新开始(英雄死亡时)
# T: 退出(英雄死亡或暂停时)
# P: 暂停
# L: 召唤boss
# C: 时停
# 空格: 发射子弹
# 左shift: 发射导弹
# 鼠标左键：激光
# 鼠标右键：核弹头
# 鼠标滚轮：激光颜色
