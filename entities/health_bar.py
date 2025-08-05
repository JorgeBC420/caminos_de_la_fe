from ursina import *

class HealthBar(Entity):
    def __init__(self, target, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.parent = camera.ui
        self.model = 'cube'
        self.color = color.red
        self.scale = (0.2, 0.02, 1)
        self.position = (0, 0.4, 0)
        
        # Fondo de la barra de vida
        self.background = Entity(
            parent=self,
            model='cube',
            color=color.dark_gray,
            scale=(1.1, 1.1, 0.9),
            z=0.01
        )
    
    def update(self):
        if hasattr(self.target, 'health') and hasattr(self.target, 'max_health'):
            # Actualizar la escala basada en la salud actual
            health_ratio = max(0, self.target.health / self.target.max_health)
            self.scale_x = 0.2 * health_ratio
            
            # Cambiar color basado en la salud
            if health_ratio > 0.6:
                self.color = color.green
            elif health_ratio > 0.3:
                self.color = color.yellow
            else:
                self.color = color.red
        
        # Mantener la posición relativa al objetivo
        if self.target:
            screen_pos = camera.world_to_screen_point(self.target.position + Vec3(0, 2, 0))
            if screen_pos.z > 0:  # Solo mostrar si está en frente de la cámara
                self.position = (screen_pos.x, screen_pos.y, 0)
                self.visible = True
            else:
                self.visible = False

health_bar = HealthBar  # Alias para compatibilidad
