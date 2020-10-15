import pygame

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
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_cell_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()  # Press "C" key to reset
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

    pygame.quit()


# Execute the program
main(WIN, WIDTH)

