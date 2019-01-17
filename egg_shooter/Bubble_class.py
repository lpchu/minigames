class Bubble:
    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity
        self.color = random.choice(COLOR_LIST)

    def get_position(self):
        return self.pos

    def update(self):
        firing_direction = angle_to_vector(firing_angle)
        self.vel[0] += BUBBLE_ACCELERATION * firing_direction[0]
        self.vel[1] -= BUBBLE_ACCELERATION * firing_direction[1]

    def draw(self, canvas):
        # update bubble position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        canvas.draw_circle(self.pos, BUBBLE_RADIUS, 1, self.color, self.color)

