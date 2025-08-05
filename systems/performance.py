class ObjectPool:
    def __init__(self, entity_type, count):
        self.pool = [entity_type() for _ in range(count)]
    
    def get_entity(self):
        for entity in self.pool:
            if not entity.enabled:
                return entity
        return self.pool[0].clone()
