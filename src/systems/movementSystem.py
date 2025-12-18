
from entities.entity import Entity

ACCELERATION = 1200
FRICTION = 1000

class MovementSystem:
    def update(self, entities: list[Entity], dt):
        player_cons = []
        
        for entity in entities:

            if entity.has_component("Position") and entity.has_component("Velocity") and entity.has_component("MovementIntent"):
                player_cons.append(entity)


        for player in player_cons:            
            position = player.get_component("Position")
            velocity = player.get_component("Velocity")
            movement_intent = player.get_component("MovementIntent")

            target_vx = movement_intent.move_x * velocity.speed
            target_vy = movement_intent.move_y * velocity.speed
        
            if movement_intent.move_x != 0:
                velocity.x = self.move_towards(velocity.x, target_vx, ACCELERATION * dt)
            else:
                velocity.x = self.move_towards(velocity.x, 0, FRICTION * dt)

            if movement_intent.move_y != 0:
                velocity.y = self.move_towards(velocity.y, target_vy, ACCELERATION * dt)
            else:
                velocity.y = self.move_towards(velocity.y, 0, FRICTION * dt)

            position.x += velocity.x * dt
            position.y += velocity.y * dt

    @staticmethod
    def move_towards(current, target, max_delta):
        if current < target:
            return min(current + max_delta, target)
        if current > target: 
            return max(current - max_delta, target)
        return target