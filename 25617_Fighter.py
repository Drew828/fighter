import pygame
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Set up the screen (window)
screen = pygame.display.set_mode((800, 600))  # Width=800, Height=600
pygame.display.set_caption("Taekwondo Simulation")

# Set up colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up fonts
font = pygame.font.SysFont("Arial", 24)

# Player stats
player = {
    "hearts": 5,
    "health": 100,  # 5 hearts * 20
    "energy": 100,
    "points": 0,
    "match_time": 0,
    "offense": 0,
    "defense": 0,
    "upg_tokens": 0
}

# Messages list
messages = []

# Stickman class (Blocky with joints)
class Fighter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pose = "idle"
        self.pose_timer = 0

    def set_pose(self, pose):
        self.pose = pose
        self.pose_timer = pygame.time.get_ticks() + 800  # ms

    def update(self):
        if self.pose != "idle" and pygame.time.get_ticks() > self.pose_timer:
            self.pose = "idle"

    def draw(self, surface):
        # Basic human figure with joints (blocky)
        color = WHITE
        
        # Head
        head = (self.x, self.y - 60)
        # Neck to torso
        neck = (self.x, self.y - 50)
        torso = (self.x, self.y)

        # Arm positions (shoulder, elbow, hand)
        shoulder_left = (self.x - 25, self.y - 40)
        elbow_left = (self.x - 45, self.y - 30)
        hand_left = (self.x - 60, self.y - 20)

        shoulder_right = (self.x + 25, self.y - 40)
        elbow_right = (self.x + 45, self.y - 30)
        hand_right = (self.x + 60, self.y - 20)

        # Leg positions (thigh, knee, foot)
        thigh_left = (self.x - 20, self.y + 20)
        knee_left = (self.x - 40, self.y + 50)
        foot_left = (self.x - 50, self.y + 70)

        thigh_right = (self.x + 20, self.y + 20)
        knee_right = (self.x + 40, self.y + 50)
        foot_right = (self.x + 50, self.y + 70)

        # Draw the head
        pygame.draw.circle(surface, color, head, 10)
        
        # Draw the torso
        pygame.draw.line(surface, color, neck, torso, 2)

        # Draw the arms (shoulder -> elbow -> hand)
        pygame.draw.line(surface, color, shoulder_left, elbow_left, 2)
        pygame.draw.line(surface, color, elbow_left, hand_left, 2)
        pygame.draw.line(surface, color, shoulder_right, elbow_right, 2)
        pygame.draw.line(surface, color, elbow_right, hand_right, 2)

        # Draw the legs (thigh -> knee -> foot)
        pygame.draw.line(surface, color, torso, thigh_left, 2)
        pygame.draw.line(surface, color, thigh_left, knee_left, 2)
        pygame.draw.line(surface, color, knee_left, foot_left, 2)
        
        pygame.draw.line(surface, color, torso, thigh_right, 2)
        pygame.draw.line(surface, color, thigh_right, knee_right, 2)
        pygame.draw.line(surface, color, knee_right, foot_right, 2)

# Initialize fighter
fighter = Fighter(400, 300)

# Draw messages and stats
def draw_ui():
    screen.fill(BLACK)  # Black background

    # Stats display
    stats_text = "HEARTS: {player['hearts']} | ENERGY: {int(player['energy'])} | HEALTH: {int(player['health'])} | POINTS: {player['points']} | TOKENS: {player['upg_tokens']}"
    stats_surface = font.render(stats_text, True, WHITE)
    screen.blit(stats_surface, (10, 10))

    # Draw health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 40, 200, 30))  # Red background for health
    pygame.draw.rect(screen, (0, 255, 0), (10, 40, int(player["health"]), 30))  # Green health fill

    # Draw energy bar
    pygame.draw.rect(screen, (255, 255, 0), (10, 80, 200, 30))  # Yellow background for energy
    pygame.draw.rect(screen, (0, 0, 255), (10, 80, int(player["energy"] * 2), 30))  # Blue energy fill

    # Draw the stickman/fighter
    fighter.draw(screen)

    # Key bindings help text
    help_text = [
        "Controls:",
        "Space: Punch",
        "K: Kick",
        "S: Spinning Kick",
        "B: Block",
        "1: Upgrade Offense",
        "2: Upgrade Defense",
        "3: Upgrade Health"
    ]
    y_offset_help = 200
    for line in help_text:
        help_surface = font.render(line, True, WHITE)
        screen.blit(help_surface, (600, y_offset_help))
        y_offset_help += 30

    pygame.display.flip()

# Game loop
last_time = time.time()
running = True
while running:
    dt = time.time() - last_time
    last_time = time.time()

    # Handle key presses for actions
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        # Call the punch function here if needed
        pass
    if keys[pygame.K_k]:
        # Call the kick function here if needed
        pass
    if keys[pygame.K_s]:
        # Call the spin_kick function here if needed
        pass
    if keys[pygame.K_b]:
        # Call the block function here if needed
        pass
    if keys[pygame.K_1]:
        # Upgrade offense
        pass
    if keys[pygame.K_2]:
        # Upgrade defense
        pass
    if keys[pygame.K_3]:
        # Upgrade health
        pass

    # Passive energy regen
    if player["energy"] < 100:
        player["energy"] += 0.1

    # Call the draw_ui function to draw everything
    draw_ui()

    # Add a short delay to control the frame rate
    pygame.time.Clock().tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()
sys.exit()
