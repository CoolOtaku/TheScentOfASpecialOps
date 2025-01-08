from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import BoxCollider, color, destroy, distance, held_keys, mouse

from entitys.weapons.weapon import Weapon

class Player(FirstPersonController):
    def __init__(self, parent=None):
        super().__init__(speed=5, origin_y=0.5, parent=parent)
        self.collider = BoxCollider(self, (0, 1, 0), (1, 2, 1))
        self.cursor.texture = 'assets/textures/other/scope.png'
        self.cursor.color = color.white
        self.cursor.rotation_z = 90
        self.cursor.scale = 0.03

        self.current_weapon = Weapon(parent=self.camera_pivot)
        self.is_running = False

        self.walk_speed = 5
        self.run_speed = 8

    def update(self):
        super().update()

        if mouse.left:
            self.attack()
        elif held_keys['e']:
            self.take()

        if self.is_running != held_keys['shift']:
            self.is_running = held_keys['shift']
            self.speed = self.run_speed if self.is_running else self.walk_speed
            self.current_weapon.animation('run', self.is_running)

    def attack(self):
        if self.current_weapon.is_action() or self.is_running:
            return

        self.current_weapon.attack()

    def take(self):
        if self.current_weapon.is_action() or self.is_running:
            return

        for weapon in self.parent.weapons:
            if distance(self.position, weapon.position) < 2:
                self.current_weapon.animation('take', False)
                self.equip_weapon(weapon)
                self.parent.weapons.remove(weapon)
                break

    def equip_weapon(self, weapon):
        if not weapon:
            return

        if self.current_weapon:
            destroy(self.current_weapon)

        weapon.equip(self)
