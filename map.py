from ursina import Entity, DirectionalLight, Vec3, Sky

from entitys.drops.wall import Wall
from entitys.drops.box import Box
from entitys.mob import Mob

from entitys.weapons.ak47 import Ak47

class Map(Entity):
    def __init__(self):
        super().__init__()
        self.ground = Entity(
            model='plane',
            texture='assets/textures/maps/grass1.jpg',
            texture_scale=(555, 555),
            scale=1000,
            collider='box'
        )

        self.map_data = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        ]
        self.build_map()
        self.build_walls()

        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        Sky(texture='sky_sunset')

        self.mob = Mob()

        self.weapons = []
        self.spawn_weapons()

    def build_map(self):
        box_size = Box.default_scale[0]
        for z, row in enumerate(self.map_data):
            for x, block_type in enumerate(row):
                if block_type == 1:
                    Box(position=(x * box_size, 0, z * box_size))

    def build_walls(self):
        box_size = Box.default_scale[0]
        wall_width = Wall.default_scale[2]

        rows = len(self.map_data)
        cols = len(self.map_data[0])

        offset = wall_width / 0.5

        for x in range(-1, cols + 1):
            Wall(position=(x * box_size, 0, -offset))
            Wall(position=(x * box_size, 0, rows * box_size + offset))

        """for z in range(rows):
            Wall(position=(-offset, 0, z * box_size), rotation=(0, 90, 0))
            Wall(position=(cols * box_size + offset, 0, z * box_size), rotation=(0, 90, 0))"""

    def spawn_weapons(self):
        pistol = Ak47(parent=self)
        self.weapons.append(pistol)
