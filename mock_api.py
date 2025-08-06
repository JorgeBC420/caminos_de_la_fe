# Simulador de backend para pruebas locales
class MockAPI:
    def get(self, endpoint):
        return {'status': 'ok', 'data': 'fake_data'}
    def post(self, endpoint, json=None):
        return {'status': 'ok', 'data': 'fake_post'}
