from entitys.primitive.primitive_object import PrimitiveObject


class WireframeCube(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='wireframe_cube',
            texture='white_cube',
            position=(0, 0.5, 0),
            scale=(1, 1, 1),
            name='WireframeCube',
            **kwargs
        )
