from systems.system import System
from components.components import *
from entities.entity import Entity

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene

class HealthSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        events = []

        for entity in entities:

            if not entity.has(Health):
                continue

            health = entity.get(Health).health

            if health <= 0:
                if entity.has(Gold, HitBy):
                    gold = entity.get(Gold).amount
                    hitBy = entity.get(HitBy).entity

                    earn_gold = Entity(self.scene)
                    earn_gold.add(EarnGoldEvent(gold, hitBy))
                    events.append(earn_gold)

                    entity.remove(HitBy)

                if entity.has(ZoneId):
                    zone = entity.get(ZoneId).id
                    farm = Entity(self.scene)
                    farm.add(FarmDestroyed(zone))
                    events.append(farm)

                if entity.has(FactionIdentity):
                    faction = entity.get(FactionIdentity).faction  

                    if faction == "ENEMY":
                        grid = self.scene.enemy_grid
                    elif faction == "PLAYER":
                        grid = self.scene.player_grid
                    elif faction == "FARM":
                        grid = self.scene.asteriod_grid
                    else:
                        continue

                    if entity.has(GridCell):
                        cells = entity.get(GridCell).cell
                        if cells is not None:
                            grid.remove_cells(entity, cells)
                            self.scene.collision_grid.remove_cells(entity, cells)

                entity.add(IsDead())
                entity.add(Destroy())


            if entity.has(Parent):
                if entity.get(Parent).entity.has(Destroy):
                    entity.add(Destroy())

        entities.extend(events)



            