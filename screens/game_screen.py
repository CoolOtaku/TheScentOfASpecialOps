from ursina import EditorCamera, Entity, mouse, application, held_keys

from screens.base_screen import BaseScreen
from entitys.player import Player
from map import Map

class GameScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager

    def load(self):
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)

        self.map = Map()
        self.player = Player(parent=self.map)

        shootables_parent = Entity()
        mouse.traverse_target = shootables_parent

        def pause_input(key):
            if key == 'tab':
                self.editor_camera.enabled = not self.editor_camera.enabled

                self.player.visible_self = self.editor_camera.enabled
                self.player.cursor.enabled = not self.editor_camera.enabled
                if self.player.current_weapon:
                    self.player.current_weapon.enabled = not self.editor_camera.enabled
                mouse.locked = not self.editor_camera.enabled
                self.editor_camera.position = self.player.position

                application.paused = self.editor_camera.enabled

        self.pause_handler = Entity(ignore_paused=True, input=pause_input)

    def update(self):
        self.player.update()
