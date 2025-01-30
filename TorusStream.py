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

# Define some constants
NUM_COLUMNS = 32
NUM_ROWS = 24
COLUMN_WIDTH = 25
COLUMN_HEIGHT = 25
TORUS_RADIUS = COLUMN_WIDTH * NUM_COLUMNS / (2 * math.pi)
COLORS = [(0, 255, 0), (0, 128, 0)]

# Define the words to display
words = ["HELLO", "WORLD"]

# Convert the words to binary representation
binary_words = [[int(b) for b in bin(ord(c))[2:].zfill(8)] for word in words for c in word]

# Initialize the binary stream
binary_stream = [[random.randint(0, 1) for _ in range(NUM_ROWS)] for _ in range(NUM_COLUMNS)]

# Define a function to update the binary stream
def update_binary_stream():
    for i in range(NUM_COLUMNS):
        # Remove the first item from the binary stream column
        binary_stream[i].pop(0)
        # Add a new random binary value to the bottom of the column
        binary_stream[i].append(random.randint(0, 1))
    
    # Wrap the binary stream around the torus
    for i in range(NUM_COLUMNS):
        for j in range(NUM_ROWS):
            # Copy the binary value from the corresponding point on the opposite side of the torus
            binary_stream[i][j] = binary_stream[(i + NUM_COLUMNS) % NUM_COLUMNS][(j + NUM_ROWS) % NUM_ROWS]

# Define a function to draw the binary stream
def draw_binary_stream(angle, distance):
    for i in range(NUM_COLUMNS):
        for j in range(len(binary_words)):
            # Get the binary value for the current row
            binary_word_value = binary_words[j][i % 8]
            # Calculate the x, y, and z coordinates of the current binary value
            torus_angle = 2 * math.pi * i / NUM_COLUMNS
            torus_radius = TORUS_RADIUS + COLUMN_WIDTH * ((j % 8) + 1)
            x = WIDTH / 2 + distance * math.cos(angle) + torus_radius * math.cos(torus_angle + angle)
            y = HEIGHT / 2 + torus_radius * math.sin(torus_angle + angle)
            z = distance * math.sin(angle) + COLUMN_HEIGHT * (j % 8)
            # Set the color of the text based on the binary value
            color = COLORS[binary_stream[i][j // 8]]
            if binary_word_value == 1:
                color = (255, 255, 255)
            # Render the text
            text = font.render(str(binary_word_value), True, color)
            # Calculate the size and position of the text in 3D space
            text_size = text.get_size()
            text_x = int(x - text_size[0] / 2)
            text_y = int(y - text_size[1] / 2)
            # Draw the text onto a surface
            text_surface = pygame.Surface(text_size, pygame.SRCALPHA)
            text_surface.blit(text, (0, 0))
            # Calculate the 3D

def draw_3d_binary_stream():
    # Clear the screen
    screen.fill((0, 0, 0))

    # Define the camera position and orientation
    camera_pos = (0, 0, -TORUS_RADIUS)
    camera_dir = (0, 0, 1)
    camera_up = (0, -1, 0)

    # Define the field of view and screen dimensions
    fov = math.pi / 4
    width, height = screen.get_size()

    # Define the viewport transformation matrix
    aspect_ratio = width / height
    view_mat = (
        (1 / math.tan(fov / 2), 0, 0, 0),
        (0, aspect_ratio / math.tan(fov / 2), 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )

    # Define the camera transformation matrix
    camera_dir = normalize(camera_dir)
    camera_right = normalize(cross(camera_dir, camera_up))
    camera_up = cross(camera_right, camera_dir)
    camera_mat = (
        (camera_right[0], camera_right[1], camera_right[2], 0),
        (camera_up[0], camera_up[1], camera_up[2], 0),
        (-camera_dir[0], -camera_dir[1], -camera_dir[2], 0),
        (0, 0, 0, 1),
    )

    # Transform each binary value into 3D space and draw it
    for i in range(NUM_COLUMNS):
        for j in range(len(binary_words)):
            # Get the binary value for the current row
            binary_word_value = binary_words[j][i % 8]

            # Calculate the x and y coordinates of the current binary value in 2D space
            angle = 2 * math.pi * i / NUM_COLUMNS
            radius = TORUS_RADIUS + COLUMN_WIDTH * ((j % 8) + 1)
            x = TORUS_RADIUS + radius * math.cos(angle)
            y = TORUS_RADIUS + radius * math.sin(angle)

            # Calculate the 3D coordinates of the current binary value
            binary_pos = (x, y, 0)
            binary_pos = transform(binary_pos, view_mat)
            binary_pos = transform(binary_pos, camera_mat)
            binary_pos = project(binary_pos, width, height)

            # Set the color of the text based on the binary value
            color = COLORS[binary_stream[i][j // 8]]
            if binary_word_value == 1:
                color = (255, 255, 255)

            # Render the text
            text = font.render(str(binary_word_value), True, color)

            # Draw the text
            text_width, text_height = text.get_size()
            screen.blit(text, (
                binary_pos[0] - text_width / 2,
                binary_pos[1] - text_height / 2
            ))

            # Calculate the angle between the text and the viewer
            angle_x = math.atan2(x - WIDTH / 2, z - distance)
            angle_y = math.atan2(y - HEIGHT / 2, z - distance)
            # Calculate the distance from the viewer to the text
            distance_x = math.sqrt((x - WIDTH / 2) ** 2 + (z - distance) ** 2)
            distance_y = math.sqrt((y - HEIGHT / 2) ** 2 + (z - distance) ** 2)
            # Scale the size of the text based on its distance from the viewer
            scale_x = max(0, (1 - distance_x / WIDTH) ** 2)
            scale_y = max(0, (1 - distance_y / HEIGHT) ** 2)
            scale = (scale_x + scale_y) / 2
            text_size_scaled = (int(text_size[0] * scale), int(text_size[1] * scale))
            text_surface_scaled = pygame.transform.scale(text_surface, text_size_scaled)
            # Rotate the text based on its angle relative to the viewer
            text_surface_rotated = pygame.transform.rotate(text_surface_scaled, math.degrees(-angle_x))
            # Calculate the final position of the text on the screen
            screen_x = int(WIDTH / 2 + distance_x * math.sin(angle_x) * math.sin(angle_y))
            screen_y = int(HEIGHT / 2 + distance_y * math.sin(angle_y))
            # Blit the text onto the screen
            screen.blit(text_surface_rotated, (screen_x - text_size_scaled[0] // 2, screen_y - text_size_scaled[1] // 2))

# Start the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update the binary stream
    update_binary_stream()
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the binary stream
    draw_binary_stream(angle, distance)
    
    # Update the display
    pygame.display.flip()
    
    # Update the camera angle and distance
    angle += 0.01
    distance += 1

# Quit pygame
pygame.quit()
