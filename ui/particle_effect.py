from ursina import Entity, TexturedQuad, color

class ParticleEffect(Entity):
    def __init__(self, texture_path, position, duration=1.0):
        super().__init__()
        self.model = TexturedQuad(texture=texture_path)
        self.position = position
        self.color = color.white
        self.fade_out(duration=duration)
