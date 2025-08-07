from ursina import *

class ProfileScene(Entity):
    def __init__(self, player):
        """Initialize the ProfileScene with the player's data.

        Args:
            player: The player entity containing model and texture information.
        """
        super().__init__()
        self.player = player
        # Entorno 3D
        self.sky = Sky()
        self.ground = Entity(model='plane', scale=100, texture='grass', texture_scale=(10,10))
        # Modelo del jugador
        self.player_model = Entity(
            model=self.player.model,
            texture=self.player.texture,
            scale=self.player.scale,
            position=(0, 0, 0),
            rotation=(0, 180, 0)
        )
        self.player_model.animate_rotation((0, 360, 0), duration=10, loop=True)
        self.load_home()
        # Cámara fija
        self.camera = EditorCamera(enabled=False)
        self.camera_pivot = Entity()
        self.camera.parent = self.camera_pivot
        self.camera_pivot.position = (0, 2, -5)
        self.camera_pivot.rotation_x = 15
        self.camera_pivot.rotation_y = 0
        self.camera_pivot.rotation_z = 0

    def load_home(self):
        home_level = getattr(self.player, 'home_level', 1)
        home_model = f'assets/homes/level_{home_level}.glb'
        self.home = Entity(model=home_model, position=(10, 0, 10), scale=3)
