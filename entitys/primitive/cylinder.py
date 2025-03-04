from ursina.models.procedural.cylinder import Cylinder

from entitys.primitive.primitive_object import PrimitiveObject


class UrsinaCylinder(PrimitiveObject):
    def __init__(self, segments=16, **kwargs):
        super().__init__(
            model=Cylinder(segments),
            texture='rainbow',
            name='UrsinaCylinder',
            collider='mesh',
            **kwargs
        )
