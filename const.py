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

def get_anim_duration(actor, name) -> float:
    return actor.getNumFrames(name) / actor.getFrameRate(name)

def validate_input_entity_property(value):
    if re.fullmatch(r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){2}$', value):
        return True
    return False

def destroy_entity(entity):
    try:
        entity.disable()
    except Exception as e:
        print(f'Виникла помилка при відключенні сутності: {e}')
    destroy(entity)
    del entity

def destroy_list(list_entity):
    for item in list_entity:
        try:
            item.disable()
        except Exception as e:
            print(f'Виникла помилка при відключенні елемента списку: {e}')
        try:
            destroy(item)
        except Exception as e:
            print(f'Виникла помилка при видаленні елемента списку: {e}')
        del item
    try:
        list_entity.disable()
    except Exception as e:
        print(f'Виникла помилка при відключенні списку: {e}')
    list_entity.clear()
    destroy(list_entity)
    del list_entity


def destroy_dict(dict_entity):
    for key, value in dict_entity.items():
        try:
            value.disable()
        except Exception as e:
            print(f'Виникла помилка при відключенні елемента {key}: {e}')
        try:
            destroy(value)
        except Exception as e:
            print(f'Виникла помилка при видаленні елемента {key}: {e}')

    dict_entity.clear()
    try:
        destroy(dict_entity)  # Знищуємо словник, якщо можливо
    except Exception as e:
        print(f'Виникла помилка при видаленні словника: {e}')
    del dict_entity
