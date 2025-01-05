from entitys.weapons.weapon import Weapon

class Akm(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            model='assets/models/weapons/akm.glb',
            origin_z=5,
            rotation=(60, 15, 80),
            cooldown=0.1,
            **kwargs
        )
        self.damage = 70
