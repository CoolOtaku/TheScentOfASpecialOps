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

        self.position_buttons = None
        self.scale_buttons = None
        self.rotation_buttons = None

        self.position_text = None
        self.scale_text = None
        self.rotation_text = None

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
            'PX+': Func(self.position_entity, 'x', 0.1),
            'PX-': Func(self.position_entity, 'x', -0.1),
            'PY+': Func(self.position_entity, 'y', 0.1),
            'PY-': Func(self.position_entity, 'y', -0.1),
            'PZ+': Func(self.position_entity, 'z', 0.1),
            'PZ-': Func(self.position_entity, 'z', -0.1),
        }, position=(0.691, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)
        self.scale_buttons = ButtonList(button_dict={
            'SX+': Func(self.scale_entity, 'x', 0.1),
            'SX-': Func(self.scale_entity, 'x', -0.1),
            'SY+': Func(self.scale_entity, 'y', 0.1),
            'SY-': Func(self.scale_entity, 'y', -0.1),
            'SZ+': Func(self.scale_entity, 'z', 0.1),
            'SZ-': Func(self.scale_entity, 'z', -0.1),
        }, position=(0.755, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)
        self.rotation_buttons = ButtonList(button_dict={
            'RX+': Func(self.rotate_entity, 'x', 10),
            'RX-': Func(self.rotate_entity, 'x', -10),
            'RY+': Func(self.rotate_entity, 'y', 10),
            'RY-': Func(self.rotate_entity, 'y', -10),
            'RZ+': Func(self.rotate_entity, 'z', 10),
            'RZ-': Func(self.rotate_entity, 'z', -10),
        }, position=(0.82, -0.27), button_height=1.5, width=0.06, on_click=self.rotate_entity)

        self.position_text = Text(position=(0.25, -0.425), color=color.black)
        self.scale_text = Text(position=(0.25, -0.45), color=color.black)
        self.rotation_text = Text(position=(0.25, -0.475), color=color.black)

        self.editor_camera = EditorCamera()

    def input(self, key):
        if key == 'left mouse down':
            self.on_mouse_down()
        elif key == 'u':
            self.unlock_mouse()

    def update(self):
        if self.selected_entity:
            self.position_text.text = f'Позиція: ({self.selected_entity.x:.2f}, {self.selected_entity.y:.2f}, {self.selected_entity.z:.2f})'
            self.scale_text.text = f'Масштаб: ({self.selected_entity.scale_x:.2f}, {self.selected_entity.scale_y:.2f}, {self.selected_entity.scale_z:.2f})'
            self.rotation_text.text = f'Обертання: ({self.selected_entity.rotation_x:.2f}, {self.selected_entity.rotation_y:.2f}, {self.selected_entity.rotation_z:.2f})'
        # Animate entity if toggled

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
