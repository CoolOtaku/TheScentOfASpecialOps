from entitys.weapons.weapon import Weapon, WeaponType

class Ak47(Weapon):
    def __init__(self, parent):
        super().__init__(
            weapon_id='ak47',
            name='AK-47',
            weapon_type=WeaponType.RIFLE,
            parent=parent,
            cooldown=0.1,
        )
        self.damage = 70
        self.scale_x = -abs(self.scale_x)
