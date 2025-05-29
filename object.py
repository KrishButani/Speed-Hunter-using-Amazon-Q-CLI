"""
Speed Hunter - A simple car chase game
Enhanced road object logic with improved visuals
"""
import pygame
import random
import math

class RoadObject:
    """Road object class for collectibles and obstacles with enhanced visuals"""
    
    def __init__(self, x, y, is_obstacle, lane_width):
        """Initialize the road object"""
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle
        self.collected = False
        
        # Set size based on type
        if is_obstacle:
            self.width = 70
            self.height = 70
        else:
            self.width = 40
            self.height = 40
            
        # Animation properties
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-3, 3)
        self.scale_factor = 1.0
        self.scale_direction = 0.01
        self.glow_size = 0
        self.glow_max = 10
        self.glow_direction = 0.5
        
        # Shadow properties
        self.shadow_offset = 5
        
        # Load appropriate image
        image_path = "assets/obstacle.png" if is_obstacle else "assets/coin.png"
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error:
            # Create a more detailed placeholder if image not found
            if is_obstacle:
                self.image = self.create_obstacle_image()
            else:
                self.image = self.create_coin_image()
                
        # Create collision rect (slightly smaller than visual object for better gameplay)
        self.rect = pygame.Rect(x - self.width // 2 + 5, y - self.height // 2 + 5, 
                               self.width - 10, self.height - 10)
                               
        # Create particle effects
        self.particles = []
        if not is_obstacle:
            self.create_sparkle_particles()
        
    def create_obstacle_image(self):
        """Create a detailed obstacle image"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Choose a random obstacle type
        obstacle_type = random.choice(['rock', 'oil', 'cone'])
        
        if obstacle_type == 'rock':
            # Draw a rock
            color = (100, 100, 100)  # Gray
            points = []
            for i in range(8):
                angle = i * (2 * math.pi / 8)
                radius = self.width // 2 - random.randint(0, 10)
                x = self.width // 2 + int(radius * math.cos(angle))
                y = self.height // 2 + int(radius * math.sin(angle))
                points.append((x, y))
            pygame.draw.polygon(image, color, points)
            
            # Add some details
            for _ in range(5):
                x = random.randint(self.width // 4, self.width * 3 // 4)
                y = random.randint(self.height // 4, self.height * 3 // 4)
                radius = random.randint(2, 6)
                pygame.draw.circle(image, (50, 50, 50), (x, y), radius)
                
        elif obstacle_type == 'oil':
            # Draw an oil spill
            color = (20, 20, 20)  # Almost black
            pygame.draw.ellipse(image, color, (5, 10, self.width - 10, self.height - 20))
            
            # Add shine effect
            shine_color = (50, 50, 80)
            pygame.draw.ellipse(image, shine_color, (15, 20, self.width - 30, self.height // 3))
            
        else:  # cone
            # Draw a traffic cone
            cone_color = (255, 100, 0)  # Orange
            
            # Base
            pygame.draw.rect(image, (50, 50, 50), 
                            (self.width // 4, self.height - 15, self.width // 2, 10))
            
            # Cone shape
            points = [
                (self.width // 2, 10),
                (self.width // 4, self.height - 15),
                (self.width * 3 // 4, self.height - 15)
            ]
            pygame.draw.polygon(image, cone_color, points)
            
            # Stripes
            for y in range(self.height - 25, 20, -15):
                pygame.draw.line(image, (255, 255, 255),
                               (self.width // 2 - (y - 20) // 3, y),
                               (self.width // 2 + (y - 20) // 3, y), 2)
        
        return image
        
    def create_coin_image(self):
        """Create a detailed coin image"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Choose a random collectible type
        collectible_type = random.choice(['coin', 'gem', 'star'])
        
        if collectible_type == 'coin':
            # Draw a gold coin
            color = (255, 215, 0)  # Gold
            pygame.draw.circle(image, color, (self.width // 2, self.height // 2), self.width // 2 - 2)
            pygame.draw.circle(image, (200, 170, 0), (self.width // 2, self.height // 2), self.width // 2 - 2, 2)
            
            # Add dollar sign
            font = pygame.font.SysFont('arial', self.width // 2)
            text = font.render('$', True, (200, 170, 0))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            image.blit(text, text_rect)
            
        elif collectible_type == 'gem':
            # Draw a gem
            color = (50, 100, 255)  # Blue
            points = [
                (self.width // 2, 5),
                (self.width - 5, self.height // 2),
                (self.width // 2, self.height - 5),
                (5, self.height // 2)
            ]
            pygame.draw.polygon(image, color, points)
            
            # Add shine
            pygame.draw.line(image, (200, 200, 255), 
                           (self.width // 4, self.height // 4),
                           (self.width // 2, self.height // 2), 3)
            
        else:  # star
            # Draw a star
            color = (255, 255, 0)  # Yellow
            points = []
            for i in range(10):
                angle = math.pi / 2 + i * math.pi / 5
                radius = self.width // 2 - 2 if i % 2 == 0 else self.width // 4
                x = self.width // 2 + int(radius * math.cos(angle))
                y = self.height // 2 + int(radius * math.sin(angle))
                points.append((x, y))
            pygame.draw.polygon(image, color, points)
        
        return image
        
    def create_sparkle_particles(self):
        """Create sparkle particles for collectibles"""
        if self.is_obstacle:
            return
            
        for _ in range(3):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(self.width // 3, self.width // 2)
            particle = {
                'x': self.width // 2 + math.cos(angle) * distance,
                'y': self.height // 2 + math.sin(angle) * distance,
                'size': random.uniform(1, 3),
                'life': random.randint(10, 30),
                'max_life': random.randint(10, 30)
            }
            self.particles.append(particle)
        
    def update(self, speed):
        """Update object position and animation"""
        # Move down the screen
        self.y += speed
        
        # Update collision rect
        self.rect.center = (self.x, self.y)
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Update animation based on object type
        if self.is_obstacle:
            # Obstacles just rotate
            pass
        else:
            # Collectibles pulse and glow
            self.scale_factor += self.scale_direction
            if self.scale_factor > 1.2 or self.scale_factor < 0.8:
                self.scale_direction *= -1
                
            self.glow_size += self.glow_direction
            if self.glow_size > self.glow_max or self.glow_size < 0:
                self.glow_direction *= -1
                
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
                # Create a new particle to replace it
                if random.random() < 0.7:
                    self.create_sparkle_particles()
        
    def draw(self, surface):
        """Draw the object with enhanced visuals"""
        # Draw shadow
        shadow_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.is_obstacle:
            shadow_shape = pygame.transform.rotate(self.image, self.rotation)
        else:
            width = int(self.width * self.scale_factor)
            height = int(self.height * self.scale_factor)
            shadow_shape = pygame.transform.scale(self.image, (width, height))
            shadow_shape = pygame.transform.rotate(shadow_shape, self.rotation)
            
        shadow_rect = shadow_shape.get_rect()
        shadow_surf.fill((0, 0, 0, 100))  # Semi-transparent black
        shadow_surf = pygame.transform.scale(shadow_surf, shadow_rect.size)
        
        # Draw shadow with offset
        shadow_pos = (self.x - shadow_rect.width // 2 + self.shadow_offset, 
                     self.y - shadow_rect.height // 2 + self.shadow_offset)
        surface.blit(shadow_surf, shadow_pos)
        
        # Draw glow for collectibles
        if not self.is_obstacle and self.glow_size > 0:
            glow_surf = pygame.Surface((self.width + self.glow_size * 2, 
                                      self.height + self.glow_size * 2), pygame.SRCALPHA)
            glow_color = (255, 255, 0, 100)  # Yellow with alpha
            pygame.draw.circle(glow_surf, glow_color, 
                              (glow_surf.get_width() // 2, glow_surf.get_height() // 2), 
                              self.width // 2 + self.glow_size)
            glow_pos = (self.x - glow_surf.get_width() // 2, self.y - glow_surf.get_height() // 2)
            surface.blit(glow_surf, glow_pos)
        
        # Draw sparkle particles for collectibles
        if not self.is_obstacle:
            for particle in self.particles:
                # Calculate alpha based on life
                alpha = int(255 * (particle['life'] / particle['max_life']))
                color = (255, 255, 255, alpha)
                
                # Draw at object's position plus particle offset
                pos = (int(self.x - self.width // 2 + particle['x']), 
                      int(self.y - self.height // 2 + particle['y']))
                
                # Draw a small star shape
                size = particle['size']
                points = []
                for i in range(10):
                    angle = i * math.pi / 5
                    radius = size * 2 if i % 2 == 0 else size
                    px = pos[0] + radius * math.cos(angle)
                    py = pos[1] + radius * math.sin(angle)
                    points.append((px, py))
                
                # Create a surface for the particle with alpha
                particle_surf = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
                pygame.draw.polygon(particle_surf, (255, 255, 255), 
                                   [(p[0] - pos[0] + size * 2, p[1] - pos[1] + size * 2) for p in points])
                surface.blit(particle_surf, (pos[0] - size * 2, pos[1] - size * 2))
        
        # Apply rotation and scaling for the main object
        if self.is_obstacle:
            # For obstacles, just rotate
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
        else:
            # For collectibles, apply pulsing effect and rotation
            width = int(self.width * self.scale_factor)
            height = int(self.height * self.scale_factor)
            scaled_image = pygame.transform.scale(self.image, (width, height))
            rotated_image = pygame.transform.rotate(scaled_image, self.rotation)
            
        # Get the rect for the rotated/scaled image
        rect = rotated_image.get_rect(center=(self.x, self.y))
        
        # Draw the object
        surface.blit(rotated_image, rect)
        
    def check_collision(self, car):
        """Check if this object collides with the car"""
        return self.rect.colliderect(car.rect)
