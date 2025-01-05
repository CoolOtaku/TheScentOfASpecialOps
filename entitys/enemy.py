from ursina import *

class Enemy(Entity):
    def __init__(self, player, shootables_parent, **kwargs):
        super().__init__(
            parent=shootables_parent,
            model='cube',
            scale_y=2,
            origin_y=-.5,
            color=color.light_gray,
            collider='box',
            **kwargs
        )
        self.player = player
        self.health_bar = Entity(
            parent=self,
            y=1.2,
            model='cube',
            color=color.red,
            world_scale=(1.5, .1, .1)
        )
        self.max_hp = 100
        self.hp = self.max_hp
        self._hp = self.max_hp

    def update(self):
        dist = distance_xz(self.player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(self.player.position, 'y')
        hit_info = raycast(
            self.world_position + Vec3(0, 1, 0),
            self.forward,
            30,
            ignore=(self,)
        )
        if hit_info.entity == self.player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            self.die()
        else:
            self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
            self.health_bar.alpha = 1

    def die(self):
        destroy(self)
