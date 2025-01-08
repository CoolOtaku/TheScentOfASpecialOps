from enum import Enum

from direct.actor.Actor import Actor
from ursina import Entity, Audio, color, invoke, mouse, camera

from const import get_anim_duration

class WeaponType(Enum):
    HANDS = 0
    PISTOL = 1
    RIFLE = 2

class Weapon(Entity):
    def __init__(self, parent=camera.ui, weapon_type=WeaponType.HANDS,
                 animated_model='assets/models/players/hands.glb', lying_model=None,
                 attack_sound='assets/sound/punch.mp3',
                 cooldown=0.9, **kwargs):
        super().__init__(
            collider='mesh',
            rotation_x=180,
            rotation_z=180,
            parent=parent,
            scale=0.02,
            **kwargs
        )
        self.animated_model = animated_model
        self.lying_model = lying_model

        self.is_equipped = True if weapon_type == WeaponType.HANDS else False
        self.actor = Actor(animated_model)
        if self.is_equipped:
            self.actor.reparent_to(self)
            self.actor.loop('idle')

        self.model = lying_model

        self.weapon_type = weapon_type
        self.cooldown = cooldown
        self.on_cooldown = False
        self.damage = 10

        self.is_looping = False

        self.attack_sound = Audio(attack_sound, autoplay=False)
        self.muzzle_flash = Entity(
            parent=self,
            model='quad',
            scale=0.5,
            color=color.yellow,
            enabled=False
        )

    def equip(self, player):
        if not self.is_equipped:
            if self.model == self.lying_model:
                self.hide()

            self.model = None
            self.actor.reparent_to(self)
            self.actor.loop('idle')
            self.is_equipped = True

        # Прив'язка зброї до гравця
        player.current_weapon = self
        self.parent = player.camera_pivot

    def drop(self):
        if self.is_equipped:
            self.actor.detachNode()
            self.model = self.lying_model
            self.parent = camera.ui.parent
            self.position = camera.world_position + camera.forward * 2
            self.is_equipped = False

    def attack(self):
        if not self.is_equipped or self.on_cooldown:
            return

        self.on_cooldown = True
        self.muzzle_flash.enabled = True
        self.animation('attack', False)
        self.attack_sound.play()

        invoke(self.muzzle_flash.disable, delay=0.05)
        invoke(setattr, self, 'on_cooldown', False, delay=self.cooldown)

        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= self.damage
            mouse.hovered_entity.blink(color.red)

    def animation(self, name, is_loop):
        if self.actor.getCurrentAnim() == name and self.is_looping == is_loop:
            return

        if name == 'run' and not is_loop:
            self.is_looping = is_loop
            self.actor.loop('idle')
            return

        if is_loop:
            self.actor.loop(name)
        else:
            self.actor.play(name)
            invoke(self.actor.loop, 'idle', delay=get_anim_duration(self.actor, name))

        self.is_looping = is_loop

    def is_action(self):
        return self.actor.getCurrentAnim() != 'idle'
