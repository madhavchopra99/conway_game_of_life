#!/usr/bin/env python3
"""Conway's Game of Life implemented with pygame."""

import random

import pygame

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

type position_type = tuple[int, int]
type positions_type = set[position_type]


def gen(num: int) -> positions_type:
    """Generate a set of random positions for a given num value."""
    return {
        (random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH))
        for _ in range(num)
    }


def draw_grid(positions: positions_type) -> None:
    """Draw the grid and fill positions with yellow color."""

    # filling positions with yellow color
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    # drawing horizontal lines
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    # drawing vertical lines
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def adjust_grid(positions: positions_type) -> positions_type:
    """Return positions of alive cells in next generation."""
    all_neighbors: positions_type = set()
    new_positions: positions_type = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        living_neighbors = sum(neighbor in positions for neighbor in neighbors)

        if living_neighbors in (2, 3):
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        living_neighbors = sum(neighbor in positions for neighbor in neighbors)

        if living_neighbors == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos: position_type) -> list[position_type]:
    """Return neighbours for given grid position."""
    x, y = pos
    return [
        (x + dx, y + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if 0 <= x + dx <= GRID_WIDTH
        and 0 <= y + dy <= GRID_HEIGHT
        and (dx, dy) != (0, 0)
    ]


def main() -> None:
    """Run the game loop."""
    running = True
    playing = False
    count = 0
    update_freq = 30

    positions: positions_type = set()

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        # update grid to next generation based on update_freq and FPS.
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        # feedback caption for playing or paused game
        pygame.display.set_caption("Playing" if playing else "Paused")

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            # checking key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)

        # drawing grid lines on screen
        screen.fill(GREY)
        draw_grid(positions)

        # updating display
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
