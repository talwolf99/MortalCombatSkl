import pygame
import sys
from enum import Enum
from game.move_type import MoveType
from game.player import Player
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



def get_p1_moves(keys):
    moves = []
    if keys[pygame.K_a]:
        moves.append(MoveType.LEFT)
    if keys[pygame.K_d]:
        moves.append(MoveType.RIGHT)
    if keys[pygame.K_w]:
        moves.append(MoveType.UP)
    return moves

def get_p2_moves(keys):
    moves = []
    if keys[pygame.K_LEFT]:
        moves.append(MoveType.LEFT)
    if keys[pygame.K_RIGHT]:
        moves.append(MoveType.RIGHT)
    if keys[pygame.K_UP]:
        moves.append(MoveType.UP)
    return moves

platforms = [
    pygame.Rect(0, 560, 800, 40)
]

p1 = Player(200, 100, (255, 0, 0))
p2 = Player(500, 100, (0, 0, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    p1.apply_movement(get_p1_moves(keys))
    p2.apply_movement(get_p2_moves(keys))

    p1.update_physics(platforms)
    p2.update_physics(platforms)

    screen.fill((20, 20, 20))
    for p in platforms:
        pygame.draw.rect(screen, (100, 100, 100), p)
    p1.draw(screen)
    p2.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
