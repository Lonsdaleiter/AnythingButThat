import entity
import assets
import random
import entitymanager
import config


class Projectile(entity.Entity):

    def __init__(self, x, y, image, x_rate, y_rate, health, damage, downwards):
        # for projectiles except ion, health = 1
        super().__init__(image, x, y, health, damage)

        self.x_dir = x_rate
        self.y_dir = y_rate

        self.downwards = downwards

    def get_max_num_on_screen(self):
        raise NotImplementedError()

    def update(self):
        super().update()
        self.move(self.x_dir, self.y_dir)

    def on_collide(self, other_entity):
        self.health -= other_entity.damage
        if self.health <= 0:
            self.kill()


class Explosion(Projectile):

    def __init__(self, x, y, damage=0, image=assets.explosion):
        super().__init__(x, y, image, 0, 0, float("inf"), damage, False)
        self.count = 0

    def update(self):
        # super().update()
        self.count += 1
        if self.count > 200:
            self.kill()

    def get_max_num_on_screen(self):
        return float("inf")


class DestructiveExplosion(Explosion):

    def __init__(self, x, y):
        super().__init__(x, y, damage=20)

    def update(self):
        self.count += 1
        if self.count > 50:
            self.kill()


class Bullet(Projectile):

    def __init__(self, x, y, downwards):
        super().__init__(x, y, assets.upbullet if not downwards else assets.downbullet,
                         0, 2 if downwards else -2, 1, 3, downwards)

    def get_max_num_on_screen(self):
        return 12


class Missile(Projectile):

    def __init__(self, x, y, downwards):
        super().__init__(x, y, assets.upmissile if not downwards else assets.downmissile,
                         0, 2 if downwards else -2, 1, 1, downwards)

    def on_collide(self, other_entity):
        if type(other_entity) != entity.ConcreteEntity and (not issubclass(type(other_entity), Explosion)
                                                            and type(other_entity) != Explosion) \
                and self in entitymanager.entities:
            DestructiveExplosion(self.x, self.y)
        if not issubclass(type(other_entity), Explosion) and type(other_entity) != Explosion:
            super().on_collide(other_entity)

    def get_max_num_on_screen(self):
        return 3


class Mine(Projectile):

    def __init__(self, x, y, downwards):
        super().__init__(x, y, assets.mine, 0, 0, float("inf"), 0, downwards)

        self.time = 0
        self.cap = 100 + random.randint(0, 100)
        self.exploded = False

    def update(self):
        super().update()

        self.time += 1
        if self.time < self.cap:
            self.move(0, -2)

    def on_collide(self, other_entity):
        if self.time > self.cap and \
                        type(other_entity) != DestructiveExplosion and \
                        type(other_entity) != entity.ConcreteEntity and \
                        type(other_entity) != Explosion and \
                        not issubclass(type(other_entity), Projectile) and\
                        not self.exploded:
            DestructiveExplosion(self.x, self.y)
            self.exploded = True

        if self.exploded:
            self.kill()

    def get_max_num_on_screen(self):
        return 5


class IonBall(Explosion):

    def __init__(self, x, y):
        super().__init__(x, y, 0, image=assets.ion_ball)

        entity.ions.append(self)

    def on_collide(self, other_entity):
        if random.randint(0, 100) == 0:
            other_entity.health -= 1

    def kill(self):
        super().kill()

        entity.ions.remove(self)


class Ion(Projectile):

    def __init__(self, x, y, downwards):
        super().__init__(x, y, assets.ion_shot, 0, 2 if downwards else -2, float("inf"), 0, downwards)

        self.collision_registry = []

    def update(self):
        self.can_move = True

        self.move(self.x_dir, self.y_dir)

        if self.health <= 0:
            self.kill()

        if self.x < -self.image.get_width() or self.x > config.WIDTH or \
                self.y < -self.image.get_height() or self.y > config.HEIGHT:
            self.kill()

    def on_collide(self, other_entity):
        if other_entity not in self.collision_registry and type(other_entity) != IonBall\
                and type(other_entity) != entity.ConcreteEntity:
            self.collision_registry.append(other_entity)
            IonBall(self.x, self.y - 40)

            self.kill()

    def get_max_num_on_screen(self):
        return 2


class Laser(Projectile):  # a weapon which shoots straight instantly through ships to the top of the screen and deals 1d

    def __init__(self, x, y):
        super().__init__(x, y - assets.laser.get_height(), assets.laser, 0, 0, float("inf"), 1, False)

        self.damaged_entities = []
        self.count = 0

    def update(self):
        super().update()

        if self.count > 200:
            self.kill()
        if self.count > 50:
            self.visible = False

        self.count += 1

    def on_collide(self, other_entity):
        if other_entity not in self.damaged_entities and type(other_entity) != entity.ConcreteEntity:
            self.damaged_entities.append(other_entity)
            other_entity.health -= self.damage

    def get_max_num_on_screen(self):
        return 1
