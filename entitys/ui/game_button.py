from ursina import Button, color

from const import PATH_TEXT_FONT, PATH_BUTTON_TEXTURE

class GameButton(Button):
    def __init__(self, **kwargs):
        super().__init__(
            font=PATH_TEXT_FONT, text_color=color.white, texture=PATH_BUTTON_TEXTURE,
            color=color.white, z=-1,
            **kwargs
        )
        self.start_scale = self.scale
        self.hovered = False
        self.is_hovered = self.hovered

    def update(self):
        if self.hovered and self.hovered != self.is_hovered:
            self.scale = self.start_scale * 1.1
            self.text_color = color.orange
            self.is_hovered = self.hovered
        elif not self.hovered and self.hovered != self.is_hovered:
            self.scale = self.start_scale
            self.text_color = color.white
            self.is_hovered = self.hovered
