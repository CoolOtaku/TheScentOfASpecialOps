from entitys.weapons.weapon import Weapon, WeaponType

class Ak47(Weapon):
    def __init__(self, parent):
        super().__init__(
            animated_model='assets/models/weapons/ak47.glb',
            lying_model='assets/models/weapons/ak47_lying.glb',
            attack_sound='assets/sound/weapons/rifle1.wav',
            weapon_type=WeaponType.RIFLE,
            parent=parent,
            cooldown=0.1,
        )
        self.damage = 70
        self.scale_x = -abs(self.scale_x)
