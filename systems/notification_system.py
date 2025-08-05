class NotificationSystem:
    def show_message(self, message):
        from ursina import Text
        notification = Text(text=message, 
                           position=(0, 0.4), 
                           background=True,
                           origin=(0,0))
        notification.fade_out(duration=1.0, delay=2.0)
