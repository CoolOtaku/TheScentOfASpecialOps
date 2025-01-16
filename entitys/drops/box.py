from ursina import Entity

class Box(Entity):
    default_scale = (2, 2, 2)

    def __init__(self, **kwargs):
        super().__init__(
            model='cube', texture='assets/textures/maps/box.jpg',
            scale=self.default_scale, origin_y=-0.5,
            collider='box', **kwargs
        )
