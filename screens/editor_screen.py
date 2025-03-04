from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from entitys.player import Player
from src.map_manager import MapManager
from screens.base_screen import BaseScreen
from src.editor_object_manager import EditorObjectManager
from const import destroy_entity, destroy_list, destroy_dict

from entitys.primitive.primitive_imports import *
from entitys.houses.houses_imports import *


class EditorScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.editor_screen_ui = Entity(parent=camera.ui)

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
        Button(text='ГРАТИ', position=(-0.05, 0.48), scale=(0.09, 0.03), on_click=self.play,
               parent=self.editor_screen_ui)
        Button(text='СТОП', position=(0.05, 0.48), scale=(0.09, 0.03), on_click=self.stop, parent=self.editor_screen_ui)

        DropdownMenu(
            'Меню',
            buttons=[
                DropdownMenuButton('Зберегти',
                                   on_click=lambda: MapManager.export_to_json(self.editor_object_manager.objects)),
                DropdownMenuButton('Завантажити',
                                   on_click=lambda: MapManager.import_from_json(self.editor_object_manager)),
                DropdownMenuButton('Вийти', on_click=lambda: self.screen_manager.set_screen('menu')),
                DropdownMenuButton('Небо', on_click=self.add_sky),
            ],
            position=(-0.88, 0.495), z=-100, parent=self.editor_screen_ui
        )
        DropdownMenu(
            'Об\'єкти (примітивні)',
            buttons=[
                DropdownMenuButton('Площина', on_click=lambda: self.editor_object_manager.create_object(Plane)),
                DropdownMenuButton('Куб', on_click=lambda: self.editor_object_manager.create_object(Cube)),
                DropdownMenuButton('Свій Куб', on_click=lambda: self.editor_object_manager.create_object(CustomCube)),
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
                DropdownMenuButton('Конус', on_click=lambda: self.editor_object_manager.create_object(UrsinaCone)),
                DropdownMenuButton('Свій Конус', on_click=lambda: self.editor_object_manager.create_object(CustomCone)),
                DropdownMenuButton('Циліндер',
                                   on_click=lambda: self.editor_object_manager.create_object(UrsinaCylinder)),
                DropdownMenuButton('Свій Циліндер',
                                   on_click=lambda: self.editor_object_manager.create_object(CustomCylinder)),
                DropdownMenuButton('Сітка',
                                   on_click=lambda: self.editor_object_manager.create_object(UrsinaGrid)),
            ],
            position=(-0.88, 0.45), z=-99, parent=self.editor_screen_ui
        )
        DropdownMenu(
            'Будинки',
            buttons=[
                DropdownMenuButton('Спостерігальна вежа',
                                   on_click=lambda: self.editor_object_manager.create_object(ObservationTower)),
                DropdownMenuButton('Трьох поверхівка',
                                   on_click=lambda: self.editor_object_manager.create_object(ThreeFloors)),

            ],
            position=(-0.88, 0.42), z=-98, parent=self.editor_screen_ui
        )

        self.position_buttons = ButtonList(button_dict={
            'PX+': lambda: self.start_holding_button('PX+', 'x', 0.02),
            'PX-': lambda: self.start_holding_button('PX-', 'x', -0.02),
            'PY+': lambda: self.start_holding_button('PY+', 'y', 0.02),
            'PY-': lambda: self.start_holding_button('PY-', 'y', -0.02),
            'PZ+': lambda: self.start_holding_button('PZ+', 'z', 0.02),
            'PZ-': lambda: self.start_holding_button('PZ-', 'z', -0.02)
        }, position=(0.691, -0.27), button_height=1.5, width=0.06, parent=self.editor_screen_ui)
        self.scale_buttons = ButtonList(button_dict={
            'SX+': lambda: self.start_holding_button('SX+', 'x', 0.02),
            'SX-': lambda: self.start_holding_button('SX-', 'x', -0.02),
            'SY+': lambda: self.start_holding_button('SY+', 'y', 0.02),
            'SY-': lambda: self.start_holding_button('SY-', 'y', -0.02),
            'SZ+': lambda: self.start_holding_button('SZ+', 'z', 0.02),
            'SZ-': lambda: self.start_holding_button('SZ-', 'z', -0.02)
        }, position=(0.755, -0.27), button_height=1.5, width=0.06, parent=self.editor_screen_ui)
        self.rotation_buttons = ButtonList(button_dict={
            'RX+': lambda: self.start_holding_button('RX+', 'x', 1),
            'RX-': lambda: self.start_holding_button('RX-', 'x', -1),
            'RY+': lambda: self.start_holding_button('RY+', 'y', 1),
            'RY-': lambda: self.start_holding_button('RY-', 'y', -1),
            'RZ+': lambda: self.start_holding_button('RZ+', 'z', 1),
            'RZ-': lambda: self.start_holding_button('RZ-', 'z', -1)
        }, position=(0.82, -0.27), button_height=1.5, width=0.06, parent=self.editor_screen_ui)
        self.vertices_buttons = Button(text='Вершини', position=(0.78, -0.25), scale=(0.2, 0.03),
                                       on_click=lambda: self.editor_object_manager.on_editing_vertices(),
                                       parent=self.editor_screen_ui)

        self.title_fields_PSR = {
            'position': Text('Позиція:', position=(-0.065, -0.35), parent=self.editor_screen_ui),
            'scale': Text('Розмір:', position=(-0.05, -0.4), parent=self.editor_screen_ui),
            'rotation': Text('Обертання:', position=(-0.1, -0.46), parent=self.editor_screen_ui)
        }
        self.input_fields_PSR = {
            'position': InputField(position=(0.3, -0.36),
                                   on_value_changed=lambda: self.editor_object_manager.validate_and_update_transform(
                                       'position', self.input_fields_PSR), parent=self.editor_screen_ui),
            'scale': InputField(position=(0.3, -0.415),
                                on_value_changed=lambda: self.editor_object_manager.validate_and_update_transform(
                                    'scale', self.input_fields_PSR), parent=self.editor_screen_ui),
            'rotation': InputField(position=(0.3, -0.47),
                                   on_value_changed=lambda: self.editor_object_manager.validate_and_update_transform(
                                       'rotation', self.input_fields_PSR), parent=self.editor_screen_ui)
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
                self.editor_object_manager.update_attribute('position', axis, value)
            elif 'S' in button_name:
                self.editor_object_manager.update_attribute('scale', axis, value)
            elif 'R' in button_name:
                self.editor_object_manager.update_attribute('rotation', axis, value)

        if self.editor_object_manager.selected_object:
            target = self.editor_object_manager.selected_vertex if self.editor_object_manager.selected_vertex and self.editor_object_manager.editing_vertices else self.editor_object_manager.selected_object

            for key, input_field in self.input_fields_PSR.items():
                new_value = f'{getattr(target, key).x:.2f},{getattr(target, key).y:.2f},{getattr(target, key).z:.2f}'

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
        if self.player:
            destroy_entity(self.player)
        self.player = Player(parent=self)

    def stop(self):
        if self.player:
            destroy_entity(self.player)
        self.editor_camera = EditorCamera()

        from ursina import held_keys
        held_keys.clear()

    def on_mouse_down(self):
        if mouse.hovered_entity:
            if (isinstance(mouse.hovered_entity, (Button, ButtonList))
                    or isinstance(mouse.hovered_entity.parent, ButtonList)
                    or isinstance(mouse.hovered_entity, FirstPersonController)):
                return

            self.editor_object_manager.select(mouse.hovered_entity)

    def start_holding_button(self, button_name, axis, value):
        self.pressed_buttons[button_name] = (axis, value)

    def stop_holding_button(self):
        self.pressed_buttons.clear()

    @staticmethod
    def unlock_mouse():
        mouse.locked = False
        mouse.visible = True

    @staticmethod
    def add_sky():
        DirectionalLight().look_at((1, -1, -1))
        Sky()

    def disable(self):
        destroy_list(self.editor_screen_ui.children)
        destroy_entity(self.editor_screen_ui)

        destroy_dict(self.pressed_buttons)

        destroy_dict(self.position_buttons.button_dict)
        destroy_entity(self.position_buttons)
        destroy_dict(self.scale_buttons.button_dict)
        destroy_entity(self.scale_buttons)
        destroy_dict(self.rotation_buttons.button_dict)
        destroy_entity(self.rotation_buttons)

        destroy_entity(self.vertices_buttons)

        destroy_dict(self.title_fields_PSR)
        destroy_dict(self.input_fields_PSR)
        destroy_dict(self.last_values_PSR)

        destroy_entity(self.editor_camera)
        destroy_entity(self.player)

        destroy_list(self.children)
        destroy_entity(self)
