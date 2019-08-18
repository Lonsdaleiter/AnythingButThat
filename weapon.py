import projectiles


class Weapon:

    def shoot(self, x, y):
        raise NotImplementedError()

    def get_weapon(self):
        raise NotImplementedError()


class Gun(Weapon):

    def get_weapon(self):
        return projectiles.Bullet

    def shoot(self, x, y):
        return projectiles.Bullet(x, y, False)


class MissileLauncher(Weapon):

    def get_weapon(self):
        return projectiles.Missile

    def shoot(self, x, y):
        return projectiles.Missile(x, y, False)


class IonLauncher(Weapon):

    def get_weapon(self):
        return projectiles.Ion

    def shoot(self, x, y):
        return projectiles.Ion(x, y, False)


class MineLauncher(Weapon):

    def get_weapon(self):
        return projectiles.Mine

    def shoot(self, x, y):
        return projectiles.Mine(x, y, False)


class LaserLauncher(Weapon):

    def get_weapon(self):
        return projectiles.Laser

    def shoot(self, x, y):
        return projectiles.Laser(x, y)
