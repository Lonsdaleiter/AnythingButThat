import entity
import keyboard
import entitymanager
import pygame
import config
import weapon
import assets
import projectiles


class Player(entity.Entity):

    def __init__(self, x, health):
        super().__init__(assets.player_spaceship, x, 650, health, 100)  # kills anything touching it to destroy bullets

        self.time_since_last_fire = 0

        self.projs = []
        self.weapons = [weapon.weapons[0], weapon.weapons[1], weapon.weapons[2], weapon.weapons[3],
                        weapon.weapons[4], weapon.weapons[5], weapon.weapons[6]]
        self.current_weapon = 0

        self.count = 0

    def kill(self, player_launched=False):
        super().kill()
        projectiles.Explosion(self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2)

    def update(self):
        if self.x < -self.image.get_width():
            self.x = config.WIDTH
        if self.x > config.WIDTH:
            self.x = -self.image.get_width()

        super().update()

        if keyboard.is_key_down(pygame.K_LEFT) and keyboard.is_key_down(pygame.K_RIGHT):
            self.image = assets.player_spaceship_both
        elif keyboard.is_key_down(pygame.K_LEFT):
            self.move(-3, 0)
            self.image = assets.player_spaceship_left
        elif keyboard.is_key_down(pygame.K_RIGHT):
            self.move(3, 0)
            self.image = assets.player_spaceship_right
        else:
            self.image = assets.player_spaceship

        self.time_since_last_fire += 1

        for proj in self.projs:
            if proj not in entitymanager.entities:
                self.projs.remove(proj)

        if keyboard.is_key_down(pygame.K_e) and self.count > 30:
            self.current_weapon += 1
            if self.current_weapon >= len(self.weapons):
                self.current_weapon = 0
            self.count = 0

        self.count += 1

        times = 0

        for proj in self.projs:
            times += 1 if type(proj) == self.weapons[self.current_weapon].get_weapon() else 0

        if keyboard.is_key_down(pygame.K_SPACE) and self.time_since_last_fire > 30\
                and times < self.weapons[self.current_weapon].get_weapon().get_max_num_on_screen(None):
            self.time_since_last_fire = 0
            firing_x = self.image.get_width() / 2 + self.x
            firing_y = self.y - 25
            self.projs.append(self.weapons[self.current_weapon].shoot(firing_x, firing_y))

    def on_collide(self, other_entity):
        self.health -= other_entity.damage
