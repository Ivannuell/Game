class SpatialGrid:
    def __init__(self, cell_size):
        self.cells = {}

    def insert(self, e, cells):
        for c in cells:
            self.cells.setdefault(c, set()).add(e)

    def remove(self, e, cells):
        for c in cells:
            bucket = self.cells.get(c)
            if bucket:
                bucket.discard(e)
                if not bucket:
                    del self.cells[c]
