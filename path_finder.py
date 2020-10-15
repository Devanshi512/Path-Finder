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
