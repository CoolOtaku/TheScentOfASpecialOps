from ursina import Entity

class Wall(Entity):
    default_scale = (2, 8, 0.5)

    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0)):
        super().__init__(
            model='cube', texture='assets/textures/maps/stone1.jpg',
            scale=self.default_scale, position=position, origin_y=-0.5,
            texture_scale=(0.5, 4), rotation=rotation,
            collider='box'
        )