from ursina import Entity

class BaseScreen(Entity):
    def __init__(self):
        super().__init__(visible = False)

    def load(self):
        pass

    def clear(self):
        for child in self.children:
            child.disable()
            child.parent = None
        self.children = []
        self.disable()
