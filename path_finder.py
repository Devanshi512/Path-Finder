import pygame
import math
from queue import PriorityQueue


WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")


# Color codes
ORANGE = (255, 165, 0)  # Start Node
TURQUOISE = (64, 224, 208)  # End Node
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)  # Walkable Node
BLACK = (0, 0, 0)  # Obstacle
PURPLE = (128, 0, 128)  # Final Path
GREY = (128, 128, 128)


class Cell:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_obstacle(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_obstacle(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def reset(self):
		self.color = WHITE

	def get_position(self):
		return self.row, self.col

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
        def __lt__(self, other):
		return False
	
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():  # DOWN
		    self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():  # UP
		    self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():  # RIGHT
		    self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():  # LEFT
		    self.neighbors.append(grid[self.row][self.col - 1])


'''
    A* selects the path that minimizes

    f(n)=g(n)+h(n)
    where n is the next node on the path,
          g(n) is the cost of the path from start node,
          h(n) is a heuristic function 
'''

def heuristic(h1, h2):
    x1, y1 = h1
    x2, y2 = h2
    return abs(x1 - x2) + abs(y1 - y2)
 
	
# Working with Grid 
def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Cell(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

	
# Get currently clicked cell's location
def get_clicked_cell_position(loc, total_rows, total_width):
    gap = total_width // total_rows
    y, x = loc
    row = y // gap
    col = x // gap

    return row, col


# Finalize and draw the path between start and end node on grid
def final_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# Main functional logic of A* Algorithm
def logic(draw, grid, start, end):
    count = 0
    priority_set = PriorityQueue()
    priority_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    priority_set_hash = {start}

    while not priority_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = priority_set.get()[2]
        priority_set_hash.remove(current)

        if current == end:
            final_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_gscore = g_score[current] + 1

            if temp_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_gscore
                f_score[neighbor] = temp_gscore + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in priority_set_hash:
                    count += 1
                    priority_set.put((f_score[neighbor], count, neighbor))
                    priority_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def main(win, width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_cell_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_cell_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()  # Press "C" key to reset
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
		
	    if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # # Press "SPACEBAR" key to run the program
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    logic(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()


# Execute the program
main(WIN, WIDTH)

