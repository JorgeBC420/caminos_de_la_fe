from ursina import *
from data.mount_data import MOUNT_DATA

class MountManager:
    def __init__(self, player):
        self.player = player
        self.owned_mounts = ['corcel_de_guerra_aethelgardia']
        self.active_mount_instance = None

    def summon_mount(self, mount_key):
        if self.active_mount_instance:
            return

        if mount_key in self.owned_mounts:
            print(f"Llamando a {mount_key}...")
            data = MOUNT_DATA[mount_key]
            self.active_mount_instance = Entity(
                model=data['model'],
                position=self.player.position + self.player.back * 2,
                rotation=self.player.rotation
            )
            self.mount_player()

    def mount_player(self):
        if not self.active_mount_instance:
            return

        self.player.visible = False
        self.player.parent = self.active_mount_instance
        self.player.position = (0, 1.2, -0.2)
        self.player.state = 'mounted'
        self.active_mount_instance.speed = MOUNT_DATA[self.player.active_mount_key]['speed']

    def dismount_player(self):
        if not self.active_mount_instance or self.player.state != 'mounted':
            return

        self.player.parent = scene
        self.player.position = self.active_mount_instance.position + self.active_mount_instance.right * 2
        self.player.visible = True
        self.player.state = 'walking'

        destroy(self.active_mount_instance)
        self.active_mount_instance = None
