class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.active_screen = None

    def add_screen(self, name, screen_class):
        self.screens[name] = {
            'class': screen_class,
            'instance': None
        }

    def set_active_screen(self, name):
        if self.active_screen:
            self.screens[self.active_screen]['instance'].hide()
            self.screens[self.active_screen]['instance'].clear()

        if not self.screens[name]['instance']:
            screen_instance = self.screens[name]['class'](self)
            screen_instance.load()
            self.screens[name]['instance'] = screen_instance

        self.active_screen = name
        self.screens[name]['instance'].show()
