import pygame
import sys
from enum import Enum
import random


# Direction for cycle movement
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# LightCycle class to manage player movement and trails
class LightCycle:
    def __init__(self, x, y, color, direction, key_controls, player_name):
        """Initialize cycle with position, color, direction, controls, and name"""
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.trail = [(x, y)]  # Store trail positions
        self.key_controls = key_controls  # Dict of keys to directions
        self.player_name = player_name
        self.speed = 5
        self.alive = True

    def move(self):
        """Update cycle position based on current direction"""
        if not self.alive:
            return
        dx, dy = self.direction.value
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.trail.append((self.x, self.y))

    def change_direction(self, new_direction):
        """Change cycle direction if not opposite to current"""
        if not self.alive:
            return
        # Prevent 180-degree turns
        current_dx, current_dy = self.direction.value
        new_dx, new_dy = new_direction.value
        if (current_dx, current_dy) != (-new_dx, -new_dy):
            self.direction = new_direction

    def draw(self, screen):
        """Draw cycle and its trail"""
        if not self.alive:
            return
        # Draw trail
        for i in range(len(self.trail) - 1):
            pygame.draw.line(screen, self.color, self.trail[i], self.trail[i + 1], 3)
        # Draw cycle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    def check_collision(self, other_trail):
        """Check if cycle collides with another trail or boundaries"""
        if not self.alive:
            return False
        head = (self.x, self.y)
        # Check screen boundaries
        if (self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600):
            self.alive = False
            return True
        # Check collision with trails
        for segment in other_trail + self.trail[:-10]:  # Exclude recent trail to allow turning
            if abs(self.x - segment[0]) < 5 and abs(self.y - segment[1]) < 5:
                self.alive = False
                return True
        return False


# Game class to manage game state and logic
class Game:
    def __init__(self):
        """Initialize Pygame and game components"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tron Light Cycle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Define controls for players
        self.player1_controls = {
            pygame.K_w: Direction.UP,
            pygame.K_s: Direction.DOWN,
            pygame.K_a: Direction.LEFT,
            pygame.K_d: Direction.RIGHT
        }
        self.player2_controls = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT
        }

        # Initialize cycles
        self.cycle1 = LightCycle(200, 300, (0, 255, 255), Direction.RIGHT, self.player1_controls, "Player 1")
        self.cycle2 = LightCycle(600, 300, (255, 255, 0), Direction.LEFT, self.player2_controls, "Player 2")
        self.game_over = False
        self.winner = None

    def handle_keyboard_input(self):
        """Process keyboard input for cycle direction changes"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key in self.cycle1.key_controls and self.cycle1.alive:
                    self.cycle1.change_direction(self.cycle1.key_controls[event.key])
                # Player 2 controls
                if event.key in self.cycle2.key_controls and self.cycle2.alive:
                    self.cycle2.change_direction(self.cycle2.key_controls[event.key])
                # Restart game on spacebar
                if event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()

    def handle_mouse_input(self):
        """Process mouse clicks for game interaction"""
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.game_over:  # Left click to restart
            mouse_pos = pygame.mouse.get_pos()
            # Check if click is within restart button area
            if 300 < mouse_pos[0] < 500 and 400 < mouse_pos[1] < 450:
                self.__init__()

    def update(self):
        """Update game state"""
        if self.game_over:
            return
        self.cycle1.move()
        self.cycle2.move()

        # Check collisions
        if self.cycle1.check_collision(self.cycle2.trail) or self.cycle2.check_collision(self.cycle1.trail):
            self.game_over = True
            if not self.cycle1.alive and not self.cycle2.alive:
                self.winner = "Draw"
            elif not self.cycle1.alive:
                self.winner = self.cycle2.player_name
            else:
                self.winner = self.cycle1.player_name

    def draw(self):
        """Render game elements"""
        self.screen.fill((0, 0, 0))  # Black background
        self.cycle1.draw(self.screen)
        self.cycle2.draw(self.screen)

        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render(f"Game Over! {self.winner} Wins!", True, (255, 255, 255))
            self.screen.blit(game_over_text, (300, 300))
            restart_text = self.font.render("Click to Restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (300, 400))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while True:
            self.handle_keyboard_input()
            self.handle_mouse_input()
            self.update()
            self.draw()
            self.clock.tick(60)


def main():
    """Entry point for the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
