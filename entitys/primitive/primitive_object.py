from ursina import Entity, Vec3, color

from const import destroy_list, destroy_entity


class PrimitiveObject(Entity):
    def __init__(self, model, texture=None, position=(0, 0.5, 0), scale=(1, 1, 1), collider='box', name="Primitive",
                 **kwargs):
        super().__init__(
            model=model,
            texture=texture,
            position=position,
            scale=scale,
            collider=collider,
            name=name,
            **kwargs
        )
        self._build_vertex_markers()

    def _build_vertex_markers(self):
        print(len(self.get_vertices()))
        for vertex in self.get_vertices():
            world_pos = Vec3(vertex) * self.scale
            Entity(model='sphere', scale=0.05, color=color.yellow, position=world_pos, parent=self)

    def get_vertices(self):
        if hasattr(self.model, 'vertices'):
            return self.model.vertices
        else:
            print(f"У моделі {self.model} нема атрибута 'vertices'")
            return []

    def select(self):
        self.collider.visible = True
        for marker in self.children:
            marker.enable()

    def dis_select(self):
        self.collider.visible = False
        for marker in self.children:
            marker.disable()

    def disable(self):
        destroy_list(self.children)
        destroy_entity(self)
