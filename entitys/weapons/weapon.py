from enum import Enum

from ursina import Entity, BoxCollider, camera, color, invoke, mouse, Audio

class WeaponType(Enum):
    PISTOL = 0
    RIFLE = 1

class Weapon(Entity):
    def __init__(self, parent=camera, weapon_type=WeaponType.RIFLE,
                 position=(0, 0, 0), origin=(-0.1, 0.9, -5), scale=2.5, rotation=(240, 15, 100),
                 cooldown=0.9, shoot_sound='assets/sound/weapons/rifle1.wav', **kwargs):
        super().__init__(
            parent=parent,
            position=position,
            origin=origin,
            scale=scale,
            rotation=rotation,
            **kwargs
        )
        self.muzzle_flash = Entity(
            parent=self,
            model='quad',
            z=1,
            world_scale=0.5,
            color=color.yellow,
            enabled=False
        )
        self.pickup_collider = BoxCollider(self, size=(1, 1, 1))
        self.weapon_type = weapon_type
        self.cooldown = cooldown
        self.on_cooldown = False
        self.damage = 100

        self.shoot_sound = Audio(shoot_sound, autoplay=False)

    def shoot(self):
        if not self.on_cooldown:
            self.on_cooldown = True
            self.muzzle_flash.enabled = True

            self.shoot_sound.play()

            invoke(self.muzzle_flash.disable, delay=0.05)
            invoke(setattr, self, 'on_cooldown', False, delay=self.cooldown)

            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= self.damage
                mouse.hovered_entity.blink(color.red)
