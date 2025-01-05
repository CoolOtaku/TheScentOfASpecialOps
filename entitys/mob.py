from ursina import Entity
from direct.actor.Actor import Actor

class Mob(Entity):
    def __init__(self, position=(10, 0, 0)):
        super().__init__(
            position=position,
            rotation=(0, 180, 0),
            scale=(1, 2, 1),
            collider='box',
        )
        self.speed = 5

        self.actor = Actor('assets/models/players/ukrainian_soldier.glb')
        self.actor.reparent_to(self)
        self.actor.loop('idle')
