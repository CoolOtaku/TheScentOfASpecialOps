from ursina import Mesh, Vec3

from entitys.primitive.primitive_object import PrimitiveObject


class Cone(PrimitiveObject):
    def __init__(self, **kwargs):
        custom_mesh = Mesh(
            vertices=[
                Vec3(0, 0.5, 0),
                Vec3(0.5, -0.5, 0.5),
                Vec3(-0.5, -0.5, 0.5),
                Vec3(-0.5, -0.5, -0.5),
                Vec3(0.5, -0.5, -0.5)
            ],
            triangles=[
                (0, 1, 2),
                (0, 2, 3),
                (0, 3, 4),
                (0, 4, 1),
                (1, 3, 2),
                (3, 1, 4)
            ],
            uvs=[
                (0.5, 1),
                (1, 0),
                (0, 0),
                (0, 1),
                (1, 1)
            ]
        )

        super().__init__(
            model=custom_mesh,
            texture='rainbow',
            name='Cone',
            **kwargs
        )
