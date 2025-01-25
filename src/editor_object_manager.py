from ursina import Vec3, color

from const import validate_input_entity_property, destroy_entity


class EditorObjectManager:
    def __init__(self, parent):
        self.parent = parent
        self.editing_vertices = False

        self.selected_object = None
        self.objects = []
        self.selected_vertex = None

    def create_object(self, obj_class, **kwargs):
        obj = obj_class(parent=self.parent, **kwargs)
        self.objects.append(obj)
        self._select_object(obj)

    def select(self, obj):
        if self.editing_vertices and self.selected_object:
            self.selected_object.disable_collider()
            self._select_vertex(obj)
        elif not self.editing_vertices:
            if self.selected_object:
                self.selected_object.enable_collider()
            self._select_object(obj)

    def _select_object(self, obj):
        self._dis_select_object()
        self.selected_object = obj
        self.selected_object.select()

    def _dis_select_object(self):
        if self.selected_object:
            self.selected_object.dis_select()
            self.selected_object = None

    def _select_vertex(self, vertex_marker):
        self._dis_select_vertex()
        if vertex_marker.parent == self.selected_object:
            self.selected_vertex = vertex_marker
            self.selected_vertex.color = color.violet

    def _dis_select_vertex(self):
        if self.selected_vertex:
            self.selected_vertex.color = color.yellow
            self.selected_vertex = None

    def on_editing_vertices(self):
        self.editing_vertices = not self.editing_vertices
        if self.editing_vertices:
            self.selected_object.show_vertices()
        else:
            self.selected_object.hide_vertices()
            self._dis_select_vertex()

    def update_attribute(self, attribute, axis, value):
        obj = self.selected_object
        if self.selected_vertex and self.editing_vertices:
            obj = self.selected_vertex

        if self.selected_object:
            attr = list(getattr(obj, attribute))
            if axis == 'x':
                attr[0] += value
            elif axis == 'y':
                attr[1] += value
            elif axis == 'z':
                attr[2] += value
            setattr(obj, attribute, tuple(attr))

            if obj == self.selected_vertex:
                self.selected_object.update_vertex_position(obj.vertex_index, obj.position)

    def validate_and_update_transform(self, attribute, input_fields):
        value = input_fields[attribute].text
        self.validate_and_update_attribute(attribute, value, lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update_attribute(self, attribute, value, parser):
        if validate_input_entity_property(value):
            obj = self.selected_object
            if self.selected_vertex and self.editing_vertices:
                obj = self.selected_vertex

            if self.selected_object:
                setattr(obj, attribute, parser(value))
                if obj == self.selected_vertex:
                    self.selected_object.update_vertex_position(obj.vertex_index, obj.position)

    def remove_object(self):
        if self.selected_object in self.objects:
            self.objects.remove(self.selected_object)
            destroy_entity(self.selected_object)
            self._dis_select_object()
            self._dis_select_vertex()
