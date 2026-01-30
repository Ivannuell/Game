class Projectile:
    __slots__ = (
        "x", "y",
        "vx", "vy",
        "faction",
        "damage",
        "alive",
        "range_left",
        "owner"
    )

    def __init__(self):
        self.alive = False

class ProjectilePool:
    def __init__(self, size):
        self.pool = [Projectile() for _ in range(size)]

    def spawn(self, x, y, vx, vy, faction, damage, max_range, owner):
        for p in self.pool:
            if not p.alive:
                p.x = x
                p.y = y
                p.vx = vx
                p.vy = vy
                p.faction = faction
                p.damage = damage
                p.range_left = max_range
                p.alive = True
                p.owner = owner
                return p
        return None

