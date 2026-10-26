import pygame
import random
from pathlib import Path
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)
DIFFICULTIES = {
    "Easy": {"base_radius": 50, "min_radius": 18, "lifespan_frames": 120},
    "Medium": {"base_radius": 40, "min_radius": 12, "lifespan_frames": 90},
    "Hard": {"base_radius": 30, "min_radius": 8, "lifespan_frames": 60},
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.round_seconds = 30
        self.font = pygame.font.SysFont("Arial", 26)
        self.hit_sound = self._load_sound("hit.wav")
        self.miss_sound = self._load_sound("miss.wav")
        self.game_over_sound = self._load_sound("game_over.wav")
        self.reset_round("Medium")

    def _load_sound(self, filename):
        sound_path = Path(__file__).resolve().parent.parent / "assets" / filename
        try:
            return pygame.mixer.Sound(str(sound_path))
        except (pygame.error, OSError):
            return None

    def reset_round(self, difficulty):
        self.difficulty = difficulty
        self.time_left_frames = self.round_seconds * 60
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game_over = False
        self._game_over_logged = False
        self.target = self._spawn_target()

    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - self.margin)
        return Target(x, y, **DIFFICULTIES[self.difficulty])

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                difficulty_keys = {
                    pygame.K_1: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_3: "Hard",
                }
                difficulty = difficulty_keys.get(event.key)
                if difficulty is not None:
                    self.reset_round(difficulty)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            if self.hit_sound is not None:
                self.hit_sound.play()
            self.target = self._spawn_target()
        else:
            self.misses += 1
            if self.miss_sound is not None:
                self.miss_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            if self.game_over_sound is not None:
                self.game_over_sound.play()
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            if self.miss_sound is not None:
                self.miss_sound.play()
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            accuracy_text = self.font.render(
                f"Final Accuracy: {self.accuracy()}%", True, WHITE
            )
            easy_text = self.font.render("1 - Easy", True, WHITE)
            medium_text = self.font.render("2 - Medium", True, WHITE)
            hard_text = self.font.render("3 - Hard", True, WHITE)

            center_x = self.width // 2
            screen.blit(
                game_over_text,
                (center_x - game_over_text.get_width() // 2, 150),
            )
            screen.blit(
                score_text,
                (center_x - score_text.get_width() // 2, 210),
            )
            screen.blit(
                accuracy_text,
                (center_x - accuracy_text.get_width() // 2, 250),
            )
            screen.blit(easy_text, (center_x - easy_text.get_width() // 2, 310))
            screen.blit(medium_text, (center_x - medium_text.get_width() // 2, 345))
            screen.blit(hard_text, (center_x - hard_text.get_width() // 2, 380))

            if not getattr(self, "_game_over_logged", False):
                print(f"Time's up! Final score: {self.score}  Accuracy: {self.accuracy()}%")
                self._game_over_logged = True
            return

        r = int(self.target.visual_radius())
        pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
        pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))

