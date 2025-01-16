from ursina.shaders import lit_with_shadows_shader
from panda3d.core import loadPrcFileData
from ursina import Ursina, Entity

from screens.screen_manager import ScreenManager
from screens.editor_screen import EditorScreen
from screens.menu_screen import MenuScreen
from screens.game_screen import GameScreen

if __name__ == '__main__':
    Entity.default_shader = lit_with_shadows_shader
    loadPrcFileData('', 'interpolate-frames 1')

    app = Ursina(title='The scent of a special ops', icon='assets/icons/icon.ico', borderless=False)

    screen_manager = ScreenManager()
    screen_manager.add_screen('menu', MenuScreen)
    screen_manager.add_screen('game', GameScreen)
    screen_manager.add_screen('editor', EditorScreen)

    screen_manager.set_screen('menu')

    app.run()
