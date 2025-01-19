from entitys.primitive.primitive_object import PrimitiveObject


class Cube(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            texture='brick',
            position=(0, 0.5, 0),
            scale=(1, 1, 1),
            name='Cube',
            **kwargs
        )
