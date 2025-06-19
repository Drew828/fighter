import pygame

WINDOW_SIZE = (800, 600)
RING_FLOOR_HEIGHT = 450

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (20, 30, 255)
BROWN = (139, 69, 19)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (0, 0, 225)

def draw_heart(surface, x, y, size):
    color = (220, 40, 70)
    pygame.draw.circle(surface, color, (x + size//3, y + size//3), size//3)
    pygame.draw.circle(surface, color, (x + 2*size//3, y + size//3), size//3)
    points = [
        (x + size//6, y + size//3),
        (x + size//2, y + size),
        (x + 5*size//6, y + size//3)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_bolt(surface, x, y, size):
    color = (255, 215, 0)
    points = [
        (x + size//2, y),
        (x + size//3, y + size//2),
        (x + 2*size//3, y + size//2),
        (x, y + size),
        (x + size//2, y + size//2),
        (x + size//3, y + size//2)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_icon_bar(surface, x, y, width, height, color, border_color):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=12)
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2, border_radius=12)

def draw_ui(screen, font, fighter1, fighter2, messages):
    # Soft blue gradient background
    for i in range(WINDOW_SIZE[1]):
        color = (
            180 - i//8,
            210 - i//12,
            255 - i//6
        )
        pygame.draw.line(screen, color, (0, i), (WINDOW_SIZE[0], i))

    # Ring
    ring_rect = pygame.Rect(0, RING_FLOOR_HEIGHT, WINDOW_SIZE[0], WINDOW_SIZE[1] - RING_FLOOR_HEIGHT)
    pygame.draw.rect(screen, (230, 230, 245), ring_rect)
    pygame.draw.rect(screen, (180, 180, 210), ring_rect, 4)
    pygame.draw.line(screen, WHITE, (0, RING_FLOOR_HEIGHT), (WINDOW_SIZE[0], RING_FLOOR_HEIGHT), 4)

    # Fighter 1 stats (left)
    stats1 = f"P1  PTS: {fighter1.pts}  TOKENS: {fighter1.upg_tokens}"
    screen.blit(font.render(stats1, True, (60, 0, 0)), (10, 10))

    # Fighter 2 stats (right)
    stats2 = f"P2  PTS: {fighter2.pts}  TOKENS: {fighter2.upg_tokens}"
    screen.blit(font.render(stats2, True, (0, 0, 60)), (WINDOW_SIZE[0] - 320, 10))

    # --- Health Bar Backgrounds ---
    bar_w, bar_h = 170, 36
    # P1 health bar
    draw_icon_bar(screen, 6, 36, bar_w, bar_h, (255, 240, 240), (200, 60, 60))
    # P2 health bar
    draw_icon_bar(screen, WINDOW_SIZE[0] - bar_w - 6, 36, bar_w, bar_h, (255, 240, 240), (60, 60, 200))
    # --- Energy Bar Backgrounds ---
    bar_w_e, bar_h_e = 170, 30
    # P1 energy bar
    draw_icon_bar(screen, 6, 78, bar_w_e, bar_h_e, (255, 255, 230), (200, 180, 60))
    # P2 energy bar
    draw_icon_bar(screen, WINDOW_SIZE[0] - bar_w_e - 6, 78, bar_w_e, bar_h_e, (255, 255, 230), (200, 180, 60))

    # Hearts for health (max 5)
    for i in range(fighter1.hrt):
        draw_heart(screen, 14 + i*32, 40, 28)
    for i in range(fighter2.hrt):
        draw_heart(screen, WINDOW_SIZE[0] - 162 + i*32, 40, 28)

    # Lightning bolts for energy (max 5)
    bolts1 = int(fighter1.eng // 20)
    for i in range(bolts1):
        draw_bolt(screen, 14 + i*32, 82, 24)
    bolts2 = int(fighter2.eng // 20)
    for i in range(bolts2):
        draw_bolt(screen, WINDOW_SIZE[0] - 162 + i*32, 82, 24)

    # Messages
    y_offset = 120
    for msg in messages[-7:]:
        screen.blit(font.render(msg, True, BLACK), (10, y_offset))
        y_offset += 22

    # Draw fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    # Help text
    help_text = [
        "P1: A/D=Move, W=Jump, F=Punch, G=Kick, H=Spin, R=Block, 1/2/3=Upgrades",
        "P2: Left/Right=Move, Up=Jump, K=Kick, L=Spin, ;=Block, Space=Punch, 8/9/0=Upgrades"
    ]
    y_help = 260
    for line in help_text:
        screen.blit(font.render(line, True, BLACK), (10, y_help))
        y_help += 20

    # New Game button
    button_rect = pygame.Rect(650, 10, 130, 40)
    pygame.draw.rect(screen, (120, 180, 255), button_rect, border_radius=12)
    pygame.draw.rect(screen, (60, 100, 180), button_rect, 2, border_radius=12)
    text = font.render("New Game", True, WHITE)
    screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

    pygame.display.flip()
    return button_rect