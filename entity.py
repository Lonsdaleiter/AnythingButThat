import pygame
import config
import entitymanager


ions = []


class Entity(pygame.sprite.Sprite):

    def __init__(self, image, x, y, health, damage):
        super().__init__()

        self.image = image
        self.x = x
        self.y = y

        self.health = health

        self.damage = damage

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        self.can_move = True

        self.visible = True

        entitymanager.entities.append(self)

    def move(self, dx, dy):
        if not self.can_move:
            return
        self.set_pos(self.x + dx, self.y + dy)

    def set_pos(self, x, y):
        if not self.can_move:
            return
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def kill(self):
        if self in entitymanager.entities:
            entitymanager.entities.remove(self)

    def on_collide(self, other_entity):
        raise NotImplementedError()

    def update(self):
        k = True

        for ion in ions:
            if ion.rect.colliderect(self.rect):
                k = False
                break

        self.can_move = k

        if self.health <= 0:
            self.kill()

        if self.x < -self.image.get_width() or self.x > config.WIDTH or \
                self.y < -self.image.get_height() or self.y > config.HEIGHT:
            self.kill()


class ConcreteEntity(Entity):

    def __init__(self, image, x, y, health):
        super().__init__(image, x, y, health, 0)

    def on_collide(self, other_entity):
        pass

    def update(self):
        pass
