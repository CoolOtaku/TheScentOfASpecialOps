from const import PATH_HOUSES_MODELS, PATH_HOUSES_TEXTURES
from entitys.primitive.primitive_object import PrimitiveObject


class ObservationTower(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model=f'{PATH_HOUSES_MODELS}observation_tower.obj',
            texture=f'{PATH_HOUSES_TEXTURES}observation_tower.jpg',
            position=(0, -1.34, 0),
            scale=2,
            name='ObservationTower',
            **kwargs
        )
