from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from src.map_manager import MapManager
from screens.base_screen import BaseScreen
from src.editor_object_manager import EditorObjectManager
from const import validate_input_entity_property, destroy_entity, destroy_list, destroy_dict

from entitys.primitive.primitive_imports import *


class EditorScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.button_play = None
        self.button_stop = None

        self.menu_main = None
        self.menu_objects_primitive = None

        self.pressed_buttons = {}
        self.position_buttons = None
        self.scale_buttons = None
        self.rotation_buttons = None

        self.vertices_buttons = None

        self.title_fields_PSR = {}
        self.input_fields_PSR = {}
        self.last_values_PSR = {}

        self.editor_object_manager = None
        self.editor_camera = None
        self.player = None

    def load(self):
        self.button_play = Button(text='ГРАТИ', position=(-0.05, 0.48), scale=(0.09, 0.03), on_click=self.play)
        self.button_stop = Button(text='СТОП', position=(0.05, 0.48), scale=(0.09, 0.03), on_click=self.stop)

        self.menu_main = DropdownMenu(
            'Меню',
            buttons=[
                DropdownMenuButton('Зберегти', on_click=lambda: MapManager.export_to_json(self.editor_object_manager.objects)),
                DropdownMenuButton('Завантажити', on_click=lambda: MapManager.import_from_json(self.editor_object_manager)),
                DropdownMenuButton('Вийти', on_click=lambda: self.screen_manager.set_screen('menu')),
                DropdownMenuButton('Небо', on_click=self.add_sky),
            ],
            position=(-0.88, 0.495), z=-100
        )
        self.menu_objects_primitive = DropdownMenu(
            'Об\'єкти (примітивні)',
            buttons=[
                DropdownMenuButton('Площина', on_click=lambda: self.editor_object_manager.create_object(Plane)),
                DropdownMenuButton('Куб', on_click=lambda: self.editor_object_manager.create_object(Cube)),
                DropdownMenuButton('Каркасний куб',
                                   on_click=lambda: self.editor_object_manager.create_object(WireframeCube)),
                DropdownMenuButton('Куб із UV зверху',
                                   on_click=lambda: self.editor_object_manager.create_object(CubeUVTop)),
                DropdownMenuButton('Чотирикутник', on_click=lambda: self.editor_object_manager.create_object(Quad)),
                DropdownMenuButton('Сфера', on_click=lambda: self.editor_object_manager.create_object(Sphere)),
                DropdownMenuButton('Коло', on_click=lambda: self.editor_object_manager.create_object(Circle)),
                DropdownMenuButton('Іco сфера', on_click=lambda: self.editor_object_manager.create_object(IcoSphere)),
                DropdownMenuButton('Небесний купол',
                                   on_click=lambda: self.editor_object_manager.create_object(SkyDome)),
                DropdownMenuButton('Діамант', on_click=lambda: self.editor_object_manager.create_object(Diamond)),
            ],
            position=(-0.88, 0.45), z=-99
        )

        self.position_buttons = ButtonList(button_dict={
            'PX+': lambda: self.start_holding_button('PX+', 'x', 0.02),
            'PX-': lambda: self.start_holding_button('PX-', 'x', -0.02),
            'PY+': lambda: self.start_holding_button('PY+', 'y', 0.02),
            'PY-': lambda: self.start_holding_button('PY-', 'y', -0.02),
            'PZ+': lambda: self.start_holding_button('PZ+', 'z', 0.02),
            'PZ-': lambda: self.start_holding_button('PZ-', 'z', -0.02)
        }, position=(0.691, -0.27), button_height=1.5, width=0.06)
        self.scale_buttons = ButtonList(button_dict={
            'SX+': lambda: self.start_holding_button('SX+', 'x', 0.02),
            'SX-': lambda: self.start_holding_button('SX-', 'x', -0.02),
            'SY+': lambda: self.start_holding_button('SY+', 'y', 0.02),
            'SY-': lambda: self.start_holding_button('SY-', 'y', -0.02),
            'SZ+': lambda: self.start_holding_button('SZ+', 'z', 0.02),
            'SZ-': lambda: self.start_holding_button('SZ-', 'z', -0.02)
        }, position=(0.755, -0.27), button_height=1.5, width=0.06)
        self.rotation_buttons = ButtonList(button_dict={
            'RX+': lambda: self.start_holding_button('RX+', 'x', 1),
            'RX-': lambda: self.start_holding_button('RX-', 'x', -1),
            'RY+': lambda: self.start_holding_button('RY+', 'y', 1),
            'RY-': lambda: self.start_holding_button('RY-', 'y', -1),
            'RZ+': lambda: self.start_holding_button('RZ+', 'z', 1),
            'RZ-': lambda: self.start_holding_button('RZ-', 'z', -1)
        }, position=(0.82, -0.27), button_height=1.5, width=0.06)
        self.vertices_buttons = Button(text='Вершини', position=(0.78, -0.25), scale=(0.2, 0.03),
                                       on_click=lambda: self.editor_object_manager.on_editing_vertices())

        self.title_fields_PSR = {
            'position': Text('Позиція:', position=(-0.065, -0.35)),
            'scale': Text('Розмір:', position=(-0.05, -0.4)),
            'rotation': Text('Обертання:', position=(-0.1, -0.46))
        }
        self.input_fields_PSR = {
            'position': InputField(position=(0.3, -0.36), on_value_changed=self.validate_and_update_position),
            'scale': InputField(position=(0.3, -0.415), on_value_changed=self.validate_and_update_scale),
            'rotation': InputField(position=(0.3, -0.47), on_value_changed=self.validate_and_update_rotation)
        }
        self.last_values_PSR = {key: '' for key in self.input_fields_PSR}

        self.editor_object_manager = EditorObjectManager(self)
        self.editor_camera = EditorCamera()

    def input(self, key):
        if key.endswith('up'):
            self.stop_holding_button()

        if key == 'left mouse down':
            self.on_mouse_down()
        elif key == 'delete':
            self.editor_object_manager.remove_object()
        elif key == 'u':
            self.unlock_mouse()

    def update(self):
        for button_name, (axis, value) in self.pressed_buttons.items():
            if 'P' in button_name:
                self.update_entity_attribute('position', axis, value)
            elif 'S' in button_name:
                self.update_entity_attribute('scale', axis, value)
            elif 'R' in button_name:
                self.update_entity_attribute('rotation', axis, value)

        if self.editor_object_manager.selected_object:
            for key, input_field in self.input_fields_PSR.items():
                new_value = f'{getattr(self.editor_object_manager.selected_object, key).x:.2f},{getattr(self.editor_object_manager.selected_object, key).y:.2f},{getattr(self.editor_object_manager.selected_object, key).z:.2f}'
                if self.last_values_PSR[key] != new_value:
                    input_field.text = new_value
                    self.last_values_PSR[key] = new_value
                input_field.show()
                self.title_fields_PSR[key].show()

            self.position_buttons.show()
            self.scale_buttons.show()
            self.rotation_buttons.show()
            self.vertices_buttons.show()
        else:
            for key, input_field in self.input_fields_PSR.items():
                input_field.hide()
                self.title_fields_PSR[key].hide()

            self.position_buttons.hide()
            self.scale_buttons.hide()
            self.rotation_buttons.hide()
            self.vertices_buttons.hide()

    def play(self):
        if self.editor_camera:
            destroy_entity(self.editor_camera)
            self.editor_camera = None
        if self.player:
            destroy(self.player)
        self.player = FirstPersonController()
        self.player.position = (0, 2, 0)

    def stop(self):
        if self.player:
            destroy_entity(self.player)
            self.player = None
        self.editor_camera = EditorCamera()

        from ursina import held_keys
        held_keys.clear()

    def on_mouse_down(self):
        if mouse.hovered_entity:
            if (isinstance(mouse.hovered_entity, (Button, ButtonList))
                    or isinstance(mouse.hovered_entity.parent, ButtonList)):
                return

            self.editor_object_manager.select(mouse.hovered_entity)

    def start_holding_button(self, button_name, axis, value):
        self.pressed_buttons[button_name] = (axis, value)

    def stop_holding_button(self):
        self.pressed_buttons.clear()

    def update_entity_attribute(self, attribute, axis, value):
        if self.editor_object_manager.selected_object:
            attr = list(getattr(self.editor_object_manager.selected_object, attribute))
            if axis == 'x':
                attr[0] += value
            elif axis == 'y':
                attr[1] += value
            elif axis == 'z':
                attr[2] += value
            setattr(self.editor_object_manager.selected_object, attribute, tuple(attr))

    def validate_and_update_position(self):
        self.validate_and_update('position', self.input_fields_PSR['position'].text,
                                 lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update_scale(self):
        self.validate_and_update('scale', self.input_fields_PSR['scale'].text,
                                 lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update_rotation(self):
        self.validate_and_update('rotation', self.input_fields_PSR['rotation'].text,
                                 lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update(self, attribute, value, parser):
        if validate_input_entity_property(value):
            if self.editor_object_manager.selected_object:
                setattr(self.editor_object_manager.selected_object, attribute, parser(value))
        else:
            print(f'Некоректне значення для {attribute}!')

    @staticmethod
    def unlock_mouse():
        mouse.locked = False
        mouse.visible = True

    @staticmethod
    def add_sky():
        Sky(texture='assets/textures/maps/sky1.jpg')

    def disable(self):
        destroy_entity(self.button_play)
        destroy_entity(self.button_stop)

        destroy_list(self.menu_main.buttons)
        destroy_entity(self.menu_main)
        destroy_list(self.menu_objects_primitive.buttons)
        destroy_entity(self.menu_objects_primitive)

        destroy_dict(self.pressed_buttons)

        destroy_list(self.position_buttons.button_dict)
        destroy_entity(self.position_buttons)
        destroy_list(self.scale_buttons.button_dict)
        destroy_entity(self.scale_buttons)
        destroy_list(self.rotation_buttons.button_dict)
        destroy_entity(self.rotation_buttons)

        destroy_entity(self.vertices_buttons)

        destroy_dict(self.title_fields_PSR)
        destroy_dict(self.input_fields_PSR)
        destroy_dict(self.last_values_PSR)

        destroy_entity(self.editor_camera)
        destroy_entity(self.player)

        destroy_list(self.children)
        destroy_entity(self)
