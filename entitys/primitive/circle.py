from entitys.primitive.primitive_object import PrimitiveObject


class Circle(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='circle',
            texture='vignette',
            position=(0, 0.5, 0),
            scale=(1, 1, 0.1),
            name='Circle',
            **kwargs
        )
