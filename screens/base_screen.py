from ursina import Entity, destroy

from const import destroy_list, destroy_entity


class BaseScreen(Entity):
    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager

    def load(self):
        pass

    def destroy(self):
        destroy_list(self.children)
        destroy_entity(self)
