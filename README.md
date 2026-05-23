# PlaneWar ✈️ 飞机大战

一个基于 Pygame 的 Python 飞机大战游戏。这是我初学 Python 时的第一个项目，现在进行了全面优化。

## 快速开始

```bash
# 安装依赖
uv sync
# 或 pip install -r requirements.txt

# 运行游戏
uv run python plane_main.py
```

## 操作说明

| 按键 | 功能 |
|------|------|
| W/A/S/D | 移动 |
| Q/E | 向左/右前斜向移动 |
| 空格 | 射击（配合 1/2/3 切换武器） |
| 左 Shift | 发射导弹 |
| 鼠标左键 | 激光 |
| 鼠标右键 | 核弹 |
| 鼠标滚轮 | 切换激光颜色 |
| B | 显示血量 |
| 1/2/3 | 切换武器（普通/加特林/追踪弹） |
| P | 暂停 |
| L | 召唤 Boss |
| C | 慢动作 |
| R | 复活 |
| T | 退出 |

## 技术优化

- **图片目录重组**：将 200+ 散落的 PNG 按类别（背景/敌机/英雄/Boss/子弹/道具/UI/爆炸/激光）归入子目录
- **激光图片压缩**：28 张彩色激光 PNG → 4 张白底基图 + 运行时 `BLEND_RGB_MULT` 染色，缩减 85%
- **冗余清理**：删除 73 个未引用文件（hero 8 方向预旋转变体、Boss 毁灭帧等）
- **类级缓存**：爆炸帧、受击帧等通过类级懒加载共享，避免重复读取磁盘
- **旋转缓存**：8 方向图片通过 `get_dir_images()` 预旋转并缓存，消除每帧 `pygame.transform.rotate()` 调用

## 项目结构

```
plane_main.py          # 主游戏循环、碰撞检测
plane_sprites/
├── __init__.py
├── base.py            # GameSprite 基类、Background
├── hero.py            # 英雄、子弹、炸弹、导弹、激光
├── enemies.py         # 敌机、精英敌机、紫色追踪敌机
├── boss.py            # Boss + 11 种攻击模式
├── items.py           # 道具掉落、HUD
├── ui.py              # 菜单界面
├── constants.py       # 常量、图片缓存工具
└── game_config.py     # 游戏数值配置
images/                # 分类后的图片资源
music/                 # 音效资源
```
