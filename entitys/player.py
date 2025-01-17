from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import BoxCollider, color, destroy, distance, held_keys, mouse

from entitys.weapons.weapon import Weapon, WeaponType


class Player(FirstPersonController):
    def __init__(self, parent):
        super().__init__(speed=10, origin_y=0.5, parent=parent)
        self.collider = BoxCollider(self, (0, 1, 0), (1, 2, 1))
        self.cursor.texture = 'assets/textures/other/scope.png'
        self.cursor.color = color.white
        self.cursor.rotation_z = 90
        self.cursor.scale = 0.03

        self.hands = Weapon(parent=self.camera_pivot)
        self.current_weapon = self.hands

        self.is_running = False
        self.walk_speed = 10
        self.run_speed = 15

    def update(self):
        super().update()

        if mouse.left:
            self.attack()
        if held_keys['e']:
            self.take()
        elif held_keys['g']:
            self.drop_weapon()

        if self.current_weapon.on_cooldown:
            return

        if self.is_running != held_keys['shift']:
            self.is_running = held_keys['shift']
            self.speed = self.run_speed if self.is_running else self.walk_speed
            self.current_weapon.animation('run', self.is_running) if self.is_running else self.current_weapon.animation(
                'idle', True)

    def attack(self):
        if self.is_running:
            return

        self.current_weapon.attack()

    def take(self):
        if self.current_weapon.is_action() or self.is_running:
            return

        for weapon in self.parent.weapons:
            if distance(self.position, weapon.position) < 2:
                self.current_weapon.animation('take', False, self.equip_weapon, weapon)
                break

    def equip_weapon(self, weapon):
        if not weapon:
            return

        if self.current_weapon:
            self.hands.hide() if self.current_weapon.weapon_type == WeaponType.HANDS else destroy(self.current_weapon)

        weapon.equip(self)

    def drop_weapon(self):
        if self.current_weapon.is_action() or self.is_running:
            return

        self.current_weapon.drop(self)
        self.current_weapon = self.hands
        self.hands.equip(self)
        self.hands.animation('take', False)
        self.hands.show()
