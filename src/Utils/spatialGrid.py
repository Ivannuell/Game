class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}
        self.entity_count = 0

    def clear(self):
        self.cells.clear()

    def get_Candidates(self):
        return [(pos, entity) for pos, entity in self.cells.items()]

    def cell_coords(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def insert(self, entity, pos, collider):
        min_x = pos.x - collider.width / 2
        max_x = pos.x + collider.width / 2
        min_y = pos.y - collider.height / 2
        max_y = pos.y + collider.height / 2

        cx1, cy1 = self.cell_coords(min_x, min_y)
        cx2, cy2 = self.cell_coords(max_x, max_y)

        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                self.cells.setdefault((cx, cy), []).append(entity)

                
    def query_neighbors(self, posx, posy):
        cx, cy = self.cell_coords(posx, posy)

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                yield from self.cells.get((cx + dx, cy + dy), [])
    
    def query_point(self, posx, posy):
        cx, cy = self.cell_coords(posx, posy)

        return self.cells.get((cx, cy), [])

    def query_range(self, posx, posy, radius):
        cx, cy = self.cell_coords(posx, posy)

        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                distance = (dx*dx + dy*dy) ** 0.5

                if distance <= radius:
                    yield from self.cells.get((cx + dx, cy + dy), [])

    def query_range_ip(self, posx, posy, radius):
        candidates = []
        cx, cy = self.cell_coords(posx, posy)

        def distance_(dx, dy):
            return (dx*dx + dy*dy) ** 0.5

        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                distance = distance_(dx, dy)

                if distance <= radius:
                    candidates.append(self.cells.get((cx + dx, cy + dy), []))
        return candidates
