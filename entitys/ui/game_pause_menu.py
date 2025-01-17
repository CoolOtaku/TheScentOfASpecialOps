from ursina import Entity, Text, camera, color

from const import PATH_WINDOW_TEXTURE, PATH_TITLE_FONT
from entitys.ui.game_button import GameButton


class GamePauseMenu(Entity):
    def __init__(self, game_screen):
        super().__init__(parent=camera.ui, enabled=False)
        Entity(
            texture=PATH_WINDOW_TEXTURE,
            scale=(1.5, 0.8), z=0,
            model='quad',
            parent=self
        )
        Text(
            text='Пауза', font=PATH_TITLE_FONT, color=color.white,
            origin=(0, -6), scale=2, z=-1,
            parent=self
        )
        GameButton(
            text='Продовжити',
            position=(0, 0),
            is_in_window=True,
            on_click=lambda: game_screen.resume_game(),
            parent=self
        )
        GameButton(
            text='Вийти в меню',
            position=(0, -0.2),
            is_in_window=True,
            on_click=lambda: game_screen.screen_manager.set_screen('menu'),
            parent=self
        )
