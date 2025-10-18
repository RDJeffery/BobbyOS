#!/usr/bin/env python3
import pygame
import subprocess
import os
import threading
import queue
import time
from pygame.locals import *

class ShellUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
        pygame.display.set_caption("Retro Shell")
        
        # Load font with fallback
        try:
            self.font = pygame.font.Font("assets/font.ttf", 14)
            self.small_font = pygame.font.Font("assets/font.ttf", 12)
        except:
            self.font = pygame.font.Font(None, 14)
            self.small_font = pygame.font.Font(None, 12)
        
        # Colors - retro terminal theme
        self.bg_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.cursor_color = (255, 255, 255)
        self.prompt_color = (255, 255, 0)
        self.error_color = (255, 0, 0)
        
        # Terminal state
        self.lines = []
        self.current_line = ""
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_lines = 12  # Fit in 240px height
        
        # Shell process
        self.proc = None
        self.output_queue = queue.Queue()
        self.running = True
        
        # Start shell process
        self.start_shell()
        
        # Add welcome message
        self.add_line("Retro Shell v1.0 - Type 'exit' to return to launcher")
        self.add_line("")
        self.update_prompt()
    
    def start_shell(self):
        """Start the shell process"""
        try:
            self.proc = subprocess.Popen(
                ["/bin/bash"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0
            )
            
            # Start output reader thread
            threading.Thread(target=self.read_output, daemon=True).start()
        except Exception as e:
            self.add_line(f"Error starting shell: {e}", self.error_color)
    
    def read_output(self):
        """Read output from shell process in background thread"""
        while self.running and self.proc:
            try:
                line = self.proc.stdout.readline()
                if line:
                    self.output_queue.put(line.rstrip())
                else:
                    break
            except:
                break
    
    def add_line(self, text, color=None):
        """Add a line to the terminal display"""
        if color is None:
            color = self.text_color
        self.lines.append((text, color))
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)
    
    def update_prompt(self):
        """Update the current prompt line"""
        # Remove old prompt if it exists
        if self.lines and self.lines[-1][0].startswith("$ "):
            self.lines.pop()
        
        # Add new prompt
        prompt = f"$ {self.current_line}"
        self.add_line(prompt, self.prompt_color)
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            elif event.key == K_RETURN:
                # Execute command
                if self.current_line.strip():
                    self.add_line(f"$ {self.current_line}")
                    if self.proc and self.proc.stdin:
                        try:
                            self.proc.stdin.write(self.current_line + "\n")
                            self.proc.stdin.flush()
                        except:
                            self.add_line("Error: Shell not responding", self.error_color)
                
                self.current_line = ""
                self.cursor_pos = 0
                self.update_prompt()
            elif event.key == K_BACKSPACE:
                if self.current_line and self.cursor_pos > 0:
                    self.current_line = self.current_line[:self.cursor_pos-1] + self.current_line[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self.update_prompt()
            elif event.key == K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                    self.update_prompt()
            elif event.key == K_RIGHT:
                if self.cursor_pos < len(self.current_line):
                    self.cursor_pos += 1
                    self.update_prompt()
            elif event.key == K_HOME:
                self.cursor_pos = 0
                self.update_prompt()
            elif event.key == K_END:
                self.cursor_pos = len(self.current_line)
                self.update_prompt()
            elif event.key == K_c and pygame.key.get_pressed()[K_LCTRL]:
                # Ctrl+C - interrupt current command
                if self.proc:
                    try:
                        self.proc.send_signal(2)  # SIGINT
                    except:
                        pass
                self.add_line("^C")
                self.current_line = ""
                self.cursor_pos = 0
                self.update_prompt()
            else:
                # Regular character input
                char = event.unicode
                if char and ord(char) >= 32:  # Printable characters
                    self.current_line = (self.current_line[:self.cursor_pos] + 
                                       char + 
                                       self.current_line[self.cursor_pos:])
                    self.cursor_pos += 1
                    self.update_prompt()
    
    def process_output(self):
        """Process output from shell"""
        while not self.output_queue.empty():
            try:
                line = self.output_queue.get_nowait()
                if line.strip():
                    self.add_line(line)
            except queue.Empty:
                break
    
    def draw(self):
        """Draw the terminal interface"""
        self.screen.fill(self.bg_color)
        
        # Draw terminal lines
        y_offset = 10
        for i, (text, color) in enumerate(self.lines):
            if i < self.max_lines:
                # Truncate long lines to fit screen
                display_text = text[:45] if len(text) > 45 else text
                text_surface = self.font.render(display_text, True, color)
                self.screen.blit(text_surface, (5, y_offset + i * 18))
        
        # Draw cursor
        if self.cursor_visible and self.lines:
            cursor_x = 5 + self.font.size(f"$ {self.current_line[:self.cursor_pos]}")[0]
            cursor_y = y_offset + (len(self.lines) - 1) * 18
            pygame.draw.line(self.screen, self.cursor_color, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + 16), 2)
        
        # Draw status bar
        status_text = f"Shell Active | Lines: {len(self.lines)}"
        status_surface = self.small_font.render(status_text, True, (100, 100, 100))
        self.screen.blit(status_surface, (5, 220))
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                else:
                    self.handle_input(event)
            
            # Process shell output
            self.process_output()
            
            # Update cursor blink
            self.cursor_timer += clock.get_time()
            if self.cursor_timer > 500:  # 500ms blink interval
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            # Draw everything
            self.draw()
            clock.tick(30)
        
        # Cleanup
        if self.proc:
            try:
                self.proc.stdin.write("exit\n")
                self.proc.stdin.flush()
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except:
                self.proc.kill()
        
        pygame.quit()

if __name__ == "__main__":
    shell_ui = ShellUI()
    shell_ui.run()