from typing import Final

PATH_TITLE_FONT: Final[str] = 'assets/fonts/phorssa.ttf'
PATH_TEXT_FONT: Final[str] = 'assets/fonts/paneuropa_crash_barrier.ttf'

PATH_BACKGROUND_TEXTURE: Final[str] = 'assets/textures/other/background.jpg'
PATH_BUTTON_TEXTURE: Final[str] = 'assets/textures/other/button_background.png'

def get_anim_duration(actor, name) -> float:
    return actor.getNumFrames(name) / actor.getFrameRate(name)
