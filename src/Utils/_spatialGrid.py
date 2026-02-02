from components.components import Position


class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}
        self.entity_count = 0

    def clear(self):
        for cell in self.cells.values():
            cell.clear()
        self.cells.clear()

    def world_to_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def insert(self, entity, cell):
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(entity)

    def remove(self, entity, cell):
        bucket = self.cells.get(cell)
        if not bucket:
            return

        try:
            bucket.remove(entity)
        except ValueError:
            pass

        if not bucket:
            del self.cells[cell]

    def insert_cells(self, entity, cells):
        for cell in cells:
            self.cells.setdefault(cell, []).append(entity)

    def _remove_cells(self, entity, cells):
        for cell in cells:
            bucket = self.cells.get(cell)
            if not bucket:
                continue

            try:
                bucket.remove(entity)
            except ValueError:
                pass

            if not bucket:
                del self.cells[cell]

    def remove_cells(self, entity, cells):
        if not cells:
            return

        for cell in cells:
            lst = self.cells.get(cell)
            if not lst:
                continue

            new_lst = [e for e in lst if e is not entity]

            if new_lst:
                self.cells[cell] = new_lst
            else:
                del self.cells[cell]




    def compute_cells(self, pos, collider):
        min_x = pos.x - collider.width * 0.5
        max_x = pos.x + collider.width * 0.5
        min_y = pos.y - collider.height * 0.5
        max_y = pos.y + collider.height * 0.5

        cx1, cy1 = self.cell_coords(min_x, min_y)
        cx2, cy2 = self.cell_coords(max_x, max_y)

        cells = set()
        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                cells.add((cx, cy))

        return tuple(cells)




    def get_Candidates(self):
        return [(pos, entity) for pos, entity in self.cells.items()]

    def cell_coords(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def _insert(self, entity, pos, collider):
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
        return self.cells.get(self.cell_coords(posx, posy), ())


    def query_range(self, posx: int, posy: int, radius: int):
        """
        This takes position x and y of the origin and look for entities in radius away.
        \n
        note: This can run multiple times in a loop as it returns a generator
        """
        cx, cy = self.cell_coords(posx, posy)

        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                distance = (dx*dx + dy*dy) ** 0.5

                if distance <= radius:
                    yield from self.cells.get((cx + dx, cy + dy), [])

    def query_range_dynamic(self, posx, posy, radius):
        """
        This takes position x and y of the origin and look for entities starting with the given radius until it finds a target
        """
        cx, cy = self.cell_coords(posx, posy)
        nearest = None
        nearest_dist_sq = float("inf")

        while True:
            r = radius
            for dx in range(-r, r+1):
                for dy in range(-r, r+1):
                    # distance = (dx*dx + dy*dy) ** 0.5

                    if abs(dx) != r and abs(dy) != r:
                        continue

                    cell = self.cells.get((cx + dx, cy + dy))
                    if not cell:
                        continue

                    for e in cell:
                        ex, ey = e.get(Position).x, e.get(Position).y
                        d2 = (ex - posx) ** 2 + (ey - posy) ** 2

                        if d2 < nearest_dist_sq:
                            nearest = e
                            nearest_dist_sq = d2
            
            if nearest is not None:
                break
            r += 1
        return nearest

    def find_nearest(
        self,
        x, y,
        max_radius=1000,
        require_component=None,
        predicate=None
    ):
        cx, cy = self.cell_coords(x, y)

        nearest = None
        nearest_dist_sq = float("inf")

        for r in range(max_radius + 1):
            found_in_ring = False

            for dx in range(-r, r + 1):
                for dy in (-r, r + 1):

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

            # Early exit only if we found a VALID entity in this ring
            if found_in_ring:
                break

        return nearest




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
