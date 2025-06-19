"""
Constants module for Taekwondo game
Contains all game settings, colors, and configuration values
"""

# Window settings
WINDOW_SIZE = (800, 600)
FRAME_RATE = 60

# Color definitions
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'MUSCLE': (200, 200, 200)
}

# Animation settings
ANIMATION_SPEED = 0.1

# Game mechanics
MOVE_COSTS = {
    'punch': 10,
    'kick': 20,
    'spin': 30,
    'block': 5
}

MOVE_POINTS = {
    'punch': 5,
    'kick': 10,
    'spin': 20
}

# Regeneration settings
ENERGY_REGEN_RATE = 10
HEALTH_REGEN_RATE = 20
POINTS_PER_TICK = 20
ENERGY_PENALTY = 10
REGEN_INTERVAL = 5.0