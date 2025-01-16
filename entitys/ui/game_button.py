from ursina import Button, color

from const import PATH_TEXT_FONT, PATH_BUTTON_TEXTURE


class GameButton(Button):
    def __init__(self, icon_texture=None, is_small=False, **kwargs):
        super().__init__(
            texture=PATH_BUTTON_TEXTURE,
            color=color.white, z=-1,
            scale=(3 if not is_small else 0.6, 0.9 if not is_small else 0.18),
            **kwargs
        )
        if self.text_entity:
            self.text_entity.font = PATH_TEXT_FONT
            self.text_entity.color = color.white

        if icon_texture:
            self.icon = icon_texture
            self.icon.scale = 0.6
            self.scale = 0.9

        self.start_scale = self.scale
        self.hovered = False
        self.is_hovered = self.hovered

    def update(self):
        if self.hovered and self.hovered != self.is_hovered:
            self.scale = self.start_scale * 1.1
            if self.text_entity: self.text_color = color.orange
            if self.icon: self.icon.color = color.red
            self.is_hovered = self.hovered
        elif not self.hovered and self.hovered != self.is_hovered:
            self.scale = self.start_scale
            if self.text_entity: self.text_color = color.white
            if self.icon: self.icon.color = color.white
            self.is_hovered = self.hovered
