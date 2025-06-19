import ui
import random
import time
import oldmain

# Initialize pygame
ui.init()

# Set up screen
screen = ui.display.set_mode((600, 400))
ui.display.set_caption("Press Keys to Perform Actions")

# Set up fonts
font = ui.font.SysFont("Arial, 24")

# Player's initial stats
player = {
    "hearts": 5,  # 5 hearts initially
    "energy": 100,  # starting energy
    "points": 100,  # starting points (independent from hearts)
    "match_time": 0  # match starts at 0 seconds
}

# List to hold text messages that will be displayed
messages = []

# Functions for actions
def punch():
    """Punch action."""
    if player["energy"] >= 10:
        player["energy"] -= 10
        player["points"] -= 5  # Punch removes 5 points
        player["hearts"] -= 1   # Punch removes 1 heart
        messages.append("You threw a punch! (-5 points, -1 heart, -10 energy)")
    else:
        messages.append("Not enough energy to punch!")

def kick():
    """Kick action."""
    if player["energy"] >= 20:
        player["energy"] -= 20
        player["points"] -= 10  # Kick removes 10 points
        player["hearts"] -= 1   # Kick removes 1 heart
        messages.append("You kicked! (-10 points, -1 heart, -20 energy)")
    else:
        messages.append("Not enough energy to kick!")

def spinning_kick():
    """Spinning kick action."""
    if player["energy"] >= 30:
        player["energy"] -= 30
        player["points"] -= 20  # Spinning kick removes 20 points
        player["hearts"] -= 1   # Spinning kick removes 1 heart
        messages.append("You performed a spinning kick! (-20 points, -1 heart, -30 energy)")
    else:
        messages.append("Not enough energy for a spinning kick!")

def block():
    """Block action with a 50% chance to stop the attack."""
    if player["energy"] >= 5:
        player["energy"] -= 5
        chance = random.random()
        if chance < 0.5:
            messages.append("You successfully blocked the attack! (-5 energy)")
        else:
            messages.append("Block failed, you took damage! (-5 energy)")
    else:
        messages.append("Not enough energy to block!")

def hearts_or_points():
    """Hearts action."""
    messages.append("You have {player['hearts']} hearts, worth {player['points']} points.")

def match():
    """Start or manage match."""
    player["match_time"] += 5
    messages.append("Match time: {player['match_time']} seconds")
    
    # Every 5 seconds, gain either 1 heart or 20 points
    if player["match_time"] % 5 == 0:
        if player["hearts"] < 5:
            # If the player has fewer than 5 hearts, gain a heart
            player["hearts"] += 1
            messages.append("You gained a heart! (+1 heart)")
        else:
            # If max hearts reached, gain points instead
            player["points"] += 20  # Gain points when max hearts are reached
            messages.append("You gained 20 points!")

def energy():
    """Energy status."""
    messages.append("You have {player['energy']} energy left.")

# Create the dictionary that maps abbreviations to functions
my_dict = {
    ui.K_SPACE: punch,  # Spacebar for punch
    ui.K_k: kick,       # 'K' key for kick
    ui.K_s: spinning_kick,  # 'S' key for spinning kick
    ui.K_b: block,      # 'B' key for block
    ui.K_h: hearts_or_points,  # 'H' key for hearts/points
    ui.K_m: match,      # 'M' key for match
    ui.K_e: energy,     # 'E' key for energy
}

def draw_messages():
    """Render and display the messages on the screen."""
    screen.fill((0, 0, 0))  # Fill the screen with black
    
    # Draw the player's stats
    stats_text = "HEARTS: {player['hearts']} | ENERGY: {player['energy']} | POINTS: {player['points']}"
    stats_surface = font.render(stats_text, True, (255, 255, 255))
    screen.blit(stats_surface, (10, 10))
    
    # Draw all messages
    y_offset = 50
    for message in messages[-5:]:  # Show last 5 messages
        message_surface = font.render(message, True, (255, 255, 255))
        screen.blit(message_surface, (10, y_offset))
        y_offset += 30

    ui.display.flip()  # Update the screen

# Set up the main game loop
running = True
while running:
    for event in ui.event.get():
        if event.type == ui.QUIT:
            running = False
        
        # Handle keydown event
        if event.type == ui.KEYDOWN:
            if event.key in my_dict:
                my_dict[event.key]()  # Call the corresponding function
    
    # Draw the messages on the screen
    draw_messages()
    
    # Pause for a short time to make the game loop responsive
    time.sleep(0.1)

# Quit pygame when done
ui.quit()
