from ursina import *

class ThirdPersonCamera:
    """
    Sistema de cámara en tercera persona con movimiento limitado
    """
    def __init__(self, target, distance=8, height=4, rotation_speed=2, sensitivity=50):
        self.target = target
        self.distance = distance
        self.height = height
        self.rotation_speed = rotation_speed
        self.sensitivity = sensitivity
        
        # Ángulos de la cámara
        self.yaw = 0
        self.pitch = -20
        
        # Límites de pitch para evitar que la cámara se voltee
        self.min_pitch = -45
        self.max_pitch = 15
        
        # Control de ratón
        self.mouse_sensitivity = 0.5
        self.right_mouse_pressed = False
        
        # Configurar cámara inicial
        self.update_camera_position()
        
    def update_camera_position(self):
        """Actualiza la posición de la cámara basada en los ángulos actuales"""
        # Calcular posición de la cámara
        offset_x = self.distance * math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        offset_z = self.distance * math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        offset_y = self.distance * math.sin(math.radians(self.pitch)) + self.height
        
        camera.position = self.target.position + Vec3(offset_x, offset_y, offset_z)
        camera.look_at(self.target.position + Vec3(0, 1, 0))
        
    def input(self, key):
        """Maneja la entrada del ratón para rotación de cámara"""
        if key == 'right mouse down':
            self.right_mouse_pressed = True
            mouse.locked = True
            
        elif key == 'right mouse up':
            self.right_mouse_pressed = False
            mouse.locked = False
            
    def update(self):
        """Actualiza la cámara cada frame"""
        # Solo rotar si el botón derecho está presionado
        if self.right_mouse_pressed:
            # Rotar basado en movimiento del ratón
            self.yaw += mouse.velocity[0] * self.mouse_sensitivity
            self.pitch -= mouse.velocity[1] * self.mouse_sensitivity
            
            # Limitar pitch
            self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch))
            
        # Actualizar posición de cámara
        self.update_camera_position()
        
    def set_target(self, new_target):
        """Cambia el objetivo de la cámara"""
        self.target = new_target
