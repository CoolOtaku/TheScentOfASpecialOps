from ursina.models.procedural.cone import Cone

from entitys.primitive.primitive_object import PrimitiveObject


class UrsinaCone(PrimitiveObject):
    def __init__(self, **kwargs):
        super().__init__(
            model=Cone(3),
            position=(0, 0, 0),
            texture='rainbow',
            name='Cone',
            collider='mesh',
            **kwargs
        )
