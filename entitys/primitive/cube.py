from entitys.primitive.primitive_object import PrimitiveObject


class Cube(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            texture='brick',
            name='Cube',
            **kwargs
        )
