import Game
import math
import MathUtil

colliders_in_game = []
collision_pairs = []
use_equations = True

class Collider:
    """Base class for all colliders"""
    def __init__(self, game_object):
        self.game_object = game_object
        colliders_in_game.append(self)

    def get_pos(self):
        """Return the position of game_object attached to the collider"""
        return self.game_object.pos

    def on_collision(self, other):
        """Called when the collider collides with another collider"""
        pass

    def delete(self):
        """Remove collider from the physics engine"""
        colliders_in_game.remove(self)

class BoxCollider(Collider):
    """A collider that represents a box"""
    def __init__(self, game_object, size=None):
        super().__init__(game_object)
        if size is None:
            size = game_object.size
        self.size = size


class CircleCollider(Collider):
    """A collider that represents a circle"""
    def __init__(self, game_object, radius=None):
        super().__init__(game_object)
        if radius is None:
            self.radius = (game_object.size[0] + game_object.size[1]) / 2 / 2  # approximate size with width and height
        else:
            self.radius = radius


def AABB_collision(pos1, size1, pos2, size2):
    """Check if two boxes are colliding"""
    return pos1[0] - size1[0] / 2 < pos2[0] + size2[0] / 2 and pos1[0] + size1[0] / 2 > pos2[0] - size2[0] / 2 and pos1[
        1] - size1[1] / 2 < pos2[1] + size2[1] / 2 and pos1[1] + size1[1] / 2 > pos2[1] - size2[1] / 2


def circle_collision(pos1, radius1, pos2, radius2):
    """Check if two circles are colliding"""
    return (pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2 < (radius1 + radius2) ** 2


def get_box_collider_penetration(box_collider1: BoxCollider, boc_collider2: BoxCollider):
    """Return the penetration of two box colliders"""
    return get_box_penetration(box_collider1.get_pos(), box_collider1.size, boc_collider2.get_pos(), boc_collider2.size)


def get_box_penetration(pos1, size1, pos2, size2):
    """Return the penetration of two boxes"""
    y_penetration = 0
    x_penetration = 0
    if pos1[1] - size1[1] / 2 < pos2[1] + size2[1] / 2 and pos1[1] + size1[1] / 2 > pos2[1] - size2[1] / 2:
        if pos1[1] < pos2[1]:
            y_penetration = (pos1[1] + size1[1] / 2) - (pos2[1] - size2[1] / 2)
        else:
            y_penetration = (pos1[1] - size1[1] / 2) - (pos2[1] + size2[1] / 2)
    if pos1[0] - size1[0] / 2 < pos2[0] + size2[0] / 2 and pos1[0] + size1[0] / 2 > pos2[0] - size2[0] / 2:
        if pos1[0] < pos2[0]:
            x_penetration = (pos1[0] + size1[0] / 2) - (pos2[0] - size2[0] / 2)
        else:
            x_penetration = (pos1[0] - size1[0] / 2) - (pos2[0] + size2[0] / 2)
    if abs(x_penetration) < abs(y_penetration):
        return x_penetration, 0
    else:
        return 0, y_penetration

    return x_penetration, y_penetration


def get_circle_collider_penetration(circle_collider1: CircleCollider, circle_collider2: CircleCollider):
    """Return the penetration of two circle colliders"""
    return get_circle_penetration(circle_collider1.get_pos(), circle_collider1.radius, circle_collider2.get_pos(),
                                  circle_collider2.radius)


def get_circle_penetration(pos1, radius1, pos2, radius2):
    """Return the penetration of two circles"""
    x_penetration = 0
    y_penetration = 0
    if circle_collision(pos1, radius1, pos2, radius2):
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        current_distance = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        x_penetration = ((radius1 + radius2) - current_distance) * math.cos(angle)
        y_penetration = ((radius1 + radius2) - current_distance) * math.sin(angle)
    return x_penetration, y_penetration


def is_colliding(collider1: Collider, collider2: Collider):
    """Check if two colliders are colliding"""
    colliding = False
    if isinstance(collider1, BoxCollider) and isinstance(collider2, BoxCollider):
        colliding = AABB_collision(collider1.get_pos(), collider1.size, collider2.get_pos(), collider2.size)
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, CircleCollider):
        colliding = circle_collision(collider1.get_pos(), collider1.radius, collider2.get_pos(), collider2.radius)
    # Circle and Box collision is approximated with the circle being interpreted as a box
    elif isinstance(collider1, BoxCollider) and isinstance(collider2, CircleCollider):
        colliding = AABB_collision(collider1.get_pos(), collider1.size, collider2.get_pos(),
                              (collider2.radius * 2, collider2.radius * 2))
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, BoxCollider):
        colliding = AABB_collision(collider1.get_pos(), (collider1.radius * 2, collider1.radius * 2), collider2.get_pos(),
                              collider2.size)
    if colliding:
        pass
    return colliding


def get_penetration(collider1: Collider, collider2: Collider):
    """Return the penetration of two colliders"""
    if isinstance(collider1, BoxCollider) and isinstance(collider2, BoxCollider):
        return get_box_collider_penetration(collider1, collider2)
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, CircleCollider):
        return get_circle_collider_penetration(collider1, collider2)
    # Circle and Box collision is approximated with the circle being interpreted as a box
    elif isinstance(collider1, BoxCollider) and isinstance(collider2, CircleCollider):
        return get_box_penetration(collider1.get_pos(), collider1.size, collider2.get_pos(),
                                   (collider2.radius * 2, collider2.radius * 2))
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, BoxCollider):
        return get_box_penetration(collider1.get_pos(), (collider1.radius * 2, collider1.radius * 2),
                                   collider2.get_pos(), collider2.size)


def get_collider_colliding(collider: Collider, colliders: list) -> list:
    """Return a list of colliders colliding with the collider"""
    collider_colliding = []
    for c in colliders:
        if is_colliding(collider, c):
            collider_colliding.append(c)
    return collider_colliding


def get_penetration_with_all(collider: Collider, colliders: list) -> list:
    """Return a list of penetration of the collider with all the colliders"""
    penetration = []
    for c in colliders:
        if is_colliding(collider, c):
            penetration.append(get_penetration(collider, c))
    return penetration


class DynamicCollider:
    """A collider that can move and collide with other colliders"""
    def __init__(self, game_object: Game.GameObject):
        self.game_object = game_object
        self.static = False
        self.initial_velocity = (0, 0)
        self.initial_acceleration = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.air_friction = 0
        self.ground_friction = 0
        self.mass = 1
        self.bounciness = 0
        self.collider = None
        self.collisions = []
        self.on_collision = []

    def register_on_collision(self, function):
        """Register a function to be called when the collider collides with another collider"""
        self.on_collision.append(function)

    def unregister_on_collision(self, function):
        """Unregister a function to be called when the collider collides with another collider"""
        self.on_collision.remove(function)

    def set_collider(self, collider: list):
        """Set the current collider (circle or box) of the dynamic collider"""
        if self.collider is not None:
            self.collider.delete()
        self.collider = collider

    def get_collider(self):
        """Return the collider of the dynamic collider"""
        return self.collider

    def update_dynamic(self):
        """Update the dynamic collider"""
        if self.static:
            return
        self.velocity = (self.velocity[0] + self.acceleration[0] * Game.timeStep,
                         self.velocity[1] + self.acceleration[1] * Game.timeStep)

        if use_equations:
            newPosx = self.game_object.pos[0] + self.velocity[0] * Game.timeStep + (self.acceleration[0] * Game.timeStep ** 2) / 2
            newPosy = self.game_object.pos[1] + self.velocity[1] * Game.timeStep + (self.acceleration[1] * Game.timeStep ** 2) / 2
            self.game_object.pos = (newPosx, newPosy)
        else:
            self.game_object.pos = (self.game_object.pos[0] + self.velocity[0] * Game.timeStep,
                                    self.game_object.pos[1] + self.velocity[1] * Game.timeStep)

        self.velocity = (self.velocity[0] * (1 - self.air_friction * Game.timeStep),
                         self.velocity[1] * (1 - self.air_friction * Game.timeStep))

    def update(self):
        """Update the dynamic collider (called by the game object)"""
        if self.collider is not None:
            if len(self.collisions) > 0:
                self._on_collision(self.collisions, False)

    def delete(self):
        """Delete the dynamic collider"""
        if self.collider is not None:
            self.collider.delete()

    def _on_collision(self, objects_colliding, should_resolve=True):
        """Called when the collider collides with another collider"""
        if should_resolve:
            for collider in objects_colliding:
                if isinstance(collider.game_object, Game.Body):
                    self._resolve_collision(collider.game_object.dynamic_collider)
        for function in self.on_collision:
            function(self.game_object, objects_colliding)

    def get_collisions(self) -> list:
        """Return the current colliding colliders of the dynamic collider"""
        return self.collisions

    def _set_collisions(self, collisions: list):
        """Set the current colliding colliders of the dynamic collider"""
        self.collisions = collisions

    def get_penetration(self, colliders):
        """Return the penetration of the collider with the colliders"""
        penetrations = get_penetration_with_all(self.collider, colliders)
        penetration_sum = (0, 0)
        for p in penetrations:
            penetration_sum = (penetration_sum[0] + p[0], penetration_sum[1] + p[1])
        return penetration_sum

    def _resolve_collision(self, collider):
        """Resolve the collision with the collider"""
        solve_constraints(self, collider)



def solve_constraints(collider1: Collider, collider2: Collider): # with energy conservation
    """Solve the constraints between the two colliders"""
    dynamic_collider1 = get_dynamic_collider(collider1.game_object)
    dynamic_collider2 = get_dynamic_collider(collider2.game_object)
    if dynamic_collider1.static:
        if dynamic_collider2.static:
            return
        else:
            solve_constraints(dynamic_collider2, dynamic_collider1)
    penetration = get_penetration(dynamic_collider1.collider, dynamic_collider2.collider)

    if not dynamic_collider2.static:
        velocity1 = dynamic_collider1.velocity
        velocity2 = dynamic_collider2.velocity
        projected_velocity1 = MathUtil.project_vector(velocity1, penetration)
        projected_velocity1 = (projected_velocity1[0], projected_velocity1[1])
        projected_velocity2 = MathUtil.project_vector(velocity2, penetration)

        # https://www.vobarian.com/collisions/2dcollisions2.pdf

        final_velocity1x = (projected_velocity1[0] * (dynamic_collider1.mass - dynamic_collider2.mass) + projected_velocity2[0] * 2 * dynamic_collider2.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity1y = (projected_velocity1[1] * (dynamic_collider1.mass - dynamic_collider2.mass) + projected_velocity2[1] * 2 * dynamic_collider2.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity1 = (final_velocity1x * dynamic_collider1.bounciness, final_velocity1y * dynamic_collider1.bounciness)
        final_velocity2x = (projected_velocity2[0] * (dynamic_collider2.mass - dynamic_collider1.mass) + projected_velocity1[0] * 2 * dynamic_collider1.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity2y = (projected_velocity2[1] * (dynamic_collider2.mass - dynamic_collider1.mass) + projected_velocity1[1] * 2 * dynamic_collider1.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity2 = (final_velocity2x * dynamic_collider2.bounciness, final_velocity2y * dynamic_collider2.bounciness)

        dynamic_collider1.velocity = dynamic_collider1.velocity[0] + final_velocity1[0] - projected_velocity1[0], dynamic_collider1.velocity[1] + final_velocity1[1] - projected_velocity1[1]
        dynamic_collider2.velocity = dynamic_collider2.velocity[0] + final_velocity2[0] - projected_velocity2[0], dynamic_collider2.velocity[1] + final_velocity2[1] - projected_velocity2[1]

        dynamic_collider1.game_object.pos = (dynamic_collider1.game_object.pos[0] - penetration[0] / 2, dynamic_collider1.game_object.pos[1] - penetration[1] / 2)
        dynamic_collider2.game_object.pos = (dynamic_collider2.game_object.pos[0] + penetration[0] / 2, dynamic_collider2.game_object.pos[1] + penetration[1] / 2)

    else:
        projected_penetration_velocity = MathUtil.project_vector(dynamic_collider1.velocity, penetration)
        dynamic_collider1.velocity = (dynamic_collider1.velocity[0] + -projected_penetration_velocity[0] * (1 + dynamic_collider1.bounciness), dynamic_collider1.velocity[1] + -projected_penetration_velocity[1] * (1 + dynamic_collider1.bounciness))

        dynamic_collider1.game_object.pos = (dynamic_collider1.game_object.pos[0] - penetration[0], dynamic_collider1.game_object.pos[1] - penetration[1])


def reset():
    """Reset the physic system"""
    colliders_in_game.clear()

def get_dynamic_collider(game_object):
    """Return the dynamic collider of the game object"""
    if game_object.dynamic_collider is not None:
        return game_object.dynamic_collider
    return None

def update(timeStep):
    """Update the physic system"""
    #clear previous collisions
    collision_pairs.clear()
    for collider in colliders_in_game:
        get_dynamic_collider(collider.game_object).collisions.clear()

    #update positions
    for collider in colliders_in_game:
        dynamic_collider = get_dynamic_collider(collider.game_object)
        if dynamic_collider is not None:
            dynamic_collider.update_dynamic()

    #detect collisions
    for i in range(len(colliders_in_game)):
        dynCollider1 = get_dynamic_collider(colliders_in_game[i].game_object)
        for j in range(i + 1, len(colliders_in_game)):
            dynCollider2 = get_dynamic_collider(colliders_in_game[j].game_object)
            if collision_pairs.__contains__((colliders_in_game[i], colliders_in_game[j])) or collision_pairs.__contains__((colliders_in_game[j], colliders_in_game[i])):
                continue
            if is_colliding(colliders_in_game[i], colliders_in_game[j]):
                collision_pairs.append((colliders_in_game[i], colliders_in_game[j]))
                dynCollider1.collisions.append(colliders_in_game[j])
                dynCollider2.collisions.append(colliders_in_game[i])

    #resolve collisions
    for collision_pair in collision_pairs:
        solve_constraints(collision_pair[0], collision_pair[1])