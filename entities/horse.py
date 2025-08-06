class Horse:
    def __init__(self, name, stats=None):
        self.name = name
        self.stats = stats or {'velocidad': 10, 'defensa': 5}
