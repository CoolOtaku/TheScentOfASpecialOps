from ursina import color

from const import destroy_entity


class EditorObjectManager:
    def __init__(self, parent):
        self.parent = parent

        self.selected_object = None
        self.objects = []

    def create_object(self, obj_class, **kwargs):
        obj = obj_class(parent=self.parent, **kwargs)
        self.objects.append(obj)
        self.select_object(obj)

    def select_object(self, obj):
        self.dis_select_object()
        self.selected_object = obj
        self.selected_object.select()

    def dis_select_object(self):
        if self.selected_object:
            self.selected_object.dis_select()
            self.selected_object = None

    def select_vertex(self, vertex_marker):
        print(vertex_marker.position)

    def remove_object(self):
        if self.selected_object in self.objects:
            self.objects.remove(self.selected_object)
            destroy_entity(self.selected_object)
            self.dis_select_object()
