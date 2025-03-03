import pygame
import asyncio
import random
import io
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SPEED = [2, 2]
BLACK = (0, 0, 0)

# Colors
RED = (255, 0, 0)
CIRCLE_RADIUS = 10

# Global variables
circle_x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
circle_y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)

# Create Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# Check if running in Pygbag
is_pygbag = "pygbag" in sys.modules

async def load_image(url, dimensions):
    import pyodide

    print(f"Fetching image from: {url}")

    # Fetch the image as binary data
    response = await pyodide.http.pyfetch(url)
    image_data = await response.bytes()  # Get the image as bytes
        
    image = pygame.image.load(io.BytesIO(image_data))  # Load image into Pygame
    return pygame.transform.scale(image, dimensions)  # Resize the image

async def main():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Basketball_ball_without_shadow.png/640px-Basketball_ball_without_shadow.png"

    # Try loading the image, fall back to a red circle
    try:
        ball = await load_image(image_url, (50, 50)) if is_pygbag else None
    except Exception as e:
        print(f"Image load failed: {e}")
        ball = None

    # If no image, use a red circle instead
    if not ball:
        ball = pygame.image.load("img/basketball.png")
        ball = pygame.transform.smoothscale(ball, (50, 50))

    ball_rect = ball.get_rect(center=(circle_x, circle_y))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the ball
        ball_rect.x += SPEED[0]
        ball_rect.y += SPEED[1]

        # Collision detection
        if ball_rect.left < 0 or ball_rect.right > SCREEN_WIDTH:
            SPEED[0] = -SPEED[0]
        if ball_rect.top < 0 or ball_rect.bottom > SCREEN_HEIGHT:
            SPEED[1] = -SPEED[1]

        # Draw everything
        screen.fill(BLACK)
        screen.blit(ball, ball_rect)  # Correctly blit the ball
        pygame.display.flip()

        await asyncio.sleep(0)  # Allow other tasks to run
        clock.tick(60)

if __name__ == "__main__":
    asyncio.ensure_future(main())

