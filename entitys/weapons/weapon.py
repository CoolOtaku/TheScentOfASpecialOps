from enum import Enum

from direct.actor.Actor import Actor
from ursina import Entity, Audio, color, invoke, mouse, SpriteSheetAnimation

from const import get_anim_duration, PATH_WEAPON_MODELS, PATH_WEAPON_SOUNDS


class WeaponType(Enum):
    HANDS = 0
    KNIFE = 1
    PISTOL = 2
    RIFLE = 3


class Weapon(Entity):
    def __init__(self, parent, weapon_id='hands', name='Hands', weapon_type=WeaponType.HANDS, cooldown=2, **kwargs):
        super().__init__(
            collider='box' if weapon_type != WeaponType.HANDS else None,
            rotation_x=180,
            rotation_z=180,
            parent=parent,
            **kwargs
        )
        self.name = name
        self.is_equipped = True if weapon_type == WeaponType.HANDS else False

        self.actor = Actor(f'{PATH_WEAPON_MODELS}{weapon_id}.glb')
        if self.is_equipped:
            self.actor.reparent_to(self)
            self.actor.loop('idle')

        self.model = f'{PATH_WEAPON_MODELS}{weapon_id}_lying.glb'
        self.scale = 0.02 if self.is_equipped else 0.05

        self.weapon_type = weapon_type
        self.cooldown = cooldown
        self.on_cooldown = False
        self.damage = 10

        self.is_looping = False

        self.draw_sound = Audio(f'{PATH_WEAPON_SOUNDS}{weapon_id}_draw.wav', autoplay=False)
        self.attack_sound = Audio(f'{PATH_WEAPON_SOUNDS}{weapon_id}_attack.wav', autoplay=False)
        self.muzzle_flash = SpriteSheetAnimation(
            texture='assets/textures/other/muzzle_flash_sprite.png',
            animations={'flash': ((0, 0), (3, 1))},
            position=(0.06, -0.06, 1),
            tileset_size=(4, 2),
            visible=False,
            scale=0.2,
            loop=False,
            fps=30,
            parent=self
        )

    def equip(self, player):
        if not self.is_equipped:
            self.collider = None
            self.model.hide()
            self.actor.reparent_to(self)
            self.animation('draw', False)
            self.draw_sound.play()
            self.position = (0, 0, 0)
            self.scale = 0.02
            if self.scale_x > 0:
                self.scale_x = -abs(self.scale_x)

            player.current_weapon = self
            player.parent.weapons.remove(self)
            self.parent = player.camera_pivot
            self.muzzle_flash.parent = self.parent
            self.is_equipped = True

    def drop(self, player):
        if self.is_equipped:
            self.collider = 'box'
            self.model.show()
            self.actor.detachNode()
            self.position = player.position - (0, 1, 0)
            self.scale = 0.05

            self.parent = player.parent
            self.muzzle_flash.parent = self.parent
            self.parent.weapons.append(self)
            self.is_equipped = False

    def attack(self):
        if not self.is_equipped or self.on_cooldown:
            return

        self.on_cooldown = True

        if self.weapon_type not in [WeaponType.HANDS, WeaponType.KNIFE]:
            self.actor.stop()

        self.animation('attack', False, self.finish_attack)

        if self.weapon_type not in [WeaponType.HANDS, WeaponType.KNIFE]:
            self.muzzle_flash.visible = True
            self.muzzle_flash.play_animation('flash')
            invoke(setattr, self.muzzle_flash, 'visible', False, delay=0.5)

        self.attack_sound.play()

        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= self.damage
            mouse.hovered_entity.blink(color.red)

        invoke(setattr, self, 'on_cooldown', False, delay=self.cooldown)

    def finish_attack(self):
        if mouse.left:
            self.attack()
        else:
            self.animation('idle', True)

    def animation(self, name, is_loop, function_after=None, *args):
        if self.actor.getCurrentAnim() == name and self.is_looping == is_loop:
            return

        if is_loop:
            self.actor.loop(name)
        else:
            self.actor.play(name)
            if function_after:
                invoke(function_after, *args, delay=get_anim_duration(self.actor, name))
            else:
                invoke(self.actor.loop, 'idle', delay=get_anim_duration(self.actor, name))

        self.is_looping = is_loop

    def is_action(self):
        return self.actor.getCurrentAnim() != 'idle'
