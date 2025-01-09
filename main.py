import random

from ursina import Ursina, Entity, window
from ursina.shaders import lit_with_shadows_shader

from panda3d.core import loadPrcFileData
loadPrcFileData("", "interpolate-frames 1")

from screens.screen_manager import ScreenManager
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen

if __name__ == "__main__":
    window.title = 'The scent of a special ops'
    window.icon = 'assets/icons/ua.png'
    window.borderless = False

    app = Ursina()
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader

    screen_manager = ScreenManager()
    screen_manager.add_screen("menu", MenuScreen)
    screen_manager.add_screen("game", GameScreen)

    screen_manager.set_active_screen("menu")
    app.run()
