from ursina import Sprite, Text, color, application

from screens.base_screen import BaseScreen
from entitys.ui.game_button import GameButton
from const import PATH_BACKGROUND_TEXTURE, PATH_TITLE_FONT

class MenuScreen(BaseScreen):
    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager

    def load(self):
        Sprite(
            texture=PATH_BACKGROUND_TEXTURE,
            scale=2, position=(0, 0), z=0,
            parent=self
        )
        Text(
            text='Головне меню', font=PATH_TITLE_FONT, color=color.dark_text,
            scale=20, origin=(0, -6), z=-1,
            parent=self
        )
        GameButton(
            text='Грати',
            scale=(3, 0.9), origin=(0, 0),
            on_click=lambda: self.screen_manager.set_active_screen("game"),
            parent=self,
        )
        GameButton(
            text='Вийти',
            scale=(3, 0.9), origin=(0, 2),
            on_click=application.quit,
            parent=self,
        )
