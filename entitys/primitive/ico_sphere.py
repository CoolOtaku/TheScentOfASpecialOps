from entitys.primitive.primitive_object import PrimitiveObject


class IcoSphere(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='icosphere',
            texture='noise',
            position=(0, 1, 0),
            collider='sphere',
            name='IcoSphere',
            **kwargs
        )