from ursina import camera


class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.active_screen = None
        self.camera_defaults = {
            'position': camera.position,
            'rotation': camera.rotation,
            'scale': camera.scale,
            'fov': camera.fov,
            'parent': camera.parent
        }

    def add_screen(self, name, screen_class):
        self.screens[name] = {
            'class': screen_class,
            'instance': None
        }

    def set_screen(self, name):
        if self.active_screen:
            self.screens[self.active_screen]['instance'].destroy()

        if not self.screens[name]['instance']:
            screen_instance = self.screens[name]['class'](self)
            screen_instance.load()
            self.screens[name]['instance'] = screen_instance

        self.active_screen = name

        if self.active_screen == 'menu':
            self.reset_camera()

        self.screens[name]['instance'].show()

    def reset_camera(self):
        camera.position = self.camera_defaults['position']
        camera.rotation = self.camera_defaults['rotation']
        camera.scale = self.camera_defaults['scale']
        camera.fov = self.camera_defaults['fov']
        camera.parent = self.camera_defaults['parent']
