"""10x10 Grid for visualizing A Star pathing."""
import os
import numpy as np
from time import sleep
import pygame as pg
import sys

# RGB color codes for pygame.
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
LIME = [124, 231, 141]
BLUE = [0, 0, 255]
RED = [255, 0, 255]
size = [900, 900]

# Global variables.
path = []  # Store the return path from end node.
toggle = True  # Disable map designators after drawing path.
mode = "Wall"
original_grid = [[None for i in range(9)] for i in range(9)]
grid_to_store_g = [[None for i in range(9)] for i in range(9)]
grid_to_store_h = [[None for i in range(9)] for i in range(9)]
grid_to_store_f = [[None for i in range(9)] for i in range(9)]

os.environ['SDL_VIDEO_CENTERED'] = 'True'
screen = pg.display.set_mode(size)
screen.convert()
pg.font.init()
try:
    font = pg.font.SysFont('saucecodepronerdfont', 25)
    font2 = pg.font.SysFont('saucecodepronerdfont', 20)
except Exception:
    font = pg.font.SysFont(None, 25)
    font2 = pg.font.SysFont(None, 20)


class Node:
    """Store Node details."""

    def __init__(self, position, g, h, f, parent=None):
        """Store Node attributes."""
        self.position = position
        self.parent = parent

        self.g = g
        self.h = h
        self.f = f

    def __repr__(self):
        """Print Position."""
        return f"{self.position}"


def calc(x, start, end):
    """Calculate distance between end and this point."""
    x = np.array((x))
    end = np.array((end))

    g = round(np.sqrt(np.sum(np.square(x - end))) * 10)  # Distance from current point to target
    h = round(np.sqrt(np.sum(np.square(start - x))) * 10)  # Distance from start to current point
    f = round(g + h)
    return g, h, f


def show(position):
    """Show A Star pathing with blue square."""
    global screen
    box_x = (position[0]*90)+45
    box_y = (position[1]*90)+45
    rect = pg.Rect(box_x, box_y, (size[0]*0.09+10), (size[1]*0.09+10))
    pg.draw.rect(screen, BLUE, rect, 5)
    pg.display.update()


def solve(maze, start, end):
    """Path from start to the end."""
    global font, font2, original_grid, grid_to_store_g, grid_to_store_h, grid_to_store_f
    moves = [[-1, 0], [-1, -1], [-1, 1],  [0, -1], [1, 0], [1, -1], [1, 1], [0, 1]]
    shape = np.shape(maze)
    start_score = calc(start, end, start)
    pos = Node(start, *start_score, None)
    unvisited = [pos]
    visited = []
    grid_to_store_g[pos.position[0]][pos.position[1]] = start_score[0]
    grid_to_store_h[pos.position[0]][pos.position[1]] = start_score[1]
    grid_to_store_f[pos.position[0]][pos.position[1]] = start_score[2]

    while len(unvisited) != 0:
        show(pos.position)
        visited.append(pos)

        children = []
        if pos.position == end:
            color_path(pos)
            break

        for move in moves:
            p = [pos.position[0], pos.position[1]]
            pos1 = list(np.add(p, move))
            if (
                    (
                        -1 < pos1[0] < shape[0] and -1 < pos1[1] < shape[1]
                    ) and
                    maze[pos1[0]][pos1[1]] != 1
            ):
                if pos1 in [x.position for x in visited]:
                    continue
                children.append(pos1)

        if children:
            for child in children:
                scores = calc(child, end, start)
                kid = Node(child, *scores, pos)
                grid_to_store_g[kid.position[0]][kid.position[1]] = scores[0]
                grid_to_store_h[kid.position[0]][kid.position[1]] = scores[1]
                grid_to_store_f[kid.position[0]][kid.position[1]] = scores[2]
                unvisited.append(kid)

        unvisited = [x for x in unvisited if x.position != pos.position]
        minf = min([x.f for x in unvisited])
        ind_minf = [x.f for x in unvisited].index(minf)
        pos = unvisited[ind_minf]
        sleep(0.3)

    for i, row in enumerate(original_grid):
        for j, item in enumerate(row):
            if item is not None:
                continue
            if grid_to_store_f[i][j] is not None:
                original_grid[i][j] = grid_to_store_f[i][j]


def Draw(pos=None):
    """Draw the Grid."""
    global mode, original_grid, screen, font, font2, grid_to_store_g, grid_to_store_h, grid_to_store_f, path
    title = font.render("A* Visualizer", True, BLACK)
    title_rect = title.get_rect()
    title_rect.centerx = size[0] * 0.5
    title_rect.centery = size[0] * 0.02
    screen.blit(title, title_rect)
    text = font.render(f"Mode: {mode}", True, BLACK)
    text_rect = text.get_rect()
    text_rect.left = size[0] * 0.8
    text_rect.centery = size[0] * 0.977
    screen.blit(text, text_rect)
    start = font.render("Press S to start", True, BLACK)
    start_rect = text.get_rect()
    start_rect.left = size[0] * 0.045
    start_rect.centery = size[0] * 0.977
    screen.blit(start, start_rect)

    if pos:
        x = ((pos[0]-(size[0]*0.05))//(size[0]*0.1))*(size[0]*0.1) + (size[0]*0.055)
        y = ((pos[1]-(size[0]*0.05))//(size[0]*0.1))*(size[0]*0.1) + (size[0]*0.055)

        for i in range(9):
            for j in range(9):
                if original_grid[i][j] is not None:
                    x_loc = i * size[0]*0.1 + size[0]*0.1
                    y_loc = j * size[1]*0.1 + size[1]*0.1

                    item = font.render(str(original_grid[i][j]), True, BLACK)
                    if isinstance(original_grid[i][j], int):
                        item = font2.render(str(original_grid[i][j]), True, BLACK)
                    item_rect = item.get_rect()
                    item_rect.centerx = x_loc
                    item_rect.centery = y_loc
                    screen.blit(item, item_rect)

        for i in range(9):
            for j in range(9):
                if grid_to_store_g[i][j] is not None:
                    x_loc = i * size[0]*0.1 + size[0]*0.1 + 30
                    y_loc = j * size[1]*0.1 + size[1]*0.1 + 30

                    item = font2.render(str(grid_to_store_g[i][j]), True, RED)
                    item_rect = item.get_rect()
                    item_rect.centerx = x_loc
                    item_rect.centery = y_loc
                    screen.blit(item, item_rect)

        for i in range(9):
            for j in range(9):
                if grid_to_store_h[i][j] is not None:
                    x_loc = i * size[0]*0.1 + size[0]*0.1 - 30
                    y_loc = j * size[1]*0.1 + size[1]*0.1 - 30

                    item = font2.render(str(grid_to_store_h[i][j]), True, BLUE)
                    item_rect = item.get_rect()
                    item_rect.centerx = x_loc
                    item_rect.centery = y_loc
                    screen.blit(item, item_rect)

    for i in range(11):
        pg.draw.line(screen, BLACK, ((size[0]*0.05)+(size[0]*0.1)*i, (size[1]*0.05)), ((size[1]*0.05)+(size[0]*0.1)*i, (size[1]*0.95)), 3)
        pg.draw.line(screen, BLACK, ((size[1]*0.05), (size[1]*0.95)-(size[1]*0.1)*i), ((size[1]*0.95), (size[1]*0.95)-(size[0]*0.1)*i), 3)

    if pos is not None:
        rect = pg.Rect(x, y, (size[0]*0.093), (size[0]*0.093))
        pg.draw.rect(screen, GREEN, rect, 5)

    for a, b in path:
        box_x = (a*90)+45
        box_y = (b*90)+45
        rect = pg.Rect(box_x, box_y, (size[0]*0.09+10), (size[1]*0.09+10))
        pg.draw.rect(screen, LIME, rect, 5)


def set_location(pos):
    """Set items in the grid."""
    global mode, original_grid
    x = ((pos[0]-(size[0]*0.055))//(size[0]*0.1))*(size[0]*0.1) + (size[0]*0.055)
    y = ((pos[1]-(size[0]*0.055))//(size[0]*0.1))*(size[0]*0.1) + (size[0]*0.055)

    if mode == 'Wall':
        original_grid[int(x//90)][int(y//90)] = 'W'

    elif mode == 'Start':
        if any('S' in row for row in original_grid):
            for i, row in enumerate(original_grid):
                for j, item in enumerate(row):
                    if item == 'S':
                        original_grid[i][j] = None
        original_grid[int(x//90)][int(y//90)] = 'S'

    elif mode == 'End':
        if any('E' in row for row in original_grid):
            for i, row in enumerate(original_grid):
                for j, item in enumerate(row):
                    if item == 'E':
                        original_grid[i][j] = None
        original_grid[int(x//90)][int(y//90)] = 'E'

    Draw()
    pg.display.update()


def color_path(pos):
    """Form the path from start to end."""
    global path
    while pos is not None:
        path.append(pos.position)
        pos = pos.parent


def transform_grid():
    """Convert grid so that the solve function can use it."""
    global original_grid
    grid2 = [[None for i in range(9)] for i in range(9)]
    for i, row in enumerate(original_grid):
        for j, item in enumerate(row):
            if item == 'S':
                start = [i, j]
                grid2[i][j] = 0
            elif item == 'E':
                end = [i, j]
                grid2[i][j] = 0
            elif item == 'W':
                grid2[i][j] = 1
            else:
                grid2[i][j] = 0

    solve(grid2, start, end)


def main_loop():
    """Pygame Drawing loop."""
    global screen, mode, toggle
    pos = None
    while True:
        Draw(pos)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                if not (45 < pos[0] < 845 and
                        45 < pos[1] < 845):
                    pos = None
                    continue
                screen.fill(WHITE)
                Draw(pos)
            if toggle:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        mode = "Wall"
                        screen.fill(WHITE)
                        Draw(pos)
                        if pos:
                            set_location(pos)
                    if event.key == pg.K_q:
                        mode = "Start"
                        screen.fill(WHITE)
                        Draw(pos)
                        if pos:
                            set_location(pos)
                    if event.key == pg.K_e:
                        mode = "End"
                        screen.fill(WHITE)
                        Draw(pos)
                        if pos:
                            set_location(pos)
                    if event.key == pg.K_s:
                        toggle = False
                        transform_grid()
        pg.display.update()


def main():
    """Call necessary functions."""
    screen.fill(WHITE)
    main_loop()
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
