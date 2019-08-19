import pygame
import os
import config


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def init():
    pygame.mixer.set_num_channels(100)


def play_sound(sound, extension=".wav"):
    if not config.SOUND_ON:
        return

    s = pygame.mixer.Sound(os.path.join(__location__, "res/sounds/effects/" + sound + extension))
    pygame.mixer.find_channel().play(s)
