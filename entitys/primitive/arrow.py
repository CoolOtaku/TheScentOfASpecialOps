from entitys.primitive.primitive_object import PrimitiveObject


class Arrow(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='arrow',
            texture='arrow',
            name='Arrow',
            **kwargs
        )
