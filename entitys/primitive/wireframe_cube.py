from entitys.primitive.primitive_object import PrimitiveObject


class WireframeCube(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='wireframe_cube',
            texture='white_cube',
            name='WireframeCube',
            **kwargs
        )
