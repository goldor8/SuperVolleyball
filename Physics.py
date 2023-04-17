import Game
import math
import MathUtil

colliders_in_game = []


class Collider:
    def __init__(self, game_object):
        self.game_object = game_object
        colliders_in_game.append(self)

    def get_pos(self):
        return self.game_object.pos

    def on_collision(self, other):
        pass


class BoxCollider(Collider):
    def __init__(self, game_object, size=None):
        super().__init__(game_object)
        if size is None:
            size = game_object.size
        self.size = size


class CircleCollider(Collider):
    def __init__(self, game_object, radius=None):
        super().__init__(game_object)
        if radius is None:
            self.radius = (game_object.size[0] + game_object.size[1]) / 2 / 2  # approximate size with width and height
        else:
            self.radius = radius


def AABB_collision(pos1, size1, pos2, size2):
    return pos1[0] - size1[0] / 2 < pos2[0] + size2[0] / 2 and pos1[0] + size1[0] / 2 > pos2[0] - size2[0] / 2 and pos1[
        1] - size1[1] / 2 < pos2[1] + size2[1] / 2 and pos1[1] + size1[1] / 2 > pos2[1] - size2[1] / 2


def circle_collision(pos1, radius1, pos2, radius2):
    return (pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2 < (radius1 + radius2) ** 2


def get_box_collider_penetration(box_collider1: BoxCollider, boc_collider2: BoxCollider):
    return get_box_penetration(box_collider1.get_pos(), box_collider1.size, boc_collider2.get_pos(), boc_collider2.size)


def get_box_penetration(pos1, size1, pos2, size2):
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
    return get_circle_penetration(circle_collider1.get_pos(), circle_collider1.radius, circle_collider2.get_pos(),
                                  circle_collider2.radius)


def get_circle_penetration(pos1, radius1, pos2, radius2):
    x_penetration = 0
    y_penetration = 0
    if circle_collision(pos1, radius1, pos2, radius2):
        angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
        current_distance = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        x_penetration = ((radius1 + radius2) - current_distance) * math.cos(angle)
        y_penetration = ((radius1 + radius2) - current_distance) * math.sin(angle)
    return x_penetration, y_penetration


def is_colliding(collider1: Collider, collider2: Collider):
    if isinstance(collider1, BoxCollider) and isinstance(collider2, BoxCollider):
        return AABB_collision(collider1.get_pos(), collider1.size, collider2.get_pos(), collider2.size)
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, CircleCollider):
        return circle_collision(collider1.get_pos(), collider1.radius, collider2.get_pos(), collider2.radius)
    # Circle and Box collision is approximated with the circle being interpreted as a box
    elif isinstance(collider1, BoxCollider) and isinstance(collider2, CircleCollider):
        return AABB_collision(collider1.get_pos(), collider1.size, collider2.get_pos(),
                              (collider2.radius * 2, collider2.radius * 2))
    elif isinstance(collider1, CircleCollider) and isinstance(collider2, BoxCollider):
        return AABB_collision(collider1.get_pos(), (collider1.radius * 2, collider1.radius * 2), collider2.get_pos(),
                              collider2.size)


def get_penetration(collider1: Collider, collider2: Collider):
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
    collider_colliding = []
    for c in colliders:
        if is_colliding(collider, c):
            collider_colliding.append(c)
    return collider_colliding


def get_penetration_with_all(collider: Collider, colliders: list) -> list:
    penetration = []
    for c in colliders:
        if is_colliding(collider, c):
            penetration.append(get_penetration(collider, c))
    return penetration


def get_penetration_coefficient(total_penetration, object_penetration):
    return object_penetration / total_penetration


def get_elastic_collision_final_velocity(velocity1, velocity2, mass1, mass2):
    final_velocity1X = (velocity1[0] * (mass1 - mass2) + 2 * mass2 * velocity2[0]) / (mass1 + mass2)
    final_velocity1Y = (velocity1[1] * (mass1 - mass2) + 2 * mass2 * velocity2[1]) / (mass1 + mass2)
    final_velocity2X = (velocity2[0] * (mass2 - mass1) + 2 * mass1 * velocity1[0]) / (mass1 + mass2)
    final_velocity2Y = (velocity2[1] * (mass2 - mass1) + 2 * mass1 * velocity1[1]) / (mass1 + mass2)
    return (final_velocity1X, final_velocity1Y), (final_velocity2X, final_velocity2Y)


class DynamicCollider:
    def __init__(self, game_object):
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

    def set_colliders(self, collider):
        self.collider = collider

    def get_colliders(self):
        return self.collider

    def update(self):
        if self.static:
            return
        self.velocity = (self.velocity[0] + self.acceleration[0] * Game.timeStep,
                         self.velocity[1] + self.acceleration[1] * Game.timeStep)
        self.game_object.pos = (self.game_object.pos[0] + self.velocity[0] * Game.timeStep,
                                self.game_object.pos[1] + self.velocity[1] * Game.timeStep)
        self.velocity = (self.velocity[0] * (1 - self.air_friction * Game.timeStep),
                         self.velocity[1] * (1 - self.air_friction * Game.timeStep))
        if self.collider is not None:
            objects_collidings = self._get_instant_collisions()
            self._set_collisions(objects_collidings)
            if len(objects_collidings) > 0:
                self._on_collision(objects_collidings)


    def _on_collision(self, objects_colliding):
        penetration_sum = self.get_penetration(objects_colliding)
        penetration_normal = math.atan2(-penetration_sum[1], -penetration_sum[0])

        velocity_angle = math.atan2(self.velocity[1], self.velocity[0])
        velocity_magnitude = MathUtil.magnitude(self.velocity)
        angle_difference = velocity_angle - penetration_normal

        bounce_angle = math.atan2(math.sin(angle_difference), -math.cos(angle_difference)) + penetration_normal
        bounce_velocity = (velocity_magnitude * math.cos(bounce_angle), velocity_magnitude * math.sin(bounce_angle))

        #self.velocity = (bounce_velocity[0] * self.bounciness, bounce_velocity[1] * self.bounciness)
        #self.game_object.pos = (self.game_object.pos[0] - penetration_sum[0], self.game_object.pos[1] - penetration_sum[1])  # correct object intersection

        for collider in objects_colliding:
            if isinstance(collider.game_object, Game.Body):
                self._resolve_collision(collider.game_object.dynamic_collider)

    def _get_kinetic_energy(self, velocity_vect):
        return (self.mass * velocity_vect ** 2) / 2

    def _get_instant_collisions(self):
        colliders_to_check = colliders_in_game.copy()
        colliders_to_check.remove(self.collider)
        return get_collider_colliding(self.collider, colliders_to_check)

    def get_collisions(self):
        return self.collisions

    def _set_collisions(self, collisions):
        self.collisions = collisions

    def get_penetration(self, colliders):
        penetrations = get_penetration_with_all(self.collider, colliders)
        penetration_sum = (0, 0)
        for p in penetrations:
            penetration_sum = (penetration_sum[0] + p[0], penetration_sum[1] + p[1])
        return penetration_sum

    def _resolve_collision(self, collider):
        solve_constraints(self, collider)



def solve_constraints(dynamic_collider1: DynamicCollider, dynamic_collider2: DynamicCollider): # with energy conservation
    if dynamic_collider1.static:
        print("should not call this function with static collider as first argument")
        return
    penetration = get_penetration(dynamic_collider1.collider, dynamic_collider2.collider)
    collision_normal_angle = math.atan2(-penetration[1], -penetration[0])

    if not dynamic_collider2.static:
        velocity1 = dynamic_collider1.velocity
        velocity2 = dynamic_collider2.velocity
        projected_velocity1 = MathUtil.project_vector(velocity1, penetration)
        projected_velocity1 = (projected_velocity1[0], projected_velocity1[1])
        projected_velocity2 = MathUtil.project_vector(velocity2, penetration)
        #print("projected : ", projected_velocity1, projected_velocity2)

        average_bounciness = (dynamic_collider1.bounciness + dynamic_collider2.bounciness) / 2

        # https://www.vobarian.com/collisions/2dcollisions2.pdf

        final_velocity1x = (projected_velocity1[0] * (dynamic_collider1.mass - dynamic_collider2.mass) + projected_velocity2[0] * 2 * dynamic_collider2.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity1y = (projected_velocity1[1] * (dynamic_collider1.mass - dynamic_collider2.mass) + projected_velocity2[1] * 2 * dynamic_collider2.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity1 = (final_velocity1x * dynamic_collider1.bounciness, final_velocity1y * dynamic_collider1.bounciness)
        final_velocity2x = (projected_velocity2[0] * (dynamic_collider2.mass - dynamic_collider1.mass) + projected_velocity1[0] * 2 * dynamic_collider1.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity2y = (projected_velocity2[1] * (dynamic_collider2.mass - dynamic_collider1.mass) + projected_velocity1[1] * 2 * dynamic_collider1.mass) / (dynamic_collider1.mass + dynamic_collider2.mass)
        final_velocity2 = (final_velocity2x * dynamic_collider2.bounciness, final_velocity2y * dynamic_collider2.bounciness)

        #print("final : ", final_velocity1, final_velocity2)
        dynamic_collider1.velocity = dynamic_collider1.velocity[0] + final_velocity1[0] - projected_velocity1[0], dynamic_collider1.velocity[1] + final_velocity1[1] - projected_velocity1[1]
        dynamic_collider2.velocity = dynamic_collider2.velocity[0] + final_velocity2[0] - projected_velocity2[0], dynamic_collider2.velocity[1] + final_velocity2[1] - projected_velocity2[1]

        #print("initial pos : ", dynamic_collider1.game_object.pos, dynamic_collider2.game_object.pos)
        #print("initial distance : ", MathUtil.magnitude(penetration))
        dynamic_collider1.game_object.pos = (dynamic_collider1.game_object.pos[0] - penetration[0] / 2, dynamic_collider1.game_object.pos[1] - penetration[1] / 2)
        dynamic_collider2.game_object.pos = (dynamic_collider2.game_object.pos[0] + penetration[0] / 2, dynamic_collider2.game_object.pos[1] + penetration[1] / 2)
        #print("final pos : ", dynamic_collider1.game_object.pos, dynamic_collider2.game_object.pos)
        #print("final distance : ", MathUtil.magnitude(get_penetration(dynamic_collider1.collider, dynamic_collider2.collider)))
        #print("final distance after move : ", MathUtil.magnitude(get_penetration(dynamic_collider1.collider, dynamic_collider2.collider)))

    else:
        velocity_angle = math.atan2(dynamic_collider1.velocity[1], dynamic_collider1.velocity[0])
        velocity_magnitude = MathUtil.magnitude(dynamic_collider1.velocity)
        angle_difference = velocity_angle - collision_normal_angle

        bounce_angle = math.atan2(math.sin(angle_difference), -math.cos(angle_difference)) + collision_normal_angle
        bounce_velocity = (velocity_magnitude * math.cos(bounce_angle), velocity_magnitude * math.sin(bounce_angle))

        dynamic_collider1.velocity = (bounce_velocity[0] * dynamic_collider1.bounciness, bounce_velocity[1] * dynamic_collider1.bounciness)
        dynamic_collider1.game_object.pos = (dynamic_collider1.game_object.pos[0] - penetration[0], dynamic_collider1.game_object.pos[1] - penetration[1])


def reset():
    colliders_in_game.clear()

