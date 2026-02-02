
class EntityManager:
    def __init__(self, entities):
        self.entities = entities
        self._to_add = []
        self._to_remove = set()

    def add(self, entity):
        self._to_add.append(entity)
    
    def remove(self, entity):
        self._to_remove.add(entity)

    def commit(self):
        self.entities[:] = [e for e in self.entities if e not in self._to_remove]
        self._to_remove.clear()

        self.entities.extend(self._to_add)
        self._to_add.clear()

