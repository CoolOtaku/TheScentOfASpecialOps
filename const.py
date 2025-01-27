import re
from typing import Final

from ursina import destroy

PATH_TITLE_FONT: Final[str] = 'assets/fonts/phorssa.ttf'
PATH_TEXT_FONT: Final[str] = 'assets/fonts/paneuropa_crash_barrier.ttf'

PATH_BACKGROUND_TEXTURE: Final[str] = 'assets/textures/other/background.jpg'
PATH_BUTTON_TEXTURE: Final[str] = 'assets/textures/other/button_background.png'
PATH_WINDOW_TEXTURE: Final[str] = 'assets/textures/other/window_background.png'

PATH_WEAPON_MODELS: Final[str] = 'assets/models/weapons/'
PATH_WEAPON_SOUNDS: Final[str] = 'assets/sound/weapons/'

PATH_HOUSES_MODELS: Final[str] = 'assets/models/maps/houses/'
PATH_HOUSES_TEXTURES: Final[str] = 'assets/textures/maps/houses/'

def get_anim_duration(actor, name) -> float:
    return actor.getNumFrames(name) / actor.getFrameRate(name)

def validate_input_entity_property(value):
    if re.fullmatch(r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){2}$', value):
        return True
    return False

def destroy_entity(entity):
    name = entity.__class__.__name__
    try:
        entity.disable()
    except Exception as e:
        print(f'Виникла помилка при відключенні сутності: {e}, Сутність: {name}')
    try:
        destroy(entity)
    except Exception as e:
        print(f'Виникла помилка при видаленні сутності: {e}, Сутність: {name}')
    del entity

def destroy_list(list_entity):
    name = list_entity.__class__.__name__
    for item in list_entity:
        destroy_entity(item)

    list_entity.clear()
    try:
        list_entity.disable()
    except Exception as e:
        print(f'Виникла помилка при відключенні списку: {e}, Сутність: {name}')
    try:
        destroy(list_entity)
    except Exception as e:
        print(f'Виникла помилка при видаленні списку: {e}, Сутність: {name}')
    del list_entity

def destroy_dict(dict_entity):
    name = dict_entity.__class__.__name__
    for key, item in dict_entity.items():
        destroy_entity(item)

    dict_entity.clear()
    try:
        dict_entity.disable()
    except Exception as e:
        print(f'Виникла помилка при відключенні словника: {e}, Сутність: {name}')
    try:
        destroy(dict_entity)
    except Exception as e:
        print(f'Виникла помилка при видаленні словника: {e}, Сутність: {name}')
    del dict_entity
