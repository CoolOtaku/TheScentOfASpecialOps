from const import PATH_HOUSES_MODELS
from entitys.primitive.primitive_object import PrimitiveObject


class ThreeFloors(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model=f'{PATH_HOUSES_MODELS}three_floors.glb',
            position=(0, 2.7, 0),
            scale=3,
            name='ThreeFloors',
            **kwargs
        )
