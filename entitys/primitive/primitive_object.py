from ursina import Entity


class PrimitiveObject(Entity):
    def __init__(self, model, texture=None, position=(0, 0.5, 0), scale=(1, 1, 1), collider='box', name="Primitive",
                 **kwargs):
        super().__init__(
            model=model,
            texture=texture,
            position=position,
            scale=scale,
            collider=collider,
            name=name,
            **kwargs
        )
