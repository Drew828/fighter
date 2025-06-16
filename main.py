import random
import time

# Player's initial stats
player = {
    "hearts": 5,  # 5 hearts initially
    "energy": 100,  # starting energy
    "points": 100,  # starting points (independent from hearts)
    "match_time": 0  # match starts at 0 seconds
}

# Functions for actions
def punch():
    """Punch action."""
    if player["energy"] >= 10:
        player["energy"] -= 10
        player["points"] -= 5  # Punch removes 5 points
        player["hearts"] -= 1   # Punch removes 1 heart
        print("You threw a punch! (-5 points, -1 heart, -10 energy)")
    else:
        print("Not enough energy to punch!")

def kick():
    """Kick action."""
    if player["energy"] >= 20:
        player["energy"] -= 20
        player["points"] -= 10  # Kick removes 10 points
        player["hearts"] -= 1   # Kick removes 1 heart
        print("You kicked! (-10 points, -1 heart, -20 energy)")
    else:
        print("Not enough energy to kick!")

def spinning_kick():
    """Spinning kick action."""
    if player["energy"] >= 30:
        player["energy"] -= 30
        player["points"] -= 20  # Spinning kick removes 20 points
        player["hearts"] -= 1   # Spinning kick removes 1 heart
        print("You performed a spinning kick! (-20 points, -1 heart, -30 energy)")
    else:
        print("Not enough energy for a spinning kick!")

def block():
    """Block action with a 50% chance to stop the attack."""
    if player["energy"] >= 5:
        player["energy"] -= 5
        chance = random.random()
        if chance < 0.5:
            print("You successfully blocked the attack! (-5 energy)")
        else:
            print("Block failed, you took damage! (-5 energy)")
    else:
        print("Not enough energy to block!")

def hearts_or_points():
    """Hearts action."""
    # Print the number of hearts and points independently
    print("You have " + str(player["hearts"]) + " hearts, worth " + str(player["points"]) + " points.")

def match():
    """Start or manage match."""
    player["match_time"] += 5
    print("Match time: {player['match_time']} seconds")
    
    # Every 5 seconds, gain either 1 heart or 20 points
    if player["match_time"] % 5 == 0:
        if player["hearts"] < 5:
            # If the player has fewer than 5 hearts, gain a heart
            player["hearts"] += 1
            print("You gained a heart! (+1 heart)")
        else:
            # If max hearts reached, gain points instead
            player["points"] += 20  # Gain points when max hearts are reached
            print("You gained 20 points!")

def energy():
    """Energy status."""
    print("You have " + str(player["energy"]) + " energy left.")

# Create the dictionary that maps abbreviations to functions
my_dict = {
    "punc": punch,
    "kic": kick,
    "spk": spinning_kick,
    "blk": block,
    "hrt": hearts_or_points,
    "mtc": match,
    "eng": energy,
}

# Example of how to call functions using the dictionary
actions = [
    "punc",  # Punch
    "kic",   # Kick
    "spk",   # Spinning Kick
    "blk",   # Block
    "mtc",   # 5-second match update
    "eng",   # Check energy
    "hrt"    # Check hearts and points
]

# Using a loop to call functions from the dictionary
for action in actions:
    try:
        my_dict[action]()  # Call each function from the dictionary
    except KeyError as e:
        print(f"KeyError: {e} - Please make sure the key is spelled correctly.")
    except Exception as e:
        print(f"An error occurred: {e}")
