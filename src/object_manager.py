from ursina import destroy


class ObjectManager:
    def __init__(self, parent):
        self.objects = []
        self.parent = parent

    def create_object(self, obj_class, **kwargs):
        obj = obj_class(parent=self.parent, **kwargs)
        self.objects.append(obj)
        return obj

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            obj.disable()
            destroy(obj)
