from ursina import mouse

from const import destroy_entity, destroy_list
from src.ui.game_pause_menu import GamePauseMenu
from screens.base_screen import BaseScreen
from entitys.player import Player
from map import Map

class GameScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.map = None
        self.player = None
        self.pause_menu = None

        self.is_paused = False

    def load(self):
        self.pause_menu = GamePauseMenu(self)

        self.map = Map(parent=self)
        self.player = Player(parent=self.map)

    def input(self, key):
        if key == 'escape':
            self.resume_game()

    def resume_game(self):
        self.pause_menu.enabled = not self.pause_menu.enabled
        mouse.visible = self.pause_menu.enabled
        mouse.locked = not self.pause_menu.enabled
        self.is_paused = self.pause_menu.enabled

    def disable(self):
        destroy_entity(self.pause_menu)

        destroy_entity(self.map)
        destroy_entity(self.player)

        destroy_list(self.children)

        destroy_entity(self)
