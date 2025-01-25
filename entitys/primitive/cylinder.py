from ursina import Mesh, Vec3

from math import pi, sin, cos

from entitys.primitive.primitive_object import PrimitiveObject


class Cylinder(PrimitiveObject):
    def __init__(self, segments=16, **kwargs):
        vertices = [Vec3(0, 0.5, 0)]
        lower_vertices = [Vec3(0, -0.5, 0)]

        uvs = [(0.5, 0.5)]
        lower_uvs = [(0.5, 0.5)]

        for i in range(segments):
            angle = 2 * pi * i / segments
            x = cos(angle) * 0.5
            z = sin(angle) * 0.5

            upper_vertex = Vec3(x, 0.5, z)
            lower_vertex = Vec3(x, -0.5, z)

            vertices.append(upper_vertex)
            lower_vertices.append(lower_vertex)

            uv_x = (x + 1) / 2
            uv_z = (z + 1) / 2
            uvs.append((uv_x, uv_z))
            lower_uvs.append((uv_x, uv_z))

        vertices.extend(lower_vertices[1:])
        uvs.extend(lower_uvs[1:])

        triangles = []

        for i in range(1, segments + 1):
            next_index = i + 1 if i < segments else 1
            triangles.append((0, i, next_index))

        center_lower_index = segments + 1
        for i in range(segments + 1, 2 * segments + 1):
            next_index = i + 1 if i < 2 * segments else segments + 1
            triangles.append((center_lower_index, next_index, i))

        for i in range(1, segments + 1):
            next_index = i + 1 if i < segments else 1
            lower_current = i + segments
            lower_next = next_index + segments

            triangles.append((i, lower_current, lower_next))
            triangles.append((i, lower_next, next_index))

        custom_mesh = Mesh(
            vertices=vertices,
            triangles=triangles,
            uvs=uvs[:len(vertices)]
        )

        super().__init__(
            model=custom_mesh,
            texture='rainbow',
            name='Cylinder',
            **kwargs
        )
