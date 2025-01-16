from ursina import destroy, mouse, application

from entitys.ui.game_pause_menu import GamePauseMenu
from screens.base_screen import BaseScreen
from entitys.player import Player
from map import Map

class GameScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

    def load(self):
        self.pause_menu = GamePauseMenu(self)

        self.map = Map(parent=self)
        #self.player = Player(parent=self.map)

        #shootables_parent = Entity()
        #mouse.traverse_target = shootables_parent

    def input(self, key):
        if key == 'escape':
            self.resume_game()

    def resume_game(self):
        self.pause_menu.enabled = not self.pause_menu.enabled
        mouse.visible = self.pause_menu.enabled
        mouse.locked = not self.pause_menu.enabled
        application.paused = self.pause_menu.enabled

    def disable(self):
        self.pause_menu.disable()
        destroy(self.pause_menu)

        self.map.disable()

        for child in self.children:
            child.disable()
            destroy(child)

        self.children.clear()
        super().disable()
        destroy(self)
        del self
