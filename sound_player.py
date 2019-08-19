import pygame
import os
import random
import config


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
last_music = 0


def init():
    pygame.mixer.set_num_channels(100)


def m(num):
    global last_music

    last_music = num
    pygame.mixer.music.load("res/sounds/music/music" + str(num) + ".wav")
    pygame.mixer.music.play()


def music():
    global last_music

    if not config.MUSIC_ON:
        return

    k = random.randint(0, 6)
    while k == last_music:
        k = random.randint(0, 6)
    m(k)


def play_sound(sound, extension=".wav"):
    if not config.SOUND_EFFECTS_ON:
        return

    s = pygame.mixer.Sound(os.path.join(__location__, "res/sounds/effects/" + sound + extension))
    pygame.mixer.find_channel().play(s)
