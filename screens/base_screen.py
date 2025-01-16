from ursina import Entity, destroy


class BaseScreen(Entity):
    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager

    def load(self):
        pass

    def destroy(self):
        for child in self.children:
            child.disable()
            destroy(child)

        self.children.clear()
        self.disable()
        destroy(self)
        del self
