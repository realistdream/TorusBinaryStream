# TorusBinaryStream

README 

*Introduction*

This Python project, titled "Torus Binary Stream Tunnel," is a graphical application that simulates a binary stream represented in a 3D toroidal space. It utilizes the Pygame library for rendering graphics and interacts with binary representations of predefined words.

*Features*

 - 3D Visualization: Displays a continuous stream of binary numbers that wrap around a torus shape.
 - Dynamic Content: The visualization dynamically updates, with binary values shifting and altering their state randomly.
 - Text Rendering: Binary values are rendered as text in a 3D space and transformed to match the perspective.
 - Interactive Display: Users can observe the evolving binary words morphed into a torus formation with animated view changes.

*Requirements*

 - Python 3.x
 - Pygame library

*Installation*

Ensure Python 3.x is installed on your system.

Install Pygame by running:

pip install pygame

*Usage*

Run the script using Python:

python TorusStream.py

*Output*

The application window will display the 3D binary stream on a torus. You can exit the application by pressing ESC or closing the window.

*Code Explanation*

The script primarily consists of functions to initialize Pygame, set up the display, and define the behavior of the binary stream:

 - Initialization: Configures the display dimensions, font settings, and color schemes.
 - Binary Generation: Converts given words ('HELLO', 'WORLD') into binary and initializes random binary streams for visual dynamics.

- Visualization Functions:
 -- update_binary_stream(): Updates the binary stream, maintaining a constant feed of new binary values.
 -- draw_binary_stream(angle, distance): Calculates positions and colors for each binary digit in the toroidal space and renders these using Pygame's drawing capabilities.
 -- draw_3d_binary_stream(): Handles the 3D transformation and perspective projection of text in the display window.

Main Loop: Continuously updates and draws the binary stream to create an animation effect until terminated by the user.

License
This project is open-source and available under the MIT License.
