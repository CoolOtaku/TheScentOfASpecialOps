from ursina.models.procedural.grid import Grid

from entitys.primitive.primitive_object import PrimitiveObject


class UrsinaGrid(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model=Grid(2, 6),
            texture='brick',
            name='UrsinaGrid',
            **kwargs
        )
