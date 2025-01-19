from entitys.primitive.primitive_object import PrimitiveObject


class Sphere(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            texture='reflection_map_3',
            position=(0, 0.5, 0),
            scale=(1, 1, 1),
            name='Sphere',
            **kwargs
        )
