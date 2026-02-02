
class EntityManager:
    def __init__(self, entities):
        self.entities = entities
        self.to_add = []
        self.to_remove = set()

    def add(self, entity):
        self.to_add.append(entity)
    
    def remove(self, entity):
        self.to_remove.add(entity)

    def commit(self):
        self.entities = [ e for e in self.entities if e not in self.to_remove]
        self.to_remove.clear()

        self.entities.extend(self.to_add)
        self.to_add.clear()

