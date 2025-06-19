import pygame
import time
import display
import movement
from fighter import Fighter

ATTACK_RANGE = 70
PUNCH_DAMAGE = 5
KICK_DAMAGE = 10
SPIN_KICK_DAMAGE = 15

def is_in_range(attacker, defender):
    return abs(attacker.x - defender.x) <= ATTACK_RANGE

def play_game():
    def create_new_fighter(x, facing_right, color):
        fighter = Fighter(x, display.RING_FLOOR_HEIGHT - 100, facing_right=facing_right, color=color)
        # Add cooldown tracking for each move
        fighter.cooldowns = {
            "punch": 0,
            "kick": 0,
            "spinkick": 0
        }
        return fighter

    def reset_game():
        nonlocal fighter1, fighter2, messages, accum_time, energy_penalty_time1, energy_penalty_time2
        fighter1 = create_new_fighter(200, True, (220,0,0))
        fighter2 = create_new_fighter(600, False, (100,0,128))
        messages.clear()
        accum_time = 0
        energy_penalty_time1 = 0
        energy_penalty_time2 = 0

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Taekwondo Simulation - Two Fighters")
    font = pygame.font.SysFont(None, 24)

    messages = []
    fighter1 = create_new_fighter(200, True, (0,0,0))
    fighter2 = create_new_fighter(600, False, (100,0,128))
    clock = pygame.time.Clock()
    last_time = time.time()
    accum_time = 0
    energy_penalty_time1 = 0
    energy_penalty_time2 = 0
    running = True

    while running:
        dt = time.time() - last_time
        last_time = time.time()
        accum_time += dt
        energy_penalty_time1 += dt
        energy_penalty_time2 += dt

        now = time.time()  # For cooldown checks

        new_game_button = display.draw_ui(screen, font, fighter1, fighter2, messages)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    reset_game()

        keys = pygame.key.get_pressed()
        # --- Player 1 Controls (WASD + F/G/H/R/1/2/3) ---
        if keys[pygame.K_a]: fighter1.perform_action("left")
        if keys[pygame.K_d]: fighter1.perform_action("right")
        if keys[pygame.K_w]: fighter1.perform_action("jump")
        if keys[pygame.K_f]:  # Punch
            if now - fighter1.cooldowns["punch"] >= 0.5:
                movement.punc(fighter1, messages)
                fighter1.cooldowns["punch"] = now
                if is_in_range(fighter1, fighter2) and fighter2.hrt > 0:
                    fighter2.take_damage(PUNCH_DAMAGE)
                    messages.append("P1 punched P2!")
        if keys[pygame.K_g]:  # Kick
            if now - fighter1.cooldowns["kick"] >= 1.0:
                movement.kic(fighter1, messages)
                fighter1.cooldowns["kick"] = now
                if is_in_range(fighter1, fighter2) and fighter2.hrt > 0:
                    fighter2.take_damage(KICK_DAMAGE)
                    messages.append("P1 kicked P2!")
        if keys[pygame.K_h]:  # Spinning Kick
            if now - fighter1.cooldowns["spinkick"] >= 2.0:
                movement.spk(fighter1, messages)
                fighter1.cooldowns["spinkick"] = now
                if is_in_range(fighter1, fighter2) and fighter2.hrt > 0:
                    fighter2.take_damage(SPIN_KICK_DAMAGE)
                    messages.append("P1 spinning kicked P2!")
        if keys[pygame.K_r]: movement.blk(fighter1, messages)
        if keys[pygame.K_1]: movement.upgrade(fighter1, messages, "offense")
        if keys[pygame.K_2]: movement.upgrade(fighter1, messages, "defense")
        if keys[pygame.K_3]: movement.upgrade(fighter1, messages, "health")

        # --- Player 2 Controls (Arrows + Space/K/L/J/8/9/0) ---
        if keys[pygame.K_LEFT]: fighter2.perform_action("left")
        if keys[pygame.K_RIGHT]: fighter2.perform_action("right")
        if keys[pygame.K_UP]: fighter2.perform_action("jump")
        if keys[pygame.K_SPACE]:  # Punch
            if now - fighter2.cooldowns["punch"] >= 0.5:
                movement.punc(fighter2, messages)
                fighter2.cooldowns["punch"] = now
                if is_in_range(fighter2, fighter1) and fighter1.hrt > 0:
                    fighter1.take_damage(PUNCH_DAMAGE)
                    messages.append("P2 punched P1!")
        if keys[pygame.K_k]:  # Kick
            if now - fighter2.cooldowns["kick"] >= 1.0:
                movement.kic(fighter2, messages)
                fighter2.cooldowns["kick"] = now
                if is_in_range(fighter2, fighter1) and fighter1.hrt > 0:
                    fighter1.take_damage(KICK_DAMAGE)
                    messages.append("P2 kicked P1!")
        if keys[pygame.K_l]:  # Spinning Kick
            if now - fighter2.cooldowns["spinkick"] >= 2.0:
                movement.spk(fighter2, messages)
                fighter2.cooldowns["spinkick"] = now
                if is_in_range(fighter2, fighter1) and fighter1.hrt > 0:
                    fighter1.take_damage(SPIN_KICK_DAMAGE)
                    messages.append("P2 spinning kicked P1!")
        if keys[pygame.K_j]: movement.blk(fighter2, messages)
        if keys[pygame.K_8]: movement.upgrade(fighter2, messages, "offense")
        if keys[pygame.K_9]: movement.upgrade(fighter2, messages, "defense")
        if keys[pygame.K_0]: movement.upgrade(fighter2, messages, "health")

        # Regenerate energy
        if fighter1.eng < 100:
            fighter1.eng = min(fighter1.eng + 10 * dt, 100)
        if fighter2.eng < 100:
            fighter2.eng = min(fighter2.eng + 10 * dt, 100)

        # Passive points and health
        if accum_time >= 5.0:
            accum_time -= 5.0
            fighter1.pts += 20
            fighter2.pts += 20
            if fighter1.health < 100 and fighter1.hrt > 0:
                fighter1.health = min(fighter1.health + 20, 100)
            elif fighter1.hrt < 5 and fighter1.hrt > 0:
                fighter1.hrt += 1
            if fighter2.health < 100 and fighter2.hrt > 0:
                fighter2.health = min(fighter2.health + 20, 100)
            elif fighter2.hrt < 5 and fighter2.hrt > 0:
                fighter2.hrt += 1
            messages.append("+20 pts / +1 heart to both!")

        # Energy penalty
        if fighter1.eng <= 0 and energy_penalty_time1 >= 1.0 and fighter1.hrt > 0:
            energy_penalty_time1 = 0
            fighter1.health -= 10
            messages.append("P1: No energy! Losing health...")
            if fighter1.health <= 0:
                fighter1.hrt -= 1
                if fighter1.hrt > 0:
                    fighter1.health = 100
                else:
                    fighter1.health = 0

        if fighter2.eng <= 0 and energy_penalty_time2 >= 1.0 and fighter2.hrt > 0:
            energy_penalty_time2 = 0
            fighter2.health -= 10
            messages.append("P2: No energy! Losing health...")
            if fighter2.health <= 0:
                fighter2.hrt -= 20
                if fighter2.hrt > 0:
                    fighter2.health = 100
                else:
                    fighter2.health = 0

        fighter1.update(dt)
        fighter2.update(dt)
        clock.tick(60)

    return False

if __name__ == "__main__":
   while True:
       play_again = play_game()
       if not play_again:
           break