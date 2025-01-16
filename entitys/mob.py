from ursina import Entity
from direct.actor.Actor import Actor

class Mob(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            rotation=(0, 180, 0),
            scale=(1, 2, 1),
            collider='box',
            **kwargs
        )
        self.speed = 5

        self.actor = Actor('assets/models/players/ukrainian_soldier.glb')
        self.actor.reparent_to(self)
        self.actor.loop('idle')
