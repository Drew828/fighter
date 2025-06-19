import display

class Fighter:
    def __init__(self, x, y, facing_right=True, health=100, eng=100, 
                 offense=1, defense=1, pts=0, upg_tokens=3, hrt=3, color=(0,0,0)):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.health = health
        self.eng = eng
        self.offense = offense
        self.defense = defense
        self.pts = pts
        self.upg_tokens = upg_tokens
        self.hrt = hrt
        self.color = color
        self.current_pose = "idle"
        self.animation_timer = 0
        self.animation_duration = 0  # NEW: store duration for smooth animation

    def set_pose(self, pose):
        self.current_pose = pose
        durations = {
            "punch": 0.4,
            "kick": 0.5,
            "spin": 0.8,
            "block": 1,
            "idle": 0
        }
        self.animation_duration = durations.get(pose, 0)
        self.animation_timer = self.animation_duration

    def perform_action(self, action):
        if action == "left":
            self.x -= 5
            self.facing_right = False
        elif action == "right":
            self.x += 5
            self.facing_right = True
        elif action == "jump":
            if self.y >= display.RING_FLOOR_HEIGHT - 100:
                self.y -= 50
        elif action == "punch":
            self.set_pose("punch") 
        elif action == "kick":
            self.set_pose("kick")
        elif action == "block":
            self.set_pose("block")
        elif action == "spin":
            self.set_pose("spin")

    def update(self, dt):
        # Gravity for jump
        if self.y < display.RING_FLOOR_HEIGHT - 100:
            self.y += 300 * dt
            if self.y > display.RING_FLOOR_HEIGHT - 100:
                self.y = display.RING_FLOOR_HEIGHT - 100
        # Animation timer
        if self.animation_timer > 0:
            self.animation_timer -= dt
            if self.animation_timer <= 0:
                self.animation_timer = 0
                self.current_pose = "idle"
        # Clamp position
        self.x = max(50, min(self.x, 750))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.hrt -= 1
            if self.hrt > 0:
                self.health = 100
            else:
                self.health = 0
                self.hrt = 0

    def get_base_joints(self):
        direction = 1 if self.facing_right else -1
        joints = {
            "head": (self.x, self.y - 60),
            "body": (self.x, self.y - 30),
            "hand_l": (self.x - 25, self.y - 35),
            "hand_r": (self.x + 25, self.y - 35),
            "foot_l": (self.x - 15, self.y),
            "foot_r": (self.x + 15, self.y)
        }
        return joints

    def lerp(self, a, b, t):
        """Linear interpolation between points a and b by t (0..1)"""
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    def get_pose_joints(self):
        joints = self.get_base_joints()
        direction = 1 if self.facing_right else -1

        # Animation progress: 0=start, 1=end
        if self.animation_duration > 0:
            progress = 1 - max(self.animation_timer / self.animation_duration, 0)
        else:
            progress = 1

        # Smoothly interpolate from idle to attack pose
        if self.current_pose == "punch":
            punch_hand = "hand_r" if self.facing_right else "hand_l"
            idle_pos = joints[punch_hand]
            attack_pos = (self.x + (50 * direction), self.y - 30)
            joints[punch_hand] = self.lerp(idle_pos, attack_pos, progress)
        elif self.current_pose == "kick":
            kick_foot = "foot_r" if self.facing_right else "foot_l"
            idle_pos = joints[kick_foot]
            attack_pos = (self.x + (45 * direction), self.y - 10)
            joints[kick_foot] = self.lerp(idle_pos, attack_pos, progress)
        elif self.current_pose == "spin":
            # Both feet move out
            idle_r = joints["foot_r"]
            idle_l = joints["foot_l"]
            attack_r = (self.x + (45 * direction), self.y - 10)
            attack_l = (self.x - (45 * direction), self.y - 10)
            joints["foot_r"] = self.lerp(idle_r, attack_r, progress)
            joints["foot_l"] = self.lerp(idle_l, attack_l, progress)
        elif self.current_pose == "block":
            block_hand1 = "hand_r" if self.facing_right else "hand_l"
            block_hand2 = "hand_l" if self.facing_right else "hand_r"
            idle1 = joints[block_hand1]
            idle2 = joints[block_hand2]
            attack1 = (self.x + (25 * direction), self.y - 50)
            attack2 = (self.x + (20 * direction), self.y - 45)
            joints[block_hand1] = self.lerp(idle1, attack1, progress)
            joints[block_hand2] = self.lerp(idle2, attack2, progress)
        return joints

    def draw(self, surface):
        import pygame
        joints = self.get_pose_joints()
        # Draw body
        pygame.draw.line(surface, self.color, joints["head"], joints["body"], 4)
        pygame.draw.line(surface, self.color, joints["body"], joints["hand_l"], 4)
        pygame.draw.line(surface, self.color, joints["body"], joints["hand_r"], 4)
        pygame.draw.line(surface, self.color, joints["body"], joints["foot_l"], 4)
        pygame.draw.line(surface, self.color, joints["body"], joints["foot_r"], 4)
        # Draw head
        pygame.draw.circle(surface, self.color, (int(joints["head"][0]), int(joints["head"][1])), 12)