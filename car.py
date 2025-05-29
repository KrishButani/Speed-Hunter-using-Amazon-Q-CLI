"""
Speed Hunter - A simple car chase game
Enhanced player car class with improved graphics
"""
import pygame
import math
import random

class Car:
    """Player car class with enhanced visuals"""
    
    def __init__(self, x, y, lane_count, lane_width):
        """Initialize the car"""
        self.x = x
        self.y = y - 200  # Position car higher above the bottom line (adjusted for larger screen)
        self.lane_count = lane_count
        self.lane_width = lane_width
        self.current_lane = lane_count // 2  # Start in middle lane
        self.target_x = x
        self.width = 80  # Increased car size for larger screen
        self.height = 140  # Increased car size for larger screen
        self.speed = 15  # Increased horizontal movement speed for larger screen
        
        # Animation properties
        self.tilt = 0
        self.max_tilt = 15
        self.tilt_speed = 2
        self.exhaust_timer = 0
        self.exhaust_particles = []
        
        # Load car image
        try:
            self.image = pygame.image.load("assets/car.png")
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error:
            # Create a more detailed placeholder if image not found
            self.image = self.create_car_image()
            
        # Create collision rect (slightly smaller than visual car for better gameplay)
        self.rect = pygame.Rect(x - self.width // 2 + 15, y - self.height // 2 + 15, 
                               self.width - 30, self.height - 30)
        
    def create_car_image(self):
        """Create a more detailed car image"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Car body
        body_color = (220, 0, 0)  # Red
        pygame.draw.rect(image, body_color, (5, 20, self.width - 10, self.height - 30), border_radius=10)
        
        # Car top
        pygame.draw.rect(image, body_color, (10, 5, self.width - 20, 35), border_radius=8)
        
        # Windows
        window_color = (100, 200, 255)
        pygame.draw.rect(image, window_color, (15, 10, self.width - 30, 25), border_radius=5)
        
        # Headlights
        pygame.draw.circle(image, (255, 255, 200), (20, self.height - 20), 8)
        pygame.draw.circle(image, (255, 255, 200), (self.width - 20, self.height - 20), 8)
        
        # Taillights
        pygame.draw.rect(image, (200, 0, 0), (15, 35, 8, 15))
        pygame.draw.rect(image, (200, 0, 0), (self.width - 23, 35, 8, 15))
        
        # Wheels
        wheel_color = (30, 30, 30)
        pygame.draw.rect(image, wheel_color, (0, 40, 10, 30), border_radius=5)
        pygame.draw.rect(image, wheel_color, (self.width - 10, 40, 10, 30), border_radius=5)
        pygame.draw.rect(image, wheel_color, (0, self.height - 50, 10, 30), border_radius=5)
        pygame.draw.rect(image, wheel_color, (self.width - 10, self.height - 50, 10, 30), border_radius=5)
        
        # Details
        pygame.draw.line(image, (0, 0, 0), (5, 70), (self.width - 5, 70), 2)
        pygame.draw.line(image, (0, 0, 0), (self.width // 2, 20), (self.width // 2, self.height - 10), 1)
        
        return image
        
    def move_left(self):
        """Move car to the left lane"""
        if self.current_lane > 0:
            self.current_lane -= 1
            self.target_x = self.current_lane * self.lane_width + self.lane_width // 2
            self.tilt = self.max_tilt  # Tilt right when moving left
            
    def move_right(self):
        """Move car to the right lane"""
        if self.current_lane < self.lane_count - 1:
            self.current_lane += 1
            self.target_x = self.current_lane * self.lane_width + self.lane_width // 2
            self.tilt = -self.max_tilt  # Tilt left when moving right
            
    def update(self):
        """Update car position and animations"""
        # Smoothly move towards target position
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)
            
        # Update collision rect
        self.rect.center = (self.x, self.y)
        
        # Update tilt animation
        if self.x == self.target_x:
            # Return to neutral when at target position
            if self.tilt > 0:
                self.tilt = max(0, self.tilt - self.tilt_speed)
            elif self.tilt < 0:
                self.tilt = min(0, self.tilt + self.tilt_speed)
                
        # Create exhaust particles
        self.exhaust_timer += 1
        if self.exhaust_timer >= 5:  # Create particles every 5 frames
            self.exhaust_timer = 0
            self.create_exhaust_particle()
            
        # Update exhaust particles
        self.update_exhaust_particles()
        
    def create_exhaust_particle(self):
        """Create an exhaust particle"""
        particle = {
            'x': self.x,
            'y': self.y + self.height // 2 - 10,
            'size': random.randint(4, 8),  # Larger particles for bigger screen
            'life': random.randint(10, 20),
            'color': (100, 100, 100, 200)  # Gray smoke with alpha
        }
        self.exhaust_particles.append(particle)
        
    def update_exhaust_particles(self):
        """Update exhaust particles"""
        for particle in self.exhaust_particles[:]:
            # Move particle up and slightly random
            particle['y'] += random.uniform(1, 3)
            particle['x'] += random.uniform(-0.5, 0.5)
            
            # Fade out
            particle['size'] += 0.2
            alpha = particle['color'][3] - 10
            if alpha <= 0:
                alpha = 0
            particle['color'] = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)
            
            # Decrease life
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.exhaust_particles.remove(particle)
        
    def draw(self, surface):
        """Draw the car and effects on the surface"""
        # Draw exhaust particles
        for particle in self.exhaust_particles:
            # Create a surface for the particle with alpha
            particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, particle['color'], 
                              (particle['size'], particle['size']), particle['size'])
            surface.blit(particle_surf, 
                        (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Draw car with tilt
        if self.tilt != 0:
            rotated_image = pygame.transform.rotate(self.image, self.tilt)
            new_rect = rotated_image.get_rect(center=(self.x, self.y))
            surface.blit(rotated_image, new_rect.topleft)
        else:
            surface.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
            
        # Draw headlight beams
        if random.random() < 0.7:  # Flicker effect
            light_surf = pygame.Surface((40, 100), pygame.SRCALPHA)  # Larger light beams
            light_color = (255, 255, 200, 50)  # Yellow with alpha
            
            # Left headlight beam
            points = [
                (self.x - 20, self.y + self.height // 2 - 20),
                (self.x - 40, self.y + self.height),
                (self.x, self.y + self.height)
            ]
            pygame.draw.polygon(surface, light_color, points)
            
            # Right headlight beam
            points = [
                (self.x + 20, self.y + self.height // 2 - 20),
                (self.x + 40, self.y + self.height),
                (self.x, self.y + self.height)
            ]
            pygame.draw.polygon(surface, light_color, points)
        
    def reset(self):
        """Reset car to starting position"""
        self.current_lane = self.lane_count // 2
        self.target_x = self.current_lane * self.lane_width + self.lane_width // 2
        self.x = self.target_x
        self.tilt = 0
        self.exhaust_particles = []
