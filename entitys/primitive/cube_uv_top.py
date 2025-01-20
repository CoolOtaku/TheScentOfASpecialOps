from entitys.primitive.primitive_object import PrimitiveObject

class CubeUVTop(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube_uv_top',
            texture='rainbow',
            name='CubeUVTop',
            **kwargs
        )
