from entitys.primitive.primitive_object import PrimitiveObject


class Plane(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='plane',
            texture='grass',
            position=(0, 0, 0),
            scale=(50, 1, 50),
            name='Plane',
            **kwargs
        )
