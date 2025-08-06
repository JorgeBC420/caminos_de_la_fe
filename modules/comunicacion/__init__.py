# Módulo de chat y mensajería
class Comunicacion:
    def __init__(self):
        self.mails = []
        self.chats = {'hermandad': [], 'global': [], 'faccion': []}

    def enviar_mail(self, remitente, destinatario, mensaje):
        self.mails.append({'de': remitente, 'para': destinatario, 'mensaje': mensaje})

    def leer_mail(self, destinatario):
        return [m for m in self.mails if m['para'] == destinatario]

    def enviar_chat(self, canal, remitente, mensaje):
        if canal in self.chats:
            self.chats[canal].append({'de': remitente, 'mensaje': mensaje})

    def leer_chat(self, canal):
        return self.chats.get(canal, [])
# Módulo de chat y mensajería
