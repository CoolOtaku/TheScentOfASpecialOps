from entitys.primitive.primitive_object import PrimitiveObject


class Circle(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='circle',
            texture='vignette',
            scale=(1, 1, 0.1),
            collider='sphere',
            name='Circle',
            **kwargs
        )
