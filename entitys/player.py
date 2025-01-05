from direct.task import Task
from direct.actor.Actor import Actor
from direct.task.TaskManagerGlobal import taskMgr
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import BoxCollider, Entity, color, destroy, distance, held_keys

from entitys.weapons.weapon import WeaponType
from const import get_anim_duration

class Player(FirstPersonController):
    def __init__(self, parent=None):
        super().__init__(speed=4, origin_y=0.5, parent=parent)
        self.collider = BoxCollider(self, (0, 1, 0), (1, 2, 1))
        self.cursor.texture = 'assets/textures/other/scope.png'
        self.cursor.color = color.white
        self.cursor.rotation_z = 90
        self.cursor.scale = 0.03

        self.hands = Entity(
            parent=self.camera_pivot,
            scale=(1.5, 2.5, 1.5)
        )
        self.actor = Actor('assets/models/players/hands.glb')
        self.actor.reparent_to(self.hands)
        self.actor.loop('idle')

        self.current_weapon = None
        self.is_action = False
        self.is_running = False

        self.walk_speed = 4
        self.run_speed = 8

    def update(self):
        super().update()
        if held_keys['left mouse']:
            self.attack()
        elif held_keys['e']:
            self.take()

        if self.is_running != held_keys['shift']:
            self.is_running = held_keys['shift']
            self.actor.loop(
                'run_with_weapon' if self.current_weapon else 'run') if self.is_running else self.return_to_idle('run')
            self.speed = self.run_speed if self.is_running else self.walk_speed

    def equip_weapon(self, weapon):
        if not weapon:
            return

        if self.current_weapon:
            destroy(self.current_weapon)

        weapon.parent = self.actor.exposeJoint(None, 'modelRoot', 'mixamorig:RightHand')
        self.current_weapon = weapon

    def attack(self):
        if self.is_action or self.is_running:
            return

        self.is_action = True
        if self.current_weapon:
            self.current_weapon.shoot()
            self.is_action = False
        else:
            self.actor.play('punch')
            taskMgr.doMethodLater(get_anim_duration(self.actor, 'punch'), self.return_to_idle, 'punch')

    def take(self):
        if self.is_action:
            return

        self.is_action = True
        if self.current_weapon:
            self.actor.play('take_with_weapon')
        else:
            self.actor.play('take')

        for weapon in self.parent.weapons:
            if distance(self.position, weapon.position) < 2:
                self.equip_weapon(weapon)
                self.parent.weapons.remove(weapon)
                break

        taskMgr.doMethodLater(get_anim_duration(self.actor, 'take'), self.return_to_idle, 'take')

    def return_to_idle(self, anim_name):
        if self.is_running:
            return Task.done

        if not self.current_weapon:
            self.actor.loop('idle')
            self.is_action = False
            return Task.done

        match self.current_weapon.weapon_type:
            case WeaponType.PISTOL:
                self.actor.loop('idle_pistol')
            case WeaponType.RIFLE:
                self.actor.loop('idle_rifle')
            case _:
                self.actor.loop('idle')

        self.is_action = False
        return Task.done
