import pygame


def load_image(path):
    return pygame.image.load("res/textures/" + path + ".png")


def scale_image(image, x, y):
    return pygame.transform.scale(image, (x, y))


background_image = scale_image(load_image("background"), 750, 750)
player_spaceship = scale_image(load_image("playerspaceship"), 33, 96)
player_spaceship_left = scale_image(load_image("playerspaceshipleft"), 33, 96)
player_spaceship_right = scale_image(load_image("playerspaceshipright"), 33, 96)
player_spaceship_both = scale_image(load_image("playerspaceshipboth"), 33, 96)
enemy_spaceship = scale_image(load_image("enemyspaceship"), 22, 64)
upbullet = load_image("upbullet")
downbullet = load_image("downbullet")
explosion = load_image("explosion")
downmissile = load_image("downmissile")
upmissile = load_image("upmissile")
ion_ball = load_image("ion")
ion_shot = load_image("ionshot")
mine = load_image("mine")
