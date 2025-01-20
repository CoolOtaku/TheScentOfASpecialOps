from entitys.primitive.primitive_object import PrimitiveObject


class Quad(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='quad',
            texture='brick',
            scale=(1, 1, 0.1),
            name='Quad',
            **kwargs
        )
