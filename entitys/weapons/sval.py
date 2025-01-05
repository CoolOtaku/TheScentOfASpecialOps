from entitys.weapons.weapon import Weapon

class Sval(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            model='assets/models/weapons/sval.obj',
            texture='assets/textures/weapons/sval.jpg',
            shoot_sound='assets/sound/weapons/sval.wav',
            cooldown=0.1,
            **kwargs
        )
        self.damage = 70
