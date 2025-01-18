from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.first_person_controller import FirstPersonController

from screens.base_screen import BaseScreen


class EditorScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.button_play = None
        self.button_quit = None

        self.menu_objects_primitive = None

        self.pressed_buttons = {}
        self.position_buttons = None
        self.scale_buttons = None
        self.rotation_buttons = None

        self.input_fields = {}
        self.last_values = {}

        self.selected_entity = None
        self.is_animating = False
        self.objects_list = []
        self.dragging_axis = None
        self.start_mouse_position = None
        self.editor_camera = None

    def load(self):
        self.button_play = Button(text='ГРАТИ', position=(-0.05, 0.48), scale=(0.09, 0.03), on_click=self.play)
        self.button_quit = Button(text='ВИЙТИ', position=(0.05, 0.48), scale=(0.09, 0.03),
                                  on_click=lambda: self.screen_manager.set_screen('menu'))

        self.menu_objects_primitive = DropdownMenu(
            'Об\'єкти (примітивні)',
            buttons=[
                DropdownMenuButton('Площина', on_click=self.spawn_plane),
                DropdownMenuButton('Небо', on_click=self.add_sky),
                DropdownMenuButton('Куб', on_click=self.spawn_cube),
            ],
            position=(-0.88, 0.45)
        )

        self.position_buttons = ButtonList(button_dict={
            'PX+': lambda: self.start_holding_button('PX+', 'x', 0.02),
            'PX-': lambda: self.start_holding_button('PX-', 'x', -0.02),
            'PY+': lambda: self.start_holding_button('PY+', 'y', 0.02),
            'PY-': lambda: self.start_holding_button('PY-', 'y', -0.02),
            'PZ+': lambda: self.start_holding_button('PZ+', 'z', 0.02),
            'PZ-': lambda: self.start_holding_button('PZ-', 'z', -0.02)
        }, position=(0.691, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)
        self.scale_buttons = ButtonList(button_dict={
            'SX+': lambda: self.start_holding_button('SX+', 'x', 0.02),
            'SX-': lambda: self.start_holding_button('SX-', 'x', -0.02),
            'SY+': lambda: self.start_holding_button('SY+', 'y', 0.02),
            'SY-': lambda: self.start_holding_button('SY-', 'y', -0.02),
            'SZ+': lambda: self.start_holding_button('SZ+', 'z', 0.02),
            'SZ-': lambda: self.start_holding_button('SZ-', 'z', -0.02)
        }, position=(0.755, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)
        self.rotation_buttons = ButtonList(button_dict={
            'RX+': lambda: self.start_holding_button('RX+', 'x', 1),
            'RX-': lambda: self.start_holding_button('RX-', 'x', -1),
            'RY+': lambda: self.start_holding_button('RY+', 'y', 1),
            'RY-': lambda: self.start_holding_button('RY-', 'y', -1),
            'RZ+': lambda: self.start_holding_button('RZ+', 'z', 1),
            'RZ-': lambda: self.start_holding_button('RZ-', 'z', -1)
        }, position=(0.82, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)

        self.input_fields = {
            'position': InputField(position=(0.3, -0.36), color=color.black, on_value_changed=self.validate_and_update_position),
            'scale': InputField(position=(0.3, -0.415), color=color.black, on_value_changed=self.validate_and_update_scale),
            'rotation': InputField(position=(0.3, -0.47), color=color.black, on_value_changed=self.validate_and_update_rotation),
        }
        self.last_values = {
            'position': self.input_fields['position'].text,
            'scale': self.input_fields['scale'].text,
            'rotation': self.input_fields['rotation'].text,
        }
        self.last_values = {key: '' for key in self.input_fields}

        self.editor_camera = EditorCamera()

    @staticmethod
    def validate_input(value):
        if re.fullmatch(r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){2}$', value):
            return True
        return False

    def validate_and_update_position(self):
        self.update_entity_attribute('position', self.input_fields['position'].text, lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update_scale(self):
        self.update_entity_attribute('scale', self.input_fields['scale'].text, lambda v: Vec3(*map(float, v.split(','))))

    def validate_and_update_rotation(self):
        self.update_entity_attribute('rotation', self.input_fields['rotation'].text, lambda v: Vec3(*map(float, v.split(','))))

    def update_entity_attribute(self, attribute, value, parser):
        if self.validate_input(value):
            if self.selected_entity:
                setattr(self.selected_entity, attribute, parser(value))
        else:
            print(f'Некоректне значення для {attribute}!')

    def input(self, key):
        if key.endswith('up'):
            self.stop_holding_button()

        if key == 'left mouse down':
            self.on_mouse_down()
        elif key == 'u':
            self.unlock_mouse()

    def update(self):
        for button_name, (axis, value) in self.pressed_buttons.items():
            if 'P' in button_name:
                self.position_entity(axis, value)
            elif 'S' in button_name:
                self.scale_entity(axis, value)
            elif 'R' in button_name:
                self.rotate_entity(axis, value)

        if self.selected_entity:
            for key, input_field in self.input_fields.items():
                new_value = f"{getattr(self.selected_entity, key).x:.2f},{getattr(self.selected_entity, key).y:.2f},{getattr(self.selected_entity, key).z:.2f}"
                if self.last_values[key] != new_value:
                    input_field.text = new_value
                    self.last_values[key] = new_value

        if self.is_animating and self.selected_entity:
            self.selected_entity.rotation_y += 1

        # Handle dragging
        if self.dragging_axis and mouse.world_point and self.selected_entity:
            current_mouse_position = mouse.world_point
            movement_delta = current_mouse_position - self.start_mouse_position

            # Move entity along the selected axis
            if self.dragging_axis == 'x':
                self.selected_entity.x += movement_delta.x
            elif self.dragging_axis == 'z':
                self.selected_entity.z += movement_delta.z

            # Update start_mouse_position for smooth dragging
            self.start_mouse_position = current_mouse_position

        # Reset dragging when mouse button is released
        if not mouse.left:
            self.dragging_axis = None

    def play(self):
        if self.editor_camera:
            destroy(self.editor_camera)
            self.editor_camera = None
        player = FirstPersonController()
        player.position = (0, 2, 0)

    def on_mouse_down(self):
        if mouse.hovered_entity:
            if (isinstance(mouse.hovered_entity, (Button, ButtonList))
                    or isinstance(mouse.hovered_entity.parent, ButtonList)):
                return

            self.select_entity(mouse.hovered_entity)

    def spawn_cube(self):
        cube = Entity(
            model='cube',
            texture='brick',
            scale=(1, 1, 1),
            position=(0, 0.5, 0),
            collider='box',
            name='Cube',
            parent=self
        )
        self.objects_list.append(cube)
        self.select_entity(cube)

    def spawn_plane(self):
        plane = Entity(
            model='plane',
            texture='grass',
            scale=(50, 1, 50),
            position=(0, 0, 0),
            collider='box',
            name='Plane',
            parent=self
        )
        self.objects_list.append(plane)
        self.select_entity(plane)

    def select_entity(self, entity):
        if self.selected_entity:
            self.selected_entity.color = color.white
        self.selected_entity = entity
        self.selected_entity.color = color.yellow
        print(f'Вибрано об\'єкт: {entity.name}')

    def toggle_animation(self):
        self.is_animating = not self.is_animating

    def start_holding_button(self, button_name, axis, value):
        self.pressed_buttons[button_name] = (axis, value)

    def stop_holding_button(self):
        self.pressed_buttons.clear()

    def position_entity(self, axis, direction):
        if self.selected_entity:
            pos = list(self.selected_entity.position)
            if axis == 'x':
                pos[0] += direction
            elif axis == 'y':
                pos[1] += direction
            elif axis == 'z':
                pos[2] += direction
            self.selected_entity.position = tuple(pos)

    def scale_entity(self, axis, amount):
        if self.selected_entity:
            scale = list(self.selected_entity.scale)
            if axis == 'x':
                scale[0] += amount
            elif axis == 'y':
                scale[1] += amount
            elif axis == 'z':
                scale[2] += amount
            self.selected_entity.scale = tuple(scale)

    def rotate_entity(self, axis, amount):
        if self.selected_entity:
            rot = list(self.selected_entity.rotation)
            if axis == 'x':
                rot[0] += amount
            elif axis == 'y':
                rot[1] += amount
            elif axis == 'z':
                rot[2] += amount
            self.selected_entity.rotation = tuple(rot)

    def unlock_mouse(self):
        mouse.locked = False
        mouse.visible = True

    def add_sky(self):
        DirectionalLight().look_at((1, -1, -1))
        Sky()
