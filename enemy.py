import entity
import assets
import random
import config
import scorekeeper
import projectiles


enemies = []


def update():
    global enemies

    if random.randint(0, 90) == 0:
        Enemy(random.randint(0, config.WIDTH - 15), 0, 7)

    for enemy in enemies:
        for otherenemy in enemies:
            if enemy is not otherenemy and enemy.rect.colliderect(otherenemy):
                otherenemy.kill()


class Enemy(entity.Entity):

    def __init__(self, x, y, health):
        super().__init__(assets.enemy_spaceship, x, y, health, 100)

        enemies.append(self)

        self.bullet_chance = 60
        self.count = 0

    def kill(self, player_launched=False):
        super().kill()
        if player_launched:
            scorekeeper.points += 1
            scorekeeper.cumulated += 1
        if self in enemies:
            enemies.remove(self)
            projectiles.Explosion(self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2)

    def update(self):
        super().update()

        self.count += 1

        self.move(0, 1)

        if random.randint(0, self.bullet_chance) == 0 and self.count > 120:
            self.count = 0
            projectiles.Bullet(self.x + self.image.get_width() / 2, self.y + self.image.get_height(), True)

    def on_collide(self, other_entity):
        if issubclass(type(other_entity), projectiles.Projectile) and not other_entity.downwards:
            self.health -= other_entity.damage
        if self.health <= 0:
            self.kill(player_launched=True)
