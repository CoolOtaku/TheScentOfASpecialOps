from ursina import Mesh, Vec3

from entitys.primitive.primitive_object import PrimitiveObject


class CustomCube(PrimitiveObject):
    def __init__(self, **kwargs):
        custom_mesh = Mesh(
            vertices=[
                Vec3(-0.5, -0.5, -0.5),
                Vec3(0.5, -0.5, -0.5),
                Vec3(0.5, 0.5, -0.5),
                Vec3(-0.5, 0.5, -0.5),
                Vec3(-0.5, -0.5, 0.5),
                Vec3(0.5, -0.5, 0.5),
                Vec3(0.5, 0.5, 0.5),
                Vec3(-0.5, 0.5, 0.5)
            ],
            triangles=[
                (0, 1, 2), (2, 3, 0),
                (4, 7, 6), (6, 5, 4),
                (0, 4, 5), (5, 1, 0),
                (7, 3, 2), (2, 6, 7),
                (1, 5, 6), (6, 2, 1),
                (0, 3, 7), (7, 4, 0)
            ],
            uvs=[
                (0, 0),
                (1, 0),
                (1, 1),
                (0, 1),
                (0, 0),
                (1, 0),
                (1, 1),
                (0, 1)
            ]
        )

        super().__init__(
            model=custom_mesh,
            texture='brick',
            name='CustomCube',
            collider='mesh',
            **kwargs
        )
