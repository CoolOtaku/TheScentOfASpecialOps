from entitys.primitive.primitive_object import PrimitiveObject


class Sphere(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            texture='reflection_map_3',
            collider='sphere',
            name='Sphere',
            **kwargs
        )
