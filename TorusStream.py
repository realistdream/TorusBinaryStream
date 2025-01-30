import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Torus Binary Stream Tunnel")

# Set up the font
font = pygame.font.SysFont("monospace", 20)

# Define constants
NUM_COLUMNS = 32
NUM_ROWS = 24
COLUMN_WIDTH = 25
COLUMN_HEIGHT = 25
TORUS_RADIUS = COLUMN_WIDTH * NUM_COLUMNS / (2 * math.pi)
COLORS = [(0, 255, 0), (0, 128, 0)]

# Words to display
words = ["HELLO", "WORLD"]

# Convert words to binary representation
binary_words = [[int(b) for b in bin(ord(c))[2:].zfill(8)] for word in words for c in word]

# Initialize binary stream
binary_stream = [[random.randint(0, 1) for _ in range(NUM_ROWS)] for _ in range(NUM_COLUMNS)]


angle = 0
distance = 200  


def update_binary_stream():
    """Shifts the binary stream downward to create a flowing effect."""
    for i in range(NUM_COLUMNS):
        binary_stream[i].pop(0)
        binary_stream[i].append(random.randint(0, 1))


def project(x, y, z):
    """Projects 3D coordinates onto 2D screen."""
    f = 500 / (500 + z)  
    screen_x = int(WIDTH / 2 + x * f)
    screen_y = int(HEIGHT / 2 + y * f)
    return screen_x, screen_y


def draw_binary_stream():
    """Renders the flowing binary digits on a 3D torus."""
    screen.fill((0, 0, 0))

    for i in range(NUM_COLUMNS):
        for j in range(len(binary_words)):
            binary_value = binary_words[j][i % 8]  
            
            # Calculate torus coordinates
            torus_angle = 2 * math.pi * i / NUM_COLUMNS
            torus_radius = TORUS_RADIUS + COLUMN_WIDTH * ((j % 8) + 1)
            x = torus_radius * math.cos(torus_angle + angle)
            y = torus_radius * math.sin(torus_angle + angle)
            z = distance - COLUMN_HEIGHT * (j % 8)

            # Convert 3D to 2D screen space
            screen_x, screen_y = project(x, y, z)

            # Determine color
            color = COLORS[binary_stream[i][j % NUM_ROWS]]
            if binary_value == 1:
                color = (255, 255, 255)

            # Render text
            text = font.render(str(binary_value), True, color)
            screen.blit(text, (screen_x - text.get_width() / 2, screen_y - text.get_height() / 2))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    update_binary_stream()  
    draw_binary_stream()  

    pygame.display.flip()  
    angle += 0.001  

pygame.quit()


    
    # Update the camera angle and distance
    angle += 0.01
    distance += 1

# Quit pygame
pygame.quit()
