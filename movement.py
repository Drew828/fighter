# movement.py - Move actions and upgrades
# =======================================

import random
from typing import List

def try_move(fighter, messages: List[str], cost: int, points: int, pose: str, msg: str) -> bool:
    try:
        cost = min(cost, 100)
        if fighter.eng >= cost:
            fighter.eng = max(0, fighter.eng - cost)
            points_earned = points + fighter.offense * 2
            fighter.pts += points_earned
            messages.append(f"{msg} (+{points_earned} pts)")
            fighter.set_pose(pose)
            return True
        else:
            messages.append(f"Not enough energy to {msg.lower()}!")
            return False
    except AttributeError as e:
        print(f"Move error: {e}")
        return False

def punc(fighter, messages: List[str]) -> None:
    try_move(fighter, messages, 10, 5, "punch", "Punch")

def kic(fighter, messages: List[str]) -> None:
    try_move(fighter, messages, 20, 10, "kick", "Kick")

def spk(fighter, messages: List[str]) -> None:
    try_move(fighter, messages, 30, 20, "spin", "Spinning Kick")

def blk(fighter, messages: List[str]) -> None:
    try:
        if fighter.eng >= 5:
            fighter.eng -= 5
            chance = 0.5 + (fighter.defense * 0.05)
            if random.random() < chance:
                messages.append("Block successful!")
            else:
                messages.append("Block failed! -20 health")
                fighter.health = max(0, fighter.health - 20)
            fighter.set_pose("block")
        else:
            messages.append("Not enough energy to block!")
    except AttributeError as e:
        print(f"Block error: {e}")

def upgrade(fighter, messages: List[str], stat: str) -> None:
    try:
        if fighter.upg_tokens > 0:
            fighter.upg_tokens -= 1
            current_value = getattr(fighter, stat, 0)
            setattr(fighter, stat, current_value + 1)
            messages.append(f"Upgraded {stat.capitalize()}!")
        else:
            messages.append("No upgrade tokens!")
    except AttributeError as e:
        print(f"Upgrade error: {e}")