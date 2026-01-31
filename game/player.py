import pygame
from .move_type import MoveType
from .physics import ACCEL, JUMP_FORCE, GRAVITY, MAX_SPEED, FRICTION

class Player:
    def __init__(self, x, y, color,
                 accel=ACCEL,
                 jump_force=JUMP_FORCE,
                 gravity=GRAVITY,
                 max_speed=MAX_SPEED,
                 friction=FRICTION,
                 window_width=800,
                 window_height=600):
        self.accel = accel
        self.jump_force = jump_force
        self.gravity = gravity
        self.max_speed = max_speed
        self.friction = friction
        self.window_width = window_width
        self.window_height = window_height
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def apply_movement(self, moves):
        for move in moves:
            if move == MoveType.LEFT:
                self.vel.x -= self.accel
            elif move == MoveType.RIGHT:
                self.vel.x += self.accel
            elif move == MoveType.UP and self.on_ground:
                self.vel.y = -self.jump_force
                self.on_ground = False

    def update_physics(self, platforms):
        self.vel.y += self.gravity
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.vel.x *= self.friction

        self.rect.x += int(self.vel.x)
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel.x > 0:
                    self.rect.right = p.left
                elif self.vel.x < 0:
                    self.rect.left = p.right
                self.vel.x = 0

        self.rect.y += int(self.vel.y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel.y > 0:
                    self.rect.bottom = p.top
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = p.bottom
                self.vel.y = 0

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.window_width)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
