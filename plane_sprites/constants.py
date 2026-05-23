import pygame

SCREEN_RECT = pygame.Rect(0, 0, 1700, 1000)

FRAME_PER_SEC = 60

CREAT_ENEMY_EVENT = pygame.USEREVENT
CREAT_RED_EVENT = pygame.USEREVENT + 1
CREAT_BLUE_EVENT = pygame.USEREVENT + 2
BLOOD = pygame.USEREVENT + 4
BOMB = pygame.USEREVENT + 5
CREAT_BIG_ENEMY_EVENT = pygame.USEREVENT + 6
ENERGY = pygame.USEREVENT + 8
CREAT_PURPLE_EVENT = pygame.USEREVENT + 9
AMMUNITION = pygame.USEREVENT + 10

# Direction → rotation angle (pygame rotates counter-clockwise)
DIRECTION_ANGLES = {0: 0, 1: 180, 2: 90, 3: 270, 4: 45, 5: 315, 6: 135, 7: 225}
ANGLE_TO_DIR = {v: k for k, v in DIRECTION_ANGLES.items()}

_IMAGE_CACHE = {}


def get_dir_images(*image_paths):
    """Pre-load and cache images rotated for all 8 directions.
    Returns dict[direction -> list of Surfaces]."""
    key = tuple(image_paths)
    if key in _IMAGE_CACHE:
        return _IMAGE_CACHE[key]
    base_imgs = [pygame.image.load(p).convert_alpha() for p in image_paths]
    result = {}
    for d in range(8):
        angle = DIRECTION_ANGLES[d]
        if angle == 0:
            result[d] = list(base_imgs)
        else:
            result[d] = [pygame.transform.rotate(img, angle) for img in base_imgs]
    _IMAGE_CACHE[key] = result
    return result
