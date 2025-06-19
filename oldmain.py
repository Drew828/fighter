import pygame
import sys
from fighter import Fighter
import movement
import display
import time

class Game:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Taekwondo Fighting Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.fighter = Fighter(400, 300)
        self.messages = []
        self.font = pygame.font.SysFont(None, 24)
        self.last_time = time.time()
        self.accum_time = 0
        self.energy_penalty_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Handle button clicks here if needed
                    pass

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: movement.punc(self.fighter, self.messages)
        if keys[pygame.K_k]: movement.kic(self.fighter, self.messages)
        if keys[pygame.K_s]: movement.spk(self.fighter, self.messages)
        if keys[pygame.K_b]: movement.blk(self.fighter, self.messages)
        if keys[pygame.K_1]: movement.upgrade(self.fighter, self.messages, "offense")
        if keys[pygame.K_2]: movement.upgrade(self.fighter, self.messages, "defense")
        if keys[pygame.K_3]: movement.upgrade(self.fighter, self.messages, "health")

    def update(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()
        self.accum_time += dt
        self.energy_penalty_time += dt

        # Regenerate energy
        if self.fighter.eng < 100:
            self.fighter.eng = min(self.fighter.eng + 10 * dt, 100)

        # Passive points and health
        if self.accum_time >= 5.0:
            self.accum_time -= 5.0
            self.fighter.pts += 20
            if self.fighter.health < 100:
                self.fighter.health = min(self.fighter.health + 20, 100)
            elif self.fighter.hrt < 5:
                self.fighter.hrt += 1
            self.messages.append("+20 pts / +1 heart!")

        # Energy penalty
        if self.fighter.eng <= 0 and self.energy_penalty_time >= 1.0:
            self.energy_penalty_time = 0
            self.fighter.health -= 10
            self.messages.append("No energy! Losing health...")
            if self.fighter.health <= 0:
                self.fighter.hrt -= 1
                self.fighter.health = 100

        self.fighter.update(dt)

    def render(self):
        display.draw_ui(self.window, self.font, self.fighter, self.messages)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS

def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

    pygame.quit()
sys.exit()