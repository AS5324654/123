"""A simple Snake game implemented with pygame.

Run this module directly to start the game::

    python snake_game.py

The game window uses the arrow keys to control the snake. Eat food to grow and avoid
colliding with yourself or the walls.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import Deque, Tuple

import pygame


# --- Configuration constants -------------------------------------------------

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
SNAKE_INITIAL_LENGTH = 3
SNAKE_SPEED = 10  # frames per second

BACKGROUND_COLOR = pygame.Color("black")
SNAKE_COLOR = pygame.Color("green")
FOOD_COLOR = pygame.Color("red")
TEXT_COLOR = pygame.Color("white")


# --- Data structures ---------------------------------------------------------


class Direction(Enum):
    """Possible movement directions for the snake."""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @property
    def vector(self) -> Tuple[int, int]:
        if self is Direction.UP:
            return (0, -1)
        if self is Direction.DOWN:
            return (0, 1)
        if self is Direction.LEFT:
            return (-1, 0)
        return (1, 0)

    def opposite(self) -> "Direction":
        if self is Direction.UP:
            return Direction.DOWN
        if self is Direction.DOWN:
            return Direction.UP
        if self is Direction.LEFT:
            return Direction.RIGHT
        return Direction.LEFT


@dataclass
class Snake:
    """Represents the snake as an ordered list of grid coordinates."""

    body: Deque[Tuple[int, int]]
    direction: Direction

    def head(self) -> Tuple[int, int]:
        return self.body[0]

    def next_head(self) -> Tuple[int, int]:
        dx, dy = self.direction.vector
        return ((self.head()[0] + dx) % GRID_WIDTH, (self.head()[1] + dy) % GRID_HEIGHT)

    def move(self, grow: bool = False) -> None:
        new_head = self.next_head()
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def hits_self(self) -> bool:
        return self.head() in list(self.body)[1:]


# --- Game functions ----------------------------------------------------------

def create_initial_snake() -> Snake:
    from collections import deque

    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    body = deque(
        [(start_x - i, start_y) for i in range(SNAKE_INITIAL_LENGTH)]
    )
    return Snake(body=body, direction=Direction.RIGHT)


def spawn_food(snake: Snake) -> Tuple[int, int]:
    while True:
        position = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if position not in snake.body:
            return position


def draw_cell(surface: pygame.Surface, position: Tuple[int, int], color: pygame.Color) -> None:
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def render(surface: pygame.Surface, snake: Snake, food: Tuple[int, int], score: int, font: pygame.font.Font) -> None:
    surface.fill(BACKGROUND_COLOR)
    for segment in snake.body:
        draw_cell(surface, segment, SNAKE_COLOR)
    draw_cell(surface, food, FOOD_COLOR)

    score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
    surface.blit(score_surface, (10, 10))

    pygame.display.flip()


def game_over(surface: pygame.Surface, score: int, font: pygame.font.Font) -> None:
    message = font.render("Game Over! Press R to restart or Q to quit.", True, TEXT_COLOR)
    score_message = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    score_rect = score_message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
    surface.blit(message, rect)
    surface.blit(score_message, score_rect)
    pygame.display.flip()


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    snake = create_initial_snake()
    food = spawn_food(snake)
    score = 0
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and snake.direction is not Direction.DOWN:
                    snake.direction = Direction.UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and snake.direction is not Direction.UP:
                    snake.direction = Direction.DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a) and snake.direction is not Direction.RIGHT:
                    snake.direction = Direction.LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake.direction is not Direction.LEFT:
                    snake.direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r and not running:
                    snake = create_initial_snake()
                    food = spawn_food(snake)
                    score = 0
                    running = True
                elif event.key == pygame.K_q and not running:
                    pygame.quit()
                    return

        if not paused and running:
            next_head = snake.next_head()
            grow = next_head == food
            snake.move(grow=grow)

            if snake.hits_self():
                running = False
                game_over(screen, score, font)
                continue

            if grow:
                score += 1
                food = spawn_food(snake)

            render(screen, snake, food, score, font)
            clock.tick(SNAKE_SPEED)

    # Wait for player input after game over
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()
                    return
                if event.key == pygame.K_q:
                    waiting = False
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    run()
