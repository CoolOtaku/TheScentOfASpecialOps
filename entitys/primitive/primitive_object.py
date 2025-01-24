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
            color=color.white,
            **kwargs
        )
        self.default_collider = collider
        self._build_vertex_markers()

    def select(self):
        self.collider.visible = True
        self.color = color.violet

    def dis_select(self):
        self.collider.visible = False
        self.color = color.white

    def enable_collider(self):
        self.collider = self.default_collider

    def disable_collider(self):
        self.collider = None

    def _build_vertex_markers(self):
        for vertex in self.get_vertices():
            world_pos = Vec3(vertex) * self.scale
            Entity(model='sphere', scale=0.05, color=color.yellow, position=world_pos, collider='box', enabled=False,
                   parent=self)

    def get_vertices(self):
        return self.model.vertices if hasattr(self.model, 'vertices') else []

    def show_vertices(self):
        for marker in self.children:
            marker.enable()

    def hide_vertices(self):
        for marker in self.children:
            marker.disable()

    def disable(self):
        destroy_list(self.children)
        destroy_entity(self)
