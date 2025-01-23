from entitys.primitive.primitive_object import PrimitiveObject


class SkyDome(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='sky_dome',
            position=(0, 1, 0),
            texture='sky_sunset',
            collider='sphere',
            name='SkyDome',
            **kwargs
        )
