from components.components import *
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene
    from entities.entity import Entity

from icecream import ic

class Grid_IndexSystem(System):
    def update(self, entities, dt):
        grid = self.scene._grid

        for e in entities:
            if not e.has(Position, Collider, GridCell):
                continue

            pos = e.get(Position)
            col = e.get(Collider)
            gc = e.get(GridCell)

            new_cells = grid.compute_cells(pos, col)

            if new_cells != gc.cells:
                grid.remove(e, gc.cells)
                grid.insert(e, new_cells)
                gc.cells = new_cells



class _Grid_CleanupSystem(System):
    def __init__(self, scene):
        super().__init__(scene)
        self.time = 0

    def update(self, entities, dt):
        for e in entities:
            if not e.has(GridCell):
                continue

            gc = e.get(GridCell)

            if not gc.alive and gc.by_grid:
                for grid, cells in gc.by_grid.items():
                    grid.remove(e, cells)

                gc.by_grid.clear()

        self.time += dt
        if self.time >= 1:
            print("collision grid cells:", sum(len(v) for v in self.scene.collision_grid.cells.values()))
            print("entities:", len(entities))
            self.time = 0




class _Grid_IndexSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

    def update(self, entities, dt):
        # self.scene.collision_grid.cells = {}

        for e in entities:
            if not e.has(Position, Collider, GridCell):
                continue

            pos = e.get(Position)
            col = e.get(Collider)
            gc  = e.get(GridCell)

            # Decide which grids this entity belongs to
            grids = []

            grids.append(self.scene.collision_grid)

            for grid in grids:
                new_cells = grid.compute_cells(pos, col)
                old_cells = gc.by_grid.get(grid)

                if old_cells is None:
                    grid.insert_cells(e, new_cells)
                elif new_cells != old_cells:
                    grid.remove_cells(e, old_cells)
                    grid.insert_cells(e, new_cells)

                gc.by_grid[grid] = new_cells