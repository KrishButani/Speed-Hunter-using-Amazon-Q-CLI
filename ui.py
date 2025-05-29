"""
Speed Hunter - A simple car chase game
Enhanced UI with interactive elements and improved visuals
"""
import pygame
import os
import math

class UI:
    """UI class for displaying game information with enhanced visuals"""
    
    def __init__(self):
        """Initialize the UI"""
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 200, 0)
        
        # Fonts
        self.font_small = pygame.font.SysFont('arial', 28)  # Increased font size
        self.font_medium = pygame.font.SysFont('arial', 42)  # Increased font size
        self.font_large = pygame.font.SysFont('arial', 92)  # Increased font size
        
        # High score file
        self.high_score_file = "highscore.txt"
        
        # UI elements
        self.score_animation = 0
        self.pulse_effect = 0
        self.pulse_direction = 1
        
        # Create button surfaces
        self.button_width = 300  # Increased button size
        self.button_height = 70  # Increased button size
        self.button_normal = self.create_button(self.BLUE)
        self.button_hover = self.create_button(self.GREEN)
        
        # Load or create speedometer
        try:
            self.speedometer = pygame.image.load("assets/speedometer.png")
            self.speedometer = pygame.transform.scale(self.speedometer, (180, 180))  # Larger speedometer
        except:
            self.speedometer = self.create_speedometer()
            
        # Load or create dashboard
        try:
            self.dashboard = pygame.image.load("assets/dashboard.png")
            # Scale dashboard to fit the new screen width
            self.dashboard = pygame.transform.scale(self.dashboard, (1200, 120))  # Adjusted for 1200x800 screen
        except:
            self.dashboard = self.create_dashboard()
            
    def create_button(self, color):
        """Create a button surface with nice styling"""
        button = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        
        # Draw button with gradient
        for i in range(self.button_height):
            # Create gradient effect
            factor = i / self.button_height
            r = min(255, int(color[0] * (1 + factor * 0.5)))
            g = min(255, int(color[1] * (1 + factor * 0.5)))
            b = min(255, int(color[2] * (1 + factor * 0.5)))
            pygame.draw.line(button, (r, g, b), (0, i), (self.button_width, i))
            
        # Add border and highlight
        pygame.draw.rect(button, (255, 255, 255, 100), (0, 0, self.button_width, 5))  # Top highlight
        pygame.draw.rect(button, (0, 0, 0, 100), (0, self.button_height-5, self.button_width, 5))  # Bottom shadow
        pygame.draw.rect(button, (255, 255, 255), (0, 0, self.button_width, self.button_height), 2)  # Border
        
        return button
        
    def create_speedometer(self):
        """Create a speedometer graphic"""
        size = 180  # Increased size
        speedometer = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw outer circle
        pygame.draw.circle(speedometer, (50, 50, 50), (size//2, size//2), size//2)
        pygame.draw.circle(speedometer, (200, 200, 200), (size//2, size//2), size//2, 3)
        
        # Draw speed markings
        for i in range(0, 220, 20):
            angle = i * 1.5 - 240  # Convert to degrees, -120 to +120
            angle_rad = math.radians(angle)
            start_pos = (size//2 + int(size//2 * 0.7 * math.cos(angle_rad)),
                        size//2 + int(size//2 * 0.7 * math.sin(angle_rad)))
            end_pos = (size//2 + int(size//2 * 0.8 * math.cos(angle_rad)),
                      size//2 + int(size//2 * 0.8 * math.sin(angle_rad)))
            pygame.draw.line(speedometer, (255, 255, 255), start_pos, end_pos, 2)
            
            # Add numbers for major markings
            if i % 40 == 0:
                text_pos = (size//2 + int(size//2 * 0.55 * math.cos(angle_rad)),
                           size//2 + int(size//2 * 0.55 * math.sin(angle_rad)))
                text = pygame.font.SysFont('arial', 18).render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=text_pos)
                speedometer.blit(text, text_rect)
                
        # Add "km/h" text
        kmh_text = pygame.font.SysFont('arial', 18).render("km/h", True, (200, 200, 200))
        speedometer.blit(kmh_text, (size//2 - kmh_text.get_width()//2, size//2 + 30))
        
        return speedometer
        
    def create_dashboard(self):
        """Create a dashboard graphic"""
        width, height = 1200, 120  # Adjusted for 1200x800 screen
        dashboard = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw main dashboard background
        pygame.draw.rect(dashboard, (40, 40, 40), (0, 0, width, height))
        pygame.draw.rect(dashboard, (60, 60, 60), (10, 10, width-20, height-20))
        
        # Add some details
        pygame.draw.line(dashboard, (100, 100, 100), (width//3, 10), (width//3, height-10), 2)
        pygame.draw.line(dashboard, (100, 100, 100), (width*2//3, 10), (width*2//3, height-10), 2)
        
        # Add metallic effect
        for i in range(10, height-10, 4):
            alpha = 50 if i % 8 == 0 else 20
            pygame.draw.line(dashboard, (255, 255, 255, alpha), (10, i), (width-10, i))
            
        return dashboard
        
    def draw_needle(self, surface, center, value, max_value, radius, color):
        """Draw a speedometer needle"""
        # Ensure value is within the range of the speedometer
        value = min(value, max_value)
        
        # Calculate angle based on the value (240 degree sweep from -120 to +120)
        max_angle = 240  # Total sweep angle of the speedometer
        angle = (value / max_value) * max_angle - 120  # -120 to +120 degrees
        angle_rad = math.radians(angle)
        
        # Calculate needle endpoint with proper scaling
        end_x = center[0] + int(radius * 0.7 * math.cos(angle_rad))
        end_y = center[1] + int(radius * 0.7 * math.sin(angle_rad))
        
        # Draw needle with proper thickness
        pygame.draw.line(surface, color, center, (end_x, end_y), 4)  # Thicker needle
        
        # Draw center cap
        pygame.draw.circle(surface, (200, 200, 200), center, 8)  # Larger cap
        pygame.draw.circle(surface, (100, 100, 100), center, 8, 1)
        
    def draw(self, surface, score, high_score, missed, max_missed, game_speed=10):
        """Draw the enhanced UI elements"""
        # Update animation values
        self.pulse_effect += 0.05 * self.pulse_direction
        if self.pulse_effect > 1.0 or self.pulse_effect < 0.0:
            self.pulse_direction *= -1
            
        if score > self.score_animation:
            self.score_animation += 1
            
        # Draw dashboard at the bottom
        surface.blit(self.dashboard, (0, surface.get_height() - 120))
        
        # Draw speedometer
        speedometer_pos = (1050, surface.get_height() - 60)  # Adjusted position
        surface.blit(self.speedometer, (speedometer_pos[0] - 90, speedometer_pos[1] - 90))
        
        # Draw needle based on game speed (adjusted for higher speeds)
        # Max speed on speedometer is now 200 km/h
        self.draw_needle(surface, speedometer_pos, game_speed, 200, 90, self.RED)
        
        # Draw digital speed readout with larger font for emphasis (integer only)
        speed_font = pygame.font.SysFont('arial', 36, bold=True)  # Increased font size
        speed_text = speed_font.render(f"{int(game_speed)} km/h", True, self.YELLOW)
        surface.blit(speed_text, (speedometer_pos[0] - speed_text.get_width() // 2, 
                                speedometer_pos[1] + 30))
        
        # Draw score with animation
        score_color = self.YELLOW if score > 0 and score == self.score_animation else self.WHITE
        score_text = self.font_medium.render(f"Score: {self.score_animation}", True, score_color)
        surface.blit(score_text, (40, surface.get_height() - 100))
        
        # Draw high score
        high_score_text = self.font_small.render(f"High Score: {high_score}", True, self.WHITE)
        surface.blit(high_score_text, (40, surface.get_height() - 50))
        
        # Draw missed objects counter with visual indicator
        missed_text = self.font_small.render(f"Missed: ", True, self.WHITE)
        surface.blit(missed_text, (350, surface.get_height() - 70))
        
        # Draw missed indicators
        for i in range(max_missed):
            color = self.RED if i < missed else (100, 100, 100)
            if i == missed - 1 and missed > 0:  # Make the latest missed indicator pulse
                pulse = int(50 * self.pulse_effect)
                color = (255, pulse, pulse)
            pygame.draw.circle(surface, color, (450 + i * 35, surface.get_height() - 60), 15)  # Larger indicators
            
        # Draw warning if close to game over
        if missed >= max_missed - 1:
            warning_text = self.font_medium.render("WARNING!", True, self.RED)
            # Make warning text pulse
            pulse_scale = 1.0 + 0.2 * self.pulse_effect
            scaled_warning = pygame.transform.scale(warning_text, 
                                                  (int(warning_text.get_width() * pulse_scale),
                                                   int(warning_text.get_height() * pulse_scale)))
            surface.blit(scaled_warning, 
                        (surface.get_width() // 2 - scaled_warning.get_width() // 2, 30))
            
    def draw_button(self, surface, text, center_pos, is_hover=False):
        """Draw an interactive button"""
        button = self.button_hover if is_hover else self.button_normal
        button_rect = button.get_rect(center=center_pos)
        surface.blit(button, button_rect)
        
        # Draw text
        text_surf = self.font_medium.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=center_pos)
        surface.blit(text_surf, text_rect)
        
        return button_rect
            
    def draw_game_over(self, surface, score, high_score):
        """Draw the enhanced game over screen"""
        # Semi-transparent overlay with gradient
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        for i in range(surface.get_height()):
            alpha = min(180, int(180 * (i / surface.get_height() * 1.5)))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, i), (surface.get_width(), i))
        surface.blit(overlay, (0, 0))
        
        # Game over text with shadow effect
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        shadow_text = self.font_large.render("GAME OVER", True, (0, 0, 0))
        
        # Draw shadow with offset
        surface.blit(shadow_text, 
                    (surface.get_width() // 2 - game_over_text.get_width() // 2 + 5, 
                     surface.get_height() // 3 + 5))
        
        # Draw main text
        surface.blit(game_over_text, 
                    (surface.get_width() // 2 - game_over_text.get_width() // 2, 
                     surface.get_height() // 3))
        
        # Final score with animation
        if score > self.score_animation:
            self.score_animation += 1
            
        score_text = self.font_medium.render(f"Final Score: {self.score_animation}", True, self.WHITE)
        surface.blit(score_text, 
                    (surface.get_width() // 2 - score_text.get_width() // 2, 
                     surface.get_height() // 2))
        
        # High score with glow effect if new high score
        if score >= high_score:
            # Create pulsing glow effect
            glow_size = int(15 * (0.5 + self.pulse_effect))  # Larger glow
            glow_surf = pygame.Surface((500 + glow_size*2, 70 + glow_size*2), pygame.SRCALPHA)  # Larger surface
            pygame.draw.rect(glow_surf, (255, 215, 0, 100), 
                            (0, 0, 500 + glow_size*2, 70 + glow_size*2), 
                            border_radius=15)
            
            glow_pos = (surface.get_width() // 2 - 250 - glow_size, 
                       surface.get_height() // 2 + 70 - glow_size)
            surface.blit(glow_surf, glow_pos)
            
            high_score_text = self.font_medium.render("NEW HIGH SCORE!", True, self.YELLOW)
        else:
            high_score_text = self.font_medium.render(f"High Score: {high_score}", True, self.WHITE)
            
        surface.blit(high_score_text, 
                    (surface.get_width() // 2 - high_score_text.get_width() // 2, 
                     surface.get_height() // 2 + 70))
        
        # Interactive buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Restart button
        restart_rect = self.draw_button(
            surface, 
            "Play Again", 
            (surface.get_width() // 2, surface.get_height() // 2 + 180),
            self.is_point_in_rect(mouse_pos, 
                                 surface.get_width() // 2 - self.button_width // 2,
                                 surface.get_height() // 2 + 180 - self.button_height // 2,
                                 self.button_width, 
                                 self.button_height)
        )
        
        # Quit button
        quit_rect = self.draw_button(
            surface, 
            "Quit Game", 
            (surface.get_width() // 2, surface.get_height() // 2 + 280),
            self.is_point_in_rect(mouse_pos, 
                                 surface.get_width() // 2 - self.button_width // 2,
                                 surface.get_height() // 2 + 280 - self.button_height // 2,
                                 self.button_width, 
                                 self.button_height)
        )
        
        return {"restart": restart_rect, "quit": quit_rect}
        
    def is_point_in_rect(self, point, x, y, width, height):
        """Check if a point is inside a rectangle"""
        return (x <= point[0] <= x + width and 
                y <= point[1] <= y + height)
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    return int(f.read().strip())
            return 0
        except:
            return 0
            
    def save_high_score(self, high_score):
        """Save high score to file"""
        try:
            with open(self.high_score_file, 'w') as f:
                f.write(str(high_score))
        except:
            pass  # Silently fail if we can't write the file
