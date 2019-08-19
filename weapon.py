import projectiles
import sound_player


class Weapon:

    def __init__(self, cost, name):
        self.cost = cost
        self.name = name

    def shoot(self, x, y):
        raise NotImplementedError()

    def get_weapon(self):
        raise NotImplementedError()


class Gun(Weapon):

    def __init__(self):
        super().__init__(0, "Space Blaster")

    def get_weapon(self):
        return projectiles.Bullet

    def shoot(self, x, y):
        return projectiles.Bullet(x, y, False)


class MissileLauncher(Weapon):

    def __init__(self):
        super().__init__(25, "Missile Launcher")

    def get_weapon(self):
        return projectiles.Missile

    def shoot(self, x, y):
        return projectiles.Missile(x, y, False)


class IonLauncher(Weapon):

    def __init__(self):
        super().__init__(35, "Ion Cannon")

    def get_weapon(self):
        return projectiles.Ion

    def shoot(self, x, y):
        return projectiles.Ion(x, y, False)


class MineLauncher(Weapon):

    def __init__(self):
        super().__init__(40, "Mine Layer")

    def get_weapon(self):
        return projectiles.Mine

    def shoot(self, x, y):
        return projectiles.Mine(x, y, False)


class LaserLauncher(Weapon):

    def __init__(self):
        super().__init__(30, "Laser Gun")

    def get_weapon(self):
        return projectiles.Laser

    def shoot(self, x, y):
        return projectiles.Laser(x, y)


class PlasmaLauncher(Weapon):

    def __init__(self):
        super().__init__(35, "Plasma Dispatcher")

    def get_weapon(self):
        return projectiles.PlasmaCloud

    def shoot(self, x, y):
        return projectiles.PlasmaCloud(x, y, False)


class DrDevice(Weapon):

    def __init__(self):
        super().__init__(60, "Dr. Device")

    def get_weapon(self):
        return projectiles.DestructoBullet

    def shoot(self, x, y):
        return projectiles.DestructoBullet(x, y, False)


weapons = [Gun(), MissileLauncher(), IonLauncher(), MineLauncher(), LaserLauncher(), PlasmaLauncher(), DrDevice()]
