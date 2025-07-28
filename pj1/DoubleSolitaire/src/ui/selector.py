import pygame

from src.utils.assets import AssetManager


class Selector:
    def __init__(self, x, y, big_image_path, medium_image_path, small_image_path, animation_speed=800, scale_factor=2):
        """
        x, y: Initial center position for the selector.
        big_image_path, medium_image_path, small_image_path: File paths for the three animation sprites.
        animation_speed: Milliseconds between frame changes.
        """
        # Load the three sprites
        # self.bg = [AssetManager.load_image(path).convert() for path in bg_paths]
        self.images = [
            AssetManager.load_image(big_image_path).convert_alpha(),
            AssetManager.load_image(medium_image_path).convert_alpha(),
            AssetManager.load_image(small_image_path).convert_alpha(),
            AssetManager.load_image(medium_image_path).convert_alpha()
        ]

        for i in range(len(self.images)):
            new_width = self.images[i].get_width() * scale_factor
            new_height = self.images[i].get_height() * scale_factor
            self.images[i] = pygame.transform.scale(self.images[i], (new_width, new_height))

        self.current_frame = 0
        self.animation_speed = animation_speed  # Time (ms) between frame changes
        self.last_update_time = pygame.time.get_ticks()

        self.rect = self.images[0].get_rect(center=(x, y))

    def update(self, new_center=None):
        """
        new_center: Optional tuple (x, y) to update the selector's position.
        This allows the selector to follow a button or any other element.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = current_time

        if new_center is not None:
            self.rect.center = new_center

    def draw(self, surface):
        image_rect = self.images[self.current_frame].get_rect(center=self.rect.center)
        image_rect.centery -= 1
        surface.blit(self.images[self.current_frame], image_rect)

