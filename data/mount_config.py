# Archivo centralizado para configuraciones de monturas (mounts)

class MountConfig:
    def __init__(self):
        self.mount_types = ['caballo', 'dragón', 'lobo']
        self.default_mount = 'caballo'

    def get_mount_types(self):
        return self.mount_types

    def set_default_mount(self, mount):
        if mount in self.mount_types:
            self.default_mount = mount

    def get_default_mount(self):
        return self.default_mount
