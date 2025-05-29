#!/usr/bin/env python3
"""
Speed Hunter - A simple car chase game
Main game loop and logic with enhanced visuals
"""
import pygame
import sys
import random
from car import Car
from object import RoadObject
from ui import UI

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 1200  # Increased from 800 to 1200
SCREEN_HEIGHT = 800  # Increased from 600 to 800
FPS = 60
LANE_COUNT = 3
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

class Game:
    """Main game class for Speed Hunter"""
    
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Speed Hunter")
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.road_img = self.load_image("assets/road.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create game objects
        self.car = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, LANE_COUNT, LANE_WIDTH)
        self.ui = UI()
        
        # Game state
        self.score = 0
        self.high_score = self.ui.load_high_score()
        self.missed_objects = 0
        self.max_missed = 5  # Changed from 3 to 5
        self.game_over = False
        self.game_speed = 10  # Initial speed set to 10 km/h
        self.coins_for_speed = 0  # Counter for coins collected for speed increase
        self.menu_active = True
        self.speed_notification = None
        self.speed_notification_timer = 0
        
        # Object spawning
        self.objects = []
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between spawns
        
        # Road animation
        self.road_y = 0
        
        # Particle effects
        self.particles = []
        
        # Sound effects
        try:
            pygame.mixer.init()
            self.coin_sound = pygame.mixer.Sound("assets/coin.wav")
            self.crash_sound = pygame.mixer.Sound("assets/crash.wav")
            self.engine_sound = pygame.mixer.Sound("assets/engine.wav")
            self.engine_sound.play(-1)  # Loop engine sound
            self.engine_sound.set_volume(0.3)
        except:
            self.coin_sound = None
            self.crash_sound = None
            self.engine_sound = None
        
    def load_image(self, path, width=None, height=None):
        """Load an image and optionally resize it"""
        try:
            image = pygame.image.load(path)
        except pygame.error:
            # Create a placeholder if image not found
            if width and height:
                image = pygame.Surface((width, height))
                image.fill(GRAY)
                # Draw some road lines
                for i in range(1, LANE_COUNT):
                    x = i * LANE_WIDTH
                    pygame.draw.line(image, WHITE, (x, 0), (x, height), 2)
                # Draw dashed lines in the middle of lanes
                for i in range(LANE_COUNT):
                    x = i * LANE_WIDTH + LANE_WIDTH // 2
                    for y in range(0, height, 40):
                        pygame.draw.line(image, WHITE, (x, y), (x, y + 20), 2)
            else:
                image = pygame.Surface((50, 50))
                image.fill((255, 0, 255))  # Magenta for missing textures
                
        if width and height:
            image = pygame.transform.scale(image, (width, height))
            
        return image
        
    def spawn_object(self):
        """Spawn a new road object"""
        # Choose a random lane
        lane = random.randint(0, LANE_COUNT - 1)
        
        # Determine object type (80% collectible, 20% obstacle)
        is_obstacle = random.random() < 0.2
        
        # Create the object
        obj = RoadObject(lane * LANE_WIDTH + LANE_WIDTH // 2, -50, is_obstacle, LANE_WIDTH)
        self.objects.append(obj)
        
    def create_particles(self, x, y, color, count=10):
        """Create particle effects"""
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'size': random.randint(2, 6),
                'color': color,
                'life': random.randint(20, 40)
            }
            self.particles.append(particle)
            
    def update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            # Move particle
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Decrease life
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
    def update(self):
        """Update game state"""
        if self.game_over or self.menu_active:
            return
            
        # Update car
        self.car.update()
        
        # Update road animation
        self.road_y = (self.road_y + self.game_speed) % SCREEN_HEIGHT
        
        # Update objects
        for obj in self.objects[:]:
            obj.update(self.game_speed)
            
            # Check if object is off screen
            if obj.y > SCREEN_HEIGHT:
                self.objects.remove(obj)
                if not obj.is_obstacle and not obj.collected:
                    self.missed_objects += 1
                    if self.missed_objects >= self.max_missed:
                        self.game_over = True
                        if self.crash_sound:
                            self.crash_sound.play()
                        
            # Check collision with car
            elif obj.check_collision(self.car):
                if obj.is_obstacle:
                    self.game_over = True
                    # Create explosion particles
                    self.create_particles(obj.x, obj.y, (255, 100, 0), 30)
                    if self.crash_sound:
                        self.crash_sound.play()
                else:
                    self.score += 10
                    obj.collected = True
                    self.objects.remove(obj)
                    
                    # Count coins for speed increase
                    self.coins_for_speed += 1
                    if self.coins_for_speed >= 10:
                        # Increase speed by exactly 10 km/h and ensure it's an integer
                        self.game_speed = int(self.game_speed) + 10
                        self.coins_for_speed = 0
                        self.speed_notification = f"Speed +10: {int(self.game_speed)} km/h"
                        self.speed_notification_timer = 60  # Show for 60 frames (1 second)
                    
                    # Create sparkle particles
                    self.create_particles(obj.x, obj.y, (255, 215, 0), 20)
                    if self.coin_sound:
                        self.coin_sound.play()
                    
        # Spawn new objects
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_object()
            self.spawn_timer = 0
            
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            
        # Update game state
        self.update_particles()
        
        # Update speed notification
        if self.speed_notification_timer > 0:
            self.speed_notification_timer -= 1
            if self.speed_notification_timer <= 0:
                self.speed_notification = None
            
    def draw(self):
        """Draw the game state"""
        # Draw road
        self.screen.blit(self.road_img, (0, self.road_y - SCREEN_HEIGHT))
        self.screen.blit(self.road_img, (0, self.road_y))
        
        # Draw objects
        for obj in self.objects:
            obj.draw(self.screen)
            
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(
                self.screen, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
            
        # Draw car
        self.car.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.screen, self.score, self.high_score, 
                    self.missed_objects, self.max_missed, self.game_speed)
                    
        # Draw speed notification if active
        if self.speed_notification:
            notification_font = pygame.font.SysFont('arial', 36)
            notification_text = notification_font.render(self.speed_notification, True, (255, 255, 0))
            
            # Make it pulse/fade based on remaining time
            alpha = int(255 * (self.speed_notification_timer / 60))
            notification_text.set_alpha(alpha)
            
            # Position in the middle of the screen
            self.screen.blit(notification_text, 
                           (self.screen.get_width() // 2 - notification_text.get_width() // 2, 
                            self.screen.get_height() // 2 - 100))
        
        # Draw game over screen
        if self.game_over:
            button_rects = self.ui.draw_game_over(self.screen, self.score, self.high_score)
            return button_rects
            
        # Draw main menu
        if self.menu_active:
            self.draw_main_menu()
            
        return None
            
    def draw_main_menu(self):
        """Draw the main menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_font = pygame.font.SysFont('arial', 92, bold=True)  # Increased font size
        title_text = title_font.render("SPEED HUNTER", True, (255, 255, 0))
        self.screen.blit(title_text, 
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        
        # Subtitle
        subtitle_font = pygame.font.SysFont('arial', 32)  # Increased font size
        subtitle_text = subtitle_font.render("Collect coins, avoid obstacles!", True, (255, 255, 255))
        self.screen.blit(subtitle_text, 
                        (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 250))
        
        # Get mouse position for button hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Start button
        start_rect = self.ui.draw_button(
            self.screen, 
            "Start Game", 
            (SCREEN_WIDTH // 2, 400),
            self.ui.is_point_in_rect(mouse_pos, 
                                   SCREEN_WIDTH // 2 - self.ui.button_width // 2,
                                   400 - self.ui.button_height // 2,
                                   self.ui.button_width, 
                                   self.ui.button_height)
        )
        
        # Quit button
        quit_rect = self.ui.draw_button(
            self.screen, 
            "Quit Game", 
            (SCREEN_WIDTH // 2, 500),
            self.ui.is_point_in_rect(mouse_pos, 
                                   SCREEN_WIDTH // 2 - self.ui.button_width // 2,
                                   500 - self.ui.button_height // 2,
                                   self.ui.button_width, 
                                   self.ui.button_height)
        )
        
        # Controls info
        controls_font = pygame.font.SysFont('arial', 28)  # Increased font size
        controls_text = controls_font.render("Use LEFT and RIGHT arrow keys to move", True, (200, 200, 200))
        self.screen.blit(controls_text, 
                        (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 600))
        
        # Missed coins info
        missed_font = pygame.font.SysFont('arial', 24)
        missed_text = missed_font.render(f"Game over after missing {self.max_missed} coins", True, (200, 200, 200))
        self.screen.blit(missed_text, 
                        (SCREEN_WIDTH // 2 - missed_text.get_width() // 2, 650))
        
        return {"start": start_rect, "quit": quit_rect}
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                
            elif event.type == pygame.KEYDOWN:
                if self.menu_active:
                    if event.key == pygame.K_RETURN:
                        self.menu_active = False
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                elif not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.car.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.car.move_right()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu_active = True
                else:  # Game over state
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    
                    if self.menu_active:
                        menu_buttons = self.draw_main_menu()
                        if menu_buttons["start"].collidepoint(mouse_pos):
                            self.menu_active = False
                        elif menu_buttons["quit"].collidepoint(mouse_pos):
                            self.quit_game()
                            
                    elif self.game_over:
                        button_rects = self.draw()
                        if button_rects["restart"].collidepoint(mouse_pos):
                            self.reset_game()
                        elif button_rects["quit"].collidepoint(mouse_pos):
                            self.quit_game()
                    
    def reset_game(self):
        """Reset the game state"""
        self.score = 0
        self.missed_objects = 0
        self.game_over = False
        self.game_speed = 10  # Reset to initial speed of exactly 10 km/h (integer)
        self.coins_for_speed = 0
        self.objects = []
        self.particles = []
        self.car.reset()
        self.ui.score_animation = 0
        self.speed_notification = None
        self.speed_notification_timer = 0
        
    def quit_game(self):
        """Save high score and quit the game"""
        self.ui.save_high_score(self.high_score)
        if self.engine_sound:
            self.engine_sound.stop()
        pygame.quit()
        sys.exit()
        
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
