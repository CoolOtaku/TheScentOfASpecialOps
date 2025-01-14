import random

from ursina import Ursina, Entity, window
from ursina.shaders import lit_with_shadows_shader
from panda3d.core import loadPrcFileData

from screens.screen_manager import ScreenManager
from screens.editor_screen import EditorScreen
from screens.menu_screen import MenuScreen
from screens.game_screen import GameScreen

if __name__ == '__main__':
    window.title = 'The scent of a special ops'
    window.icon = 'assets/icons/ua.png'
    window.borderless = False

    app = Ursina()
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader
    loadPrcFileData('', 'interpolate-frames 1')

    screen_manager = ScreenManager()
    screen_manager.add_screen('menu', MenuScreen)
    screen_manager.add_screen('game', GameScreen)
    screen_manager.add_screen('editor', EditorScreen)

    screen_manager.set_active_screen('menu')
    app.run()
