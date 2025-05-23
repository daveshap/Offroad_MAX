import math
import random
import pygame
import pymunk

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_Y = 100
SEGMENT_LENGTH = 60
NUM_SEGMENTS = 200

COLORS = {
    "sky": (135, 206, 235),
    "ground": (60, 179, 113),
    "truck": (200, 0, 0),
    "wheel": (0, 0, 0)
}


def generate_terrain():
    points = []
    x = 0
    y = SCREEN_HEIGHT - GROUND_Y
    for _ in range(NUM_SEGMENTS):
        dy = random.randint(-20, 20)
        y = min(max(y + dy, SCREEN_HEIGHT - 250), SCREEN_HEIGHT - 50)
        points.append((x, y))
        x += SEGMENT_LENGTH
    return points


def add_terrain(space, points):
    for i in range(len(points) - 1):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        seg = pymunk.Segment(body, points[i], points[i + 1], 2)
        seg.friction = 1.0
        space.add(body, seg)


def add_truck(space, position):
    mass = 5
    size = (60, 20)
    moment = pymunk.moment_for_box(mass, size)
    chassis_body = pymunk.Body(mass, moment)
    chassis_body.position = position
    chassis_shape = pymunk.Poly.create_box(chassis_body, size)
    chassis_shape.friction = 1.0

    wheel_radius = 15
    wheel_mass = 1
    wheel_moment = pymunk.moment_for_circle(wheel_mass, 0, wheel_radius)

    wheel1_body = pymunk.Body(wheel_mass, wheel_moment)
    wheel2_body = pymunk.Body(wheel_mass, wheel_moment)
    wheel1_body.position = (position[0] - 25, position[1] - 15)
    wheel2_body.position = (position[0] + 25, position[1] - 15)
    wheel1_shape = pymunk.Circle(wheel1_body, wheel_radius)
    wheel2_shape = pymunk.Circle(wheel2_body, wheel_radius)
    for w in (wheel1_shape, wheel2_shape):
        w.friction = 1.5

    j1 = pymunk.PinJoint(chassis_body, wheel1_body, (-25, -10), (0, 0))
    j2 = pymunk.PinJoint(chassis_body, wheel2_body, (25, -10), (0, 0))

    motor1 = pymunk.SimpleMotor(chassis_body, wheel1_body, 0)
    motor2 = pymunk.SimpleMotor(chassis_body, wheel2_body, 0)
    motor1.max_force = 100000
    motor2.max_force = 100000

    space.add(chassis_body, chassis_shape,
              wheel1_body, wheel1_shape,
              wheel2_body, wheel2_shape,
              j1, j2, motor1, motor2)

    return chassis_body, motor1, motor2


def to_pygame(p):
    return int(p[0]), int(SCREEN_HEIGHT - p[1])


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Offroad_MAX Prototype")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 900)

    points = generate_terrain()
    add_terrain(space, points)

    truck_body, motor1, motor2 = add_truck(space, (80, points[0][1] + 40))

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        rate = 0
        if keys[pygame.K_RIGHT]:
            rate = -8
        elif keys[pygame.K_LEFT]:
            rate = 8
        motor1.rate = rate
        motor2.rate = rate

        space.step(dt)

        offset_x = SCREEN_WIDTH / 2 - truck_body.position.x
        screen.fill(COLORS["sky"])

        # draw terrain
        for i in range(len(points) - 1):
            p1 = to_pygame((points[i][0] + offset_x, points[i][1]))
            p2 = to_pygame((points[i + 1][0] + offset_x, points[i + 1][1]))
            pygame.draw.line(screen, COLORS["ground"], p1, p2, 3)

        # draw truck
        for shape in truck_body.shapes:
            if isinstance(shape, pymunk.Poly):
                verts = []
                for v in shape.get_vertices():
                    world = truck_body.local_to_world(v)
                    verts.append(to_pygame((world.x + offset_x, world.y)))
                pygame.draw.polygon(screen, COLORS["truck"], verts)

        for wheel in (motor1.b, motor2.b):
            pos = to_pygame((wheel.position.x + offset_x, wheel.position.y))
            wheel_shape = next(iter(wheel.shapes))
            pygame.draw.circle(screen, COLORS["wheel"], pos, int(wheel_shape.radius), 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
