import pygame


keys = []


def update():
    global keys

    keys = pygame.key.get_pressed()


def is_key_down(key):
    global keys

    return keys[key]
