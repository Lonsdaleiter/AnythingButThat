import pygame
import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


currentlyplaying = 0


def init():
    pygame.mixer.set_num_channels(300)


def play_sound(sound, extension=".wav"):
    global currentlyplaying

    if currentlyplaying > 298:
        print("too many sounds")
        return

    s = pygame.mixer.Sound(os.path.join(__location__, "res/sounds/effects/" + sound + extension))
    pygame.mixer.Channel(currentlyplaying + 1).play(s)
    currentlyplaying += 1
