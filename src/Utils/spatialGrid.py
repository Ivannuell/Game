from components.components import Position


class SpatialGrid:
    def __init__(self, cell_size):
        self.cells = {}
        self.cell_size = cell_size

    def cell_coords(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def compute_cells(self, pos, col):
        min_x = pos.x - col.width * 0.5
        max_x = pos.x + col.width * 0.5
        min_y = pos.y - col.height * 0.5
        max_y = pos.y + col.height * 0.5

        cx1, cy1 = self.cell_coords(min_x, min_y)
        cx2, cy2 = self.cell_coords(max_x, max_y)

        cells = set()
        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                cells.add((cx, cy))

        return tuple(cells)

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

    # QUERRY METHODS
    def query_neighbors(self, posx, posy):
        cx, cy = self.cell_coords(posx, posy)

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                yield from self.cells.get((cx + dx, cy + dy), [])

    def query_point(self, posx, posy):
        return self.cells.get(self.cell_coords(posx, posy), ())
    

    def find_nearest(
        self,
        x, y,
        min_radius=0,
        require_component=None,
        predicate=None
    ):
        cx, cy = self.cell_coords(x, y)

        nearest = None
        nearest_dist_sq = float("inf")

        r = min_radius

        while True:
            found_in_ring = False

            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):

                    # outer ring only
                    if abs(dx) != r and abs(dy) != r:
                        continue

                    cell = self.cells.get((cx + dx, cy + dy))
                    if not cell:
                        continue

                    for e in cell:
                        # ---- FILTERS ----
                        if require_component and not e.has(require_component):
                            continue

                        if predicate and not predicate(e):
                            continue
                        # ------------------

                        pos = e.get(Position)
                        d2 = (pos.x - x) ** 2 + (pos.y - y) ** 2

                        if d2 < nearest_dist_sq:
                            nearest = e
                            nearest_dist_sq = d2
                            found_in_ring = True

            # 🔑 Stop only when we found something VALID
            if found_in_ring:
                return nearest

            r += 1
