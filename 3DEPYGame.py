import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import socket
import threading

# Define the vertices and edges for the cube
vertices_cube = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges_cube = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Define the vertices and edges for the character
vertices_character = (
    (-0.5, -1, -0.5),
    (0.5, -1, -0.5),
    (0.5, 1, -0.5),
    (-0.5, 1, -0.5),
    (-0.5, -1, 0.5),
    (0.5, -1, 0.5),
    (0.5, 1, 0.5),
    (-0.5, 1, 0.5)
)

edges_character = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Function to draw a cube given vertices and edges
def draw_cube(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to handle a client connection and update player position
def handle_client(client_socket, player_position):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        x, y, z = map(float, data.split(','))
        player_position[:] = [x, y, z]

    client_socket.close()

# Function to run the multiplayer server
def multiplayer_server(player_position):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, player_position))
        client_handler.start()

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up the perspective and initial translation
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Initial player position
player_position = [0, 0, 0]

# Start the multiplayer server in a separate thread
multiplayer_thread = threading.Thread(target=multiplayer_server, args=(player_position,))
multiplayer_thread.start()

# Main loop for rendering
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Rotate the scene
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Draw the cube
    draw_cube(vertices_cube, edges_cube)
    
    # Translate to the player's position and draw the character
    glTranslatef(*player_position)
    draw_cube(vertices_character, edges_character)
    
    pygame.display.flip()
    pygame.time.wait(10)

if __name__ == "__main__":
    main()
