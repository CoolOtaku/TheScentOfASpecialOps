from entitys.primitive.primitive_object import PrimitiveObject


class Diamond(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='diamond',
            texture='noise',
            collider='mesh',
            name='Diamond',
            **kwargs
        )