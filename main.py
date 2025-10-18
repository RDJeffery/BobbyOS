#!/usr/bin/env python3
import pygame, json, os, subprocess, time
from pygame.locals import *

class GameUI:
    def __init__(self):
        # --- Basic setup ---
        pygame.init()
        self.screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
        pygame.display.set_caption("Pi GameUI")
        
        # Load assets
        self.font = pygame.font.Font(os.path.join('assets', 'font.ttf'), 16)
        self.small_font = pygame.font.Font(os.path.join('assets', 'font.ttf'), 12)
        self.bg = pygame.image.load(os.path.join('assets', 'bg.png')).convert()
        self.clock = pygame.time.Clock()
        
        # Load config
        config_path = os.path.join('config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.menu_items = json.load(f)
        else:
            self.menu_items = [{"label": "Demo", "command": "echo 'Hello World'"}]
        
        # Menu layout settings (adjusted for taskbar)
        self.grid_cols = 2  # 2 columns for 320px width
        self.grid_rows = 3  # 3 rows to leave space for taskbar
        self.item_width = 140
        self.item_height = 50
        self.item_spacing = 10
        self.start_x = 20
        self.start_y = 20
        
        self.selected = 0
        self.running = True
        self.current_state = "splash"  # splash, menu
        self.splash_start_time = time.time()
        self.splash_duration = 3.0  # 3 seconds
        
        # Splash screen properties
        self.splash_alpha = 0
        self.splash_fade_speed = 2
        
        # Initialize gamepad support
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)
            print(f"Gamepad {i}: {joystick.get_name()}")
        
        # Input handling
        self.key_repeat_delay = 200  # ms
        self.key_repeat_interval = 100  # ms
        self.last_key_time = 0
        self.key_repeat_timer = 0
        
        # Animation properties
        self.selection_animation = 0.0
        self.selection_animation_speed = 0.1
        self.pulse_animation = 0.0
        self.pulse_speed = 0.05
        
        # Taskbar properties
        self.taskbar_height = 30
        self.show_settings_menu = False
        self.settings_menu_items = [
            {"label": "Shutdown", "command": "sudo shutdown now"},
            {"label": "Reboot", "command": "sudo reboot"},
            {"label": "Sleep", "command": "sudo systemctl suspend"}
        ]
        self.settings_menu_selected = 0
        
    def show_splash_screen(self):
        """Display splash screen with fade in/out animation"""
        current_time = time.time()
        elapsed = current_time - self.splash_start_time
        
        # Create splash surface
        splash_surface = pygame.Surface((320, 240))
        splash_surface.fill((102, 102, 153))  # Black background
        
        # Draw logo/gamepad icon (simple pixel art style)
        # Create a simple gamepad icon
        gamepad_color = (255, 255, 255)
        # Main body
        pygame.draw.rect(splash_surface, gamepad_color, (120, 100, 80, 40))
        # Left stick
        pygame.draw.circle(splash_surface, gamepad_color, (140, 120), 15)
        # Right stick
        pygame.draw.circle(splash_surface, gamepad_color, (180, 120), 15)
        # D-pad
        pygame.draw.rect(splash_surface, gamepad_color, (100, 110, 20, 20))
        # Buttons
        pygame.draw.circle(splash_surface, gamepad_color, (200, 110), 8)
        pygame.draw.circle(splash_surface, gamepad_color, (210, 120), 8)
        pygame.draw.circle(splash_surface, gamepad_color, (200, 130), 8)
        pygame.draw.circle(splash_surface, gamepad_color, (190, 120), 8)
        
        # Title text
        title_font = pygame.font.Font(os.path.join('assets', 'font.ttf'), 24)
        title_text = title_font.render("Pi GameUI", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(160, 60))
        splash_surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(os.path.join('assets', 'font.ttf'), 12)
        subtitle_text = subtitle_font.render("Retro Gaming Launcher", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(160, 80))
        splash_surface.blit(subtitle_text, subtitle_rect)
        
        # Handle fade animation
        if elapsed < 1.0:  # Fade in
            self.splash_alpha = min(255, int(elapsed * 255))
        elif elapsed < self.splash_duration - 1.0:  # Hold
            self.splash_alpha = 255
        else:  # Fade out
            fade_out_time = elapsed - (self.splash_duration - 1.0)
            self.splash_alpha = max(0, int(255 - fade_out_time * 255))
        
        # Apply alpha and blit
        splash_surface.set_alpha(self.splash_alpha)
        self.screen.blit(splash_surface, (0, 0))
        
        # Check if splash is complete
        if elapsed >= self.splash_duration:
            self.current_state = "menu"
    
    def show_main_menu(self):
        """Display the main menu with grid layout and animations"""
        # Update animations
        self.selection_animation += self.selection_animation_speed
        self.pulse_animation += self.pulse_speed
        
        # Draw background with custom color instead of image
        self.screen.fill((102, 102, 153))
        
        # Draw menu items in grid
        for i, item in enumerate(self.menu_items):
            # Calculate grid position
            row = i // self.grid_cols
            col = i % self.grid_cols
            
            x = self.start_x + col * (self.item_width + self.item_spacing)
            y = self.start_y + row * (self.item_height + self.item_spacing)
            
            # Add selection animation offset
            if i == self.selected:
                # Pulsing effect for selected item
                pulse_offset = int(3 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse_animation * 360).x))
                x += pulse_offset
                y += pulse_offset
            
            # Create item surface
            item_surface = pygame.Surface((self.item_width, self.item_height))
            
            # Highlight selected item
            if i == self.selected:
                # Animated selection background
                selection_intensity = int(80 + 20 * abs(pygame.math.Vector2(1, 0).rotate(self.selection_animation * 360).x))
                pygame.draw.rect(item_surface, (selection_intensity, selection_intensity, selection_intensity), 
                               (0, 0, self.item_width, self.item_height))
                pygame.draw.rect(item_surface, (120, 120, 120), (2, 2, self.item_width-4, self.item_height-4))
                text_color = (255, 255, 255)
                border_color = (255, 255, 0)
            else:
                # Draw normal background
                pygame.draw.rect(item_surface, (40, 40, 40), (0, 0, self.item_width, self.item_height))
                pygame.draw.rect(item_surface, (60, 60, 60), (2, 2, self.item_width-4, self.item_height-4))
                text_color = (200, 200, 200)
                border_color = (100, 100, 100)
            
            # Draw border with animation
            border_width = 3 if i == self.selected else 2
            pygame.draw.rect(item_surface, border_color, (0, 0, self.item_width, self.item_height), border_width)
            
            # Draw icon placeholder (simple pixel art style)
            icon_size = 24
            icon_x = (self.item_width - icon_size) // 2
            icon_y = 8
            
            # Create a simple icon based on item type
            if "retro" in item["label"].lower() or "game" in item["label"].lower():
                # Game controller icon
                pygame.draw.rect(item_surface, text_color, (icon_x + 4, icon_y + 8, 16, 8))
                pygame.draw.circle(item_surface, text_color, (icon_x + 8, icon_y + 12), 3)
                pygame.draw.circle(item_surface, text_color, (icon_x + 16, icon_y + 12), 3)
            elif "pac" in item["label"].lower():
                # Pac-Man icon
                pygame.draw.circle(item_surface, text_color, (icon_x + 12, icon_y + 12), 10)
                # Draw mouth
                pygame.draw.polygon(item_surface, (0, 0, 0), [
                    (icon_x + 12, icon_y + 12),
                    (icon_x + 20, icon_y + 8),
                    (icon_x + 20, icon_y + 16)
                ])
            elif "tetris" in item["label"].lower():
                # Tetris blocks icon
                pygame.draw.rect(item_surface, text_color, (icon_x + 6, icon_y + 6, 6, 6))
                pygame.draw.rect(item_surface, text_color, (icon_x + 12, icon_y + 6, 6, 6))
                pygame.draw.rect(item_surface, text_color, (icon_x + 6, icon_y + 12, 6, 6))
                pygame.draw.rect(item_surface, text_color, (icon_x + 18, icon_y + 12, 6, 6))
            elif "snake" in item["label"].lower():
                # Snake icon
                pygame.draw.rect(item_surface, text_color, (icon_x + 6, icon_y + 10, 12, 4))
                pygame.draw.rect(item_surface, text_color, (icon_x + 8, icon_y + 8, 4, 4))
                pygame.draw.rect(item_surface, text_color, (icon_x + 12, icon_y + 6, 4, 4))
            elif "settings" in item["label"].lower():
                # Settings gear icon
                pygame.draw.circle(item_surface, text_color, (icon_x + 12, icon_y + 12), 8, 2)
                pygame.draw.line(item_surface, text_color, (icon_x + 12, icon_y + 4), (icon_x + 12, icon_y + 8), 2)
                pygame.draw.line(item_surface, text_color, (icon_x + 4, icon_y + 12), (icon_x + 8, icon_y + 12), 2)
            elif "shutdown" in item["label"].lower():
                # Power button icon
                pygame.draw.circle(item_surface, text_color, (icon_x + 12, icon_y + 12), 8, 2)
                pygame.draw.line(item_surface, text_color, (icon_x + 12, icon_y + 4), (icon_x + 12, icon_y + 8), 2)
            else:
                # Generic app icon
                pygame.draw.rect(item_surface, text_color, (icon_x + 4, icon_y + 4, 16, 16), 2)
                pygame.draw.rect(item_surface, text_color, (icon_x + 6, icon_y + 6, 12, 12))
            
            # Draw item text with shadow effect
            text = self.small_font.render(item["label"], True, (0, 0, 0))  # Shadow
            text_rect = text.get_rect(center=(self.item_width // 2 + 1, self.item_height - 7))
            item_surface.blit(text, text_rect)
            
            text = self.small_font.render(item["label"], True, text_color)  # Main text
            text_rect = text.get_rect(center=(self.item_width // 2, self.item_height - 8))
            item_surface.blit(text, text_rect)
            
            # Blit item to screen
            self.screen.blit(item_surface, (x, y))
        
        # Draw selection indicator (arrow) with animation
        if self.selected < len(self.menu_items):
            row = self.selected // self.grid_cols
            col = self.selected % self.grid_cols
            x = self.start_x + col * (self.item_width + self.item_spacing)
            y = self.start_y + row * (self.item_height + self.item_spacing)
            
            # Animated arrow pointing to selected item
            arrow_x = x - 15
            arrow_y = y + self.item_height // 2
            
            # Pulsing arrow
            pulse_scale = 1.0 + 0.2 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse_animation * 360).x)
            arrow_points = [
                (arrow_x, arrow_y),
                (arrow_x + int(10 * pulse_scale), arrow_y - int(5 * pulse_scale)),
                (arrow_x + int(10 * pulse_scale), arrow_y + int(5 * pulse_scale))
            ]
            pygame.draw.polygon(self.screen, (255, 255, 0), arrow_points)
        
        # Draw taskbar
        self.draw_taskbar()
    
    def draw_taskbar(self):
        """Draw the taskbar at the bottom of the screen"""
        taskbar_y = 240 - self.taskbar_height
        
        # Draw taskbar background with gradient effect
        for i in range(self.taskbar_height):
            color_intensity = int(60 + (i / self.taskbar_height) * 20)
            pygame.draw.line(self.screen, (color_intensity, color_intensity, color_intensity), 
                           (0, taskbar_y + i), (320, taskbar_y + i))
        
        # Draw taskbar border
        pygame.draw.rect(self.screen, (150, 150, 150), (0, taskbar_y, 320, self.taskbar_height), 2)
        
        # Draw power button (left side)
        power_button_rect = pygame.Rect(5, taskbar_y + 5, 20, 20)
        power_color = (200, 100, 100) if not self.show_settings_menu else (255, 150, 150)
        pygame.draw.rect(self.screen, power_color, power_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), power_button_rect, 2)
        
        # Power icon
        pygame.draw.circle(self.screen, (255, 255, 255), (15, taskbar_y + 15), 6, 2)
        pygame.draw.line(self.screen, (255, 255, 255), (15, taskbar_y + 9), (15, taskbar_y + 12), 2)
        
        # Draw digital clock (center)
        current_time = time.strftime("%H:%M:%S")
        clock_text = self.small_font.render(current_time, True, (255, 255, 255))
        clock_rect = clock_text.get_rect(center=(160, taskbar_y + 15))
        
        # Clock background
        clock_bg_rect = pygame.Rect(clock_rect.x - 5, clock_rect.y - 2, clock_rect.width + 10, clock_rect.height + 4)
        pygame.draw.rect(self.screen, (40, 40, 40), clock_bg_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), clock_bg_rect, 1)
        
        self.screen.blit(clock_text, clock_rect)
        
        # Draw settings button (right side)
        settings_button_rect = pygame.Rect(295, taskbar_y + 5, 20, 20)
        settings_color = (100, 150, 200)
        pygame.draw.rect(self.screen, settings_color, settings_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), settings_button_rect, 2)
        
        # Settings gear icon
        pygame.draw.circle(self.screen, (255, 255, 255), (305, taskbar_y + 15), 6, 2)
        pygame.draw.line(self.screen, (255, 255, 255), (305, taskbar_y + 9), (305, taskbar_y + 12), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (299, taskbar_y + 15), (302, taskbar_y + 15), 1)
        
        # Draw settings context menu if open
        if self.show_settings_menu:
            self.draw_settings_menu()
    
    def draw_settings_menu(self):
        """Draw the settings context menu"""
        menu_width = 120
        menu_height = len(self.settings_menu_items) * 25 + 10
        # Center the menu on screen
        menu_x = (320 - menu_width) // 2
        menu_y = (240 - menu_height) // 2
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((320, 240))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Menu background with shadow
        shadow_rect = pygame.Rect(menu_x + 3, menu_y + 3, menu_width, menu_height)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect)
        
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (80, 80, 80), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 2)
        
        # Draw menu items
        for i, item in enumerate(self.settings_menu_items):
            item_y = menu_y + 5 + i * 25
            item_rect = pygame.Rect(menu_x + 5, item_y, menu_width - 10, 20)
            
            if i == self.settings_menu_selected:
                pygame.draw.rect(self.screen, (120, 120, 120), item_rect)
                pygame.draw.rect(self.screen, (180, 180, 180), item_rect, 1)
                text_color = (255, 255, 255)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), item_rect, 1)
                text_color = (220, 220, 220)
            
            # Draw item text with shadow
            text = self.small_font.render(item["label"], True, (0, 0, 0))  # Shadow
            text_rect = text.get_rect(center=(menu_x + menu_width // 2 + 1, item_y + 11))
            self.screen.blit(text, text_rect)
            
            text = self.small_font.render(item["label"], True, text_color)  # Main text
            text_rect = text.get_rect(center=(menu_x + menu_width // 2, item_y + 10))
            self.screen.blit(text, text_rect)
    
    def handle_events(self):
        """Handle all input events"""
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if self.current_state == "menu":
                    self.handle_keyboard_navigation(event.key)
                elif self.current_state == "splash":
                    # Allow skipping splash with any key
                    self.current_state = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle touchscreen input
                if self.current_state == "menu":
                    self.handle_touch_input(event.pos)
            elif event.type == pygame.JOYBUTTONDOWN:
                # Handle gamepad button input
                if self.current_state == "menu":
                    self.handle_gamepad_button(event.button, event.joy)
            elif event.type == pygame.JOYHATMOTION:
                # Handle gamepad D-pad input
                if self.current_state == "menu":
                    self.handle_gamepad_hat(event.value, event.joy)
            elif event.type == pygame.JOYAXISMOTION:
                # Handle gamepad analog stick input
                if self.current_state == "menu":
                    self.handle_gamepad_axis(event.axis, event.value, event.joy)
        
        # Handle key repeat for smooth navigation (only when settings menu is closed)
        if self.current_state == "menu" and not self.show_settings_menu:
            keys = pygame.key.get_pressed()
            if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
                if current_time - self.last_key_time > self.key_repeat_delay:
                    if current_time - self.key_repeat_timer > self.key_repeat_interval:
                        if keys[K_UP]:
                            self.move_selection(-self.grid_cols)
                        elif keys[K_DOWN]:
                            self.move_selection(self.grid_cols)
                        elif keys[K_LEFT]:
                            self.move_selection(-1)
                        elif keys[K_RIGHT]:
                            self.move_selection(1)
                        self.key_repeat_timer = current_time
            else:
                self.last_key_time = current_time
                self.key_repeat_timer = current_time
    
    def move_selection(self, direction):
        """Move selection in the given direction"""
        new_selection = self.selected + direction
        if 0 <= new_selection < len(self.menu_items):
            self.selected = new_selection
    
    def handle_keyboard_navigation(self, key):
        """Handle keyboard navigation"""
        if self.show_settings_menu:
            # Handle settings menu navigation
            if key == K_UP:
                self.settings_menu_selected = (self.settings_menu_selected - 1) % len(self.settings_menu_items)
            elif key == K_DOWN:
                self.settings_menu_selected = (self.settings_menu_selected + 1) % len(self.settings_menu_items)
            elif key in (K_RETURN, K_SPACE):
                self.launch_app(self.settings_menu_items[self.settings_menu_selected])
                self.show_settings_menu = False
            elif key == K_ESCAPE:
                self.show_settings_menu = False
        else:
            # Handle main menu navigation
            if key == K_UP:
                self.move_selection(-self.grid_cols)
            elif key == K_DOWN:
                self.move_selection(self.grid_cols)
            elif key == K_LEFT:
                self.move_selection(-1)
            elif key == K_RIGHT:
                self.move_selection(1)
            elif key in (K_RETURN, K_SPACE):
                self.launch_app(self.menu_items[self.selected])
            elif key == K_ESCAPE:
                self.running = False
            elif key == K_F1:  # F1 key to open settings menu
                self.show_settings_menu = True
                self.settings_menu_selected = 0
    
    def handle_touch_input(self, pos):
        """Handle touchscreen input"""
        mouse_x, mouse_y = pos
        
        # Check if touch is on taskbar buttons first
        if self.handle_taskbar_touch(mouse_x, mouse_y):
            return
        
        # Check if touch is on a menu item
        for i, item in enumerate(self.menu_items):
            row = i // self.grid_cols
            col = i % self.grid_cols
            x = self.start_x + col * (self.item_width + self.item_spacing)
            y = self.start_y + row * (self.item_height + self.item_spacing)
            item_rect = pygame.Rect(x, y, self.item_width, self.item_height)
            if item_rect.collidepoint(mouse_x, mouse_y):
                self.selected = i
                self.launch_app(item)
                break
    
    def handle_taskbar_touch(self, mouse_x, mouse_y):
        """Handle touch input on taskbar elements"""
        taskbar_y = 240 - self.taskbar_height
        
        # Check power button (left side)
        power_button_rect = pygame.Rect(5, taskbar_y + 5, 20, 20)
        if power_button_rect.collidepoint(mouse_x, mouse_y):
            self.show_settings_menu = not self.show_settings_menu
            if not self.show_settings_menu:
                self.settings_menu_selected = 0
            return True
        
        # Check settings button (right side)
        settings_button_rect = pygame.Rect(295, taskbar_y + 5, 20, 20)
        if settings_button_rect.collidepoint(mouse_x, mouse_y):
            self.show_settings_menu = not self.show_settings_menu
            if not self.show_settings_menu:
                self.settings_menu_selected = 0
            return True
        
        # Check settings menu items if open
        if self.show_settings_menu:
            menu_width = 120
            menu_height = len(self.settings_menu_items) * 25 + 10
            # Center the menu on screen (same as draw_settings_menu)
            menu_x = (320 - menu_width) // 2
            menu_y = (240 - menu_height) // 2
            
            for i, item in enumerate(self.settings_menu_items):
                item_y = menu_y + 5 + i * 25
                item_rect = pygame.Rect(menu_x + 5, item_y, menu_width - 10, 20)
                if item_rect.collidepoint(mouse_x, mouse_y):
                    self.settings_menu_selected = i
                    self.launch_app(item)
                    self.show_settings_menu = False
                    return True
        
        # If clicked outside settings menu, close it
        if self.show_settings_menu:
            self.show_settings_menu = False
            self.settings_menu_selected = 0
            return True
        
        return False
    
    def handle_gamepad_button(self, button, joystick_id):
        """Handle gamepad button presses"""
        # Common gamepad button mappings
        if button == 0:  # A button (Xbox) / Cross (PlayStation)
            self.launch_app(self.menu_items[self.selected])
        elif button == 1:  # B button (Xbox) / Circle (PlayStation)
            self.running = False
        elif button == 2:  # X button (Xbox) / Square (PlayStation)
            pass  # Could be used for settings
        elif button == 3:  # Y button (Xbox) / Triangle (PlayStation)
            pass  # Could be used for info
    
    def handle_gamepad_hat(self, hat_value, joystick_id):
        """Handle gamepad D-pad input"""
        x, y = hat_value
        if y == 1:  # Up
            self.move_selection(-self.grid_cols)
        elif y == -1:  # Down
            self.move_selection(self.grid_cols)
        elif x == -1:  # Left
            self.move_selection(-1)
        elif x == 1:  # Right
            self.move_selection(1)
    
    def handle_gamepad_axis(self, axis, value, joystick_id):
        """Handle gamepad analog stick input"""
        # Dead zone to prevent drift
        dead_zone = 0.3
        if abs(value) < dead_zone:
            return
        
        if axis == 1:  # Left stick Y axis
            if value < -dead_zone:  # Up
                self.move_selection(-self.grid_cols)
            elif value > dead_zone:  # Down
                self.move_selection(self.grid_cols)
        elif axis == 0:  # Left stick X axis
            if value < -dead_zone:  # Left
                self.move_selection(-1)
            elif value > dead_zone:  # Right
                self.move_selection(1)
    
    def launch_app(self, app):
        """Launch the selected application"""
        try:
            print(f"Launching: {app['label']} - {app['command']}")
            
            # Hide the launcher window (minimize)
            pygame.display.iconify()
            
            # Launch app and wait for it to complete
            result = subprocess.run(app["command"], shell=True, capture_output=True, text=True)
            
            # Show the launcher again
            pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
            
            # Print any output from the app
            if result.stdout:
                print(f"App output: {result.stdout}")
            if result.stderr:
                print(f"App error: {result.stderr}")
            if result.returncode != 0:
                print(f"App exited with code: {result.returncode}")
                
        except Exception as e:
            print(f"Error launching app: {e}")
            # Make sure to restore the launcher window even if there's an error
            pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            if self.current_state == "splash":
                self.show_splash_screen()
            elif self.current_state == "menu":
                self.show_main_menu()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.run()
