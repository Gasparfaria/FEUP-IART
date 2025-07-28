import pygame

from src.utils.assets import AssetManager

class Background:
    def __init__(self, bg_paths, animation_speed=3000, fade_duration=1000):
        """
        bg_paths: List of file paths for the background images.
        animation_speed: Time (in ms) between frame changes.
        fade_duration: Time (in ms) for the fade transition.
        """
        self.bg = [AssetManager.load_image(path).convert() for path in bg_paths]
        self.animation_speed = animation_speed
        self.fade_duration = fade_duration

        self.current_bg_frame = 0
        self.next_bg_frame = self.current_bg_frame
        self.last_update_time = pygame.time.get_ticks()
        self.in_transition = False
        self.transition_start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.in_transition:
            if current_time - self.last_update_time > self.animation_speed:
                self.next_bg_frame = (self.current_bg_frame + 1) % len(self.bg)
                self.transition_start_time = current_time
                self.in_transition = True
                self.last_update_time = current_time
        else:
            # If the transition is complete, finalize the new background.
            transition_progress = (current_time - self.transition_start_time) / self.fade_duration
            if transition_progress >= 1:
                self.current_bg_frame = self.next_bg_frame
                self.in_transition = False

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        if self.in_transition:
            transition_progress = (current_time - self.transition_start_time) / self.fade_duration
            if transition_progress > 1:
                transition_progress = 1
            surface.blit(self.bg[self.next_bg_frame], (0, 0))
            alpha_current = int(255 * (1 - transition_progress))
            current_image = self.bg[self.current_bg_frame].copy()
            current_image.set_alpha(alpha_current)
            surface.blit(current_image, (0, 0))
        else:
            surface.blit(self.bg[self.current_bg_frame], (0, 0))
