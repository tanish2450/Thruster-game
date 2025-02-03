import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stick Thruster")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)  # Arrow color

# Stick settings
stick_length = 100
stick_thickness = 10
stick_x = WIDTH // 2
stick_y = HEIGHT // 2  # Start in the middle
angle = 0  # Stick starts horizontal
rotation_speed = 0
rotation_friction = 0.95  # Slows down spinning
thrust = 0.3  # How fast the thrusters move the stick
velocity_x, velocity_y = 0, 0
friction = 0.98  # More friction for better control

# Obstacles
obstacle_list = []
OBSTACLE_SPEED = 2
OBSTACLE_SIZE = 20
OBSTACLE_FREQUENCY = 100
frame_count = 0

# Score
score = 0
font = pygame.font.Font(None, 36)

# Star background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]

# Game state
game_state = "menu"

# Functions
def create_obstacle():
    """Creates a red circle obstacle at a random position at the top of the screen."""
    x = random.randint(50, WIDTH - 50)
    y = -20  # Start slightly off-screen
    obstacle_list.append([x, y])

def draw_text(text, x, y, color=WHITE, size=36):
    """Draws text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    if game_state == "menu":
        draw_text("Stick Thruster", WIDTH // 2 - 100, HEIGHT // 3, WHITE, 40)
        draw_text("Press ENTER to Start", WIDTH // 2 - 120, HEIGHT // 2, GREEN, 30)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "playing"
                score = 0
                stick_x = WIDTH // 2
                stick_y = HEIGHT // 2
                velocity_x, velocity_y = 0, 0
                angle = 0
                rotation_speed = 0
                obstacle_list.clear()

    elif game_state == "playing":
        # Draw stars
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, 2)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Thrusters for rotation
        if keys[pygame.K_LEFT]:  # Left thruster fires
            rotation_speed -= 0.5  # Apply torque (counterclockwise)

        if keys[pygame.K_RIGHT]:  # Right thruster fires
            rotation_speed += 0.5  # Apply torque (clockwise)

        # Move forward when both thrusters are held
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:  
            velocity_x += thrust * math.sin(math.radians(angle))
            velocity_y -= thrust * math.cos(math.radians(angle))

        # Move backward
        if keys[pygame.K_DOWN]:  
            velocity_x -= thrust * math.sin(math.radians(angle))
            velocity_y += thrust * math.cos(math.radians(angle))

        # Apply rotation friction
        rotation_speed *= rotation_friction
        angle += rotation_speed  # Update rotation

        # Apply movement friction
        velocity_x *= friction
        velocity_y *= friction

        # Update stick position
        stick_x += velocity_x
        stick_y += velocity_y

        # Keep stick within screen bounds
        stick_x = max(0, min(WIDTH, stick_x))
        stick_y = max(0, min(HEIGHT, stick_y))

        # Calculate stick endpoints
        end1_x = stick_x + (stick_length / 2) * math.cos(math.radians(angle))
        end1_y = stick_y + (stick_length / 2) * math.sin(math.radians(angle))
        end2_x = stick_x - (stick_length / 2) * math.cos(math.radians(angle))
        end2_y = stick_y - (stick_length / 2) * math.sin(math.radians(angle))

        # Draw stick
        pygame.draw.line(screen, WHITE, (end1_x, end1_y), (end2_x, end2_y), stick_thickness)

        # Draw direction arrow (Shows where the stick is facing)
        arrow_x = stick_x + (stick_length / 2 + 15) * math.cos(math.radians(angle))
        arrow_y = stick_y + (stick_length / 2 + 15) * math.sin(math.radians(angle))
        pygame.draw.polygon(screen, YELLOW, [
            (arrow_x, arrow_y),
            (arrow_x - 5 * math.cos(math.radians(angle - 135)), arrow_y - 5 * math.sin(math.radians(angle - 135))),
            (arrow_x - 5 * math.cos(math.radians(angle + 135)), arrow_y - 5 * math.sin(math.radians(angle + 135))),
        ])

        # Generate obstacles less frequently
        if frame_count % OBSTACLE_FREQUENCY == 0:
            create_obstacle()
        frame_count += 1

        # Move obstacles downward
        for obstacle in obstacle_list:
            obstacle[1] += OBSTACLE_SPEED
            pygame.draw.circle(screen, RED, (int(obstacle[0]), int(obstacle[1])), OBSTACLE_SIZE)  # Back to red circles

        # Collision detection
        for obstacle in obstacle_list:
            distance = math.sqrt((stick_x - obstacle[0])**2 + (stick_y - obstacle[1])**2)
            if distance < OBSTACLE_SIZE + stick_length / 2:
                game_state = "game_over"

        # Update score
        score += 1
        draw_text(f"Score: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
