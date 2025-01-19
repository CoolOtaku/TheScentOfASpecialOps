from ursina import Entity


class PrimitiveObject(Entity):
    def __init__(self, model, texture, position, scale, name, **kwargs):
        super().__init__(
            model=model,
            texture=texture,
            position=position,
            scale=scale,
            name=name,
            collider='box',
            **kwargs
        )
