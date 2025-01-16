from ursina import Entity

class Wall(Entity):
    default_scale = (2, 8, 0.5)

    def __init__(self, **kwargs):
        super().__init__(
            model='cube', texture='assets/textures/maps/stone1.jpg',
            scale=self.default_scale, origin_y=-0.5,
            texture_scale=(0.5, 4),
            collider='box', **kwargs
        )