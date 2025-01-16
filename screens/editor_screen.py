from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from screens.base_screen import BaseScreen

class EditorScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

        self.selected_entity = None
        self.is_animating = False
        self.objects_list = []
        self.gizmo = None
        self.dragging_axis = None
        self.start_mouse_position = None
        self.editor_camera = None

    def load(self):
        # UI Buttons
        Button(text='Cube', position=(-0.83, 0.45), scale=(0.1, 0.05), color=color.azure, on_click=self.spawn_cube)
        Button(text='Plane', position=(-0.83, 0.39), scale=(0.1, 0.05), color=color.azure, on_click=self.spawn_plane)
        # Button(text='Animate', position=(-0.7, 0.2), scale=(0.2, 0.1), color=color.violet, on_click=toggle_animation)

        Button(text='PLAY', position=(-0.05, 0.47), scale=(0.08, 0.04), color=color.gray, on_click=self.play)
        Button(text='QUIT', position=(0.05, 0.47), scale=(0.08, 0.04), color=color.gray, on_click=self.stop)

        # Rotation Buttons
        Button(text='R_X+', position=(0.8, -0.4), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.rotate_entity('x', 10))
        Button(text='R_X-', position=(0.8, -0.34), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.rotate_entity('x', -10))
        Button(text='R_Y+', position=(0.8, -0.28), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.rotate_entity('y', 10))
        Button(text='R_Y-', position=(0.8, -0.22), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.rotate_entity('y', -10))
        Button(text='R_Z+', position=(0.8, -0.16), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.rotate_entity('z', 10))
        Button(text='R_Z-', position=(0.8, -0.1), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.rotate_entity('z', -10))
        # Movement Buttons
        Button(text='M_X+', position=(0.69, -0.4), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.move_entity('x', 0.1))
        Button(text='M_X-', position=(0.69, -0.34), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.move_entity('x', -0.1))
        Button(text='M_Y+', position=(0.69, -0.28), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.move_entity('y', 0.1))
        Button(text='M_Y-', position=(0.69, -0.22), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.move_entity('y', -0.1))
        Button(text='M_Z+', position=(0.69, -0.16), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.move_entity('z', 0.1))
        Button(text='M_Z-', position=(0.69, -0.1), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.move_entity('z', -0.1))
        # Scaling Buttons
        Button(text='S_X+', position=(0.58, -0.4), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.scale_entity('x', 0.1))
        Button(text='S_X-', position=(0.58, -0.34), scale=(0.1, 0.05), color=color.red,
               on_click=lambda: self.scale_entity('x', -0.1))
        Button(text='S_Y+', position=(0.58, -0.28), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.scale_entity('y', 0.1))
        Button(text='S_Y-', position=(0.58, -0.22), scale=(0.1, 0.05), color=color.green,
               on_click=lambda: self.scale_entity('y', -0.1))
        Button(text='S_Z+', position=(0.58, -0.16), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.scale_entity('z', 0.1))
        Button(text='S_Z-', position=(0.58, -0.1), scale=(0.1, 0.05), color=color.blue,
               on_click=lambda: self.scale_entity('z', -0.1))

        Button(text='Skybox', position=(-0.83, 0.33), scale=(0.1, 0.05), color=color.violet, on_click=self.add_sky)

        self.position_text = Text(position=(-0.8, -0.45), color=color.white, font_size=18)
        self.scale_text = Text(position=(-0.8, -0.39), color=color.white, font_size=18)
        self.rotation_text = Text(position=(-0.8, -0.42), color=color.white, font_size=18)

        self.editor_camera = EditorCamera()

    def spawn_cube(self):
        cube = Entity(
            model='cube',
            texture='brick',
            scale=(1, 1, 1),
            position=(0, 0.5, 0),
            collider='box',
            name='Cube'
        )
        self.objects_list.append(cube)
        self.select_entity(cube)

    def spawn_plane(self):
        plane = Entity(
            model='plane',
            texture='grass',
            scale=(50, 1, 50),
            position=(0, 0, 0),
            collider='mesh',
            name='Plane'
        )
        self.objects_list.append(plane)
        self.select_entity(plane)

    def play(self):
        if self.editor_camera:
            destroy(self.editor_camera)
            self.editor_camera = None
        player = FirstPersonController()
        player.position = Vec3(0, 2, 0)

    def stop(self):
        app.quit()

    def update_gizmo(self):
        if self.selected_entity and not self.gizmo:
            self.gizmo = Gizmo()
        if self.gizmo and self.selected_entity:
            self.gizmo.update_position(self.selected_entity)

    def select_entity(self, entity):
        if self.selected_entity:
            # reset color of selected entity
            self.selected_entity.color = color.white
        self.selected_entity = entity
        if self.selected_entity:
            print(f"Selected: {entity.name}")
            self.selected_entity.color = color.yellow
            self.update_gizmo()

    # it dont work
    def on_mouse_down(self):
        # Perform a raycast from the mouse position
        hit_info = mouse.hovered_entity
        if hit_info and hit_info != self.gizmo:  # Ignore gizmo clicks
            self.select_entity(hit_info)

    # Animation Toggle
    def toggle_animation(self):
        self.is_animating = not self.is_animating

    # Function to move the selected entity along X, Y, or Z axis
    def move_entity(self, axis, direction):
        if self.selected_entity:
            pos = list(self.selected_entity.position)
            if axis == 'x':
                pos[0] += direction
            elif axis == 'y':
                pos[1] += direction
            elif axis == 'z':
                pos[2] += direction
            self.selected_entity.position = tuple(pos)

    # Function to rotate the selected entity around X, Y, or Z axis
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

    # Function to scale the selected entity along X, Y, or Z axis
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

    def unlock_mouse(self):
        mouse.locked = False  # Unlocks the mouse
        mouse.visible = True  # Makes the mouse cursor visible

    def input(self, key):
        if key == 'u':  # Press 'U' to unlock the mouse
            self.unlock_mouse()

    # Update function for animations and gizmos
    def update(self):
        if self.selected_entity:
            self.position_text.text = f"Position: ({self.selected_entity.x:.2f}, {self.selected_entity.y:.2f}, {self.selected_entity.z:.2f})"
            self.scale_text.text = f"Scale: ({self.selected_entity.scale_x:.2f}, {self.selected_entity.scale_y:.2f}, {self.selected_entity.scale_z:.2f})"
            self.rotation_text.text = f"Rotation: ({self.selected_entity.rotation_x:.2f}, {self.selected_entity.rotation_y:.2f}, {self.selected_entity.rotation_z:.2f})"
        # Animate entity if toggled

        if self.is_animating and self.selected_entity:
            self.selected_entity.rotation_y += 1

        # Update gizmo position
        if self.gizmo and self.selected_entity:
            self.gizmo.update_position(self.selected_entity)

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

    def add_sky(self):
        DirectionalLight().look_at(Vec3(1, -1, -1))
        Sky()

class Gizmo(Entity):
    def __init__(self):
        super().__init__()
        self.handles = []
        self.create_gizmo()

    def create_gizmo(self):
        # create translation arrows (red = X, blue = Z, no z cuz z is buggy)
        self.handles.append(Entity(
            model='cube', color=color.red, scale=(0.4, 0.05, 0.05),
            position=(0.5, 0, 0), collider='box', parent=self,
            on_click=lambda: self.start_drag('x')
        ))
        self.handles.append(Entity(
            model='cube', color=color.blue, scale=(0.05, 0.05, 0.4),
            position=(0, 0, 0.5), collider='box', parent=self,
            on_click=lambda: self.start_drag('z')
        ))

    def start_drag(self, axis):
        global dragging_axis, start_mouse_position
        dragging_axis = axis
        start_mouse_position = mouse.world_point

    def update_position(self, entity):
        self.position = entity.position
