import json

from ursina import Vec3

from entitys.primitive.primitive_imports import *


class MapManager:
    @staticmethod
    def export_to_json(objects, filename='map.json'):
        data = []

        for obj in objects:
            obj_data = {
                'class': obj.__class__.__name__,
                'texture': obj.texture.name if obj.texture else None,
                'position': MapManager.vec3_to_list(obj.position),
                'scale': MapManager.vec3_to_list(obj.scale),
                'rotation': MapManager.vec3_to_list(obj.rotation),
                'vertices': [MapManager.vec3_to_list(v) for v in obj.get_vertices()]
            }
            data.append(obj_data)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f'Карта успішно збережена в {filename}')

    @staticmethod
    def import_from_json(editor_object, filename='map.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            for obj_data in data:
                obj_class = globals().get(obj_data['class'])
                if obj_class:
                    obj_instance = obj_class()
                    for key, value in obj_data.items():
                        if key == 'vertices':
                            for i in range(len(value)):
                                obj_instance.update_vertex_position(i, obj_instance.local_to_world(Vec3(*value[i])))

                        setattr(obj_instance, key, value)

                    obj_instance.parent = editor_object.parent
                    editor_object.objects.append(obj_instance)

            print(f'Карта успішно завантажена з {filename}')
        except Exception as e:
            print(f'Помилка завантаження карти: {e}')

    @staticmethod
    def vec3_to_list(vec):
        return [vec.x, vec.y, vec.z] if isinstance(vec, Vec3) else vec
