import pygame

from src.utils.assets import AssetManager


class MenuButton:
    def __init__(self, x, y, text, normal_image_path, font, scale_factor=2, y_offset=-5):
        """
        x, y: Center position for the button.
        text: The button label.
        normal_image_path: Path to the normal state image (e.g., "assets/images/Button.png").
        hover_image_path: Path to the hover/selected state image (e.g., "assets/images/ButtonHover.png").
        font: A pygame.font.Font object for rendering the text.
        scale_factor: Integer factor to scale the button images.
        """
        # Load images
        self.normal_image = AssetManager.load_image(normal_image_path).convert_alpha()
        self.selected_image = None
        self.y_offset = y_offset

        self.normal_image = self.scale_image(self.normal_image, scale_factor)

        self.isSelected = False

        # Store font and text
        self.font = font
        self.text = text

        # Set the current image to normal by default and get its rect
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect(center=(x, y))

        # Render the text and center it on the button
        self.text_surface = self.font.render(self.text, False, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery + y_offset))

    def scale_image(self, image, scale_factor):
        # Scale images by the given integer factor (preserving the pixel art look)
        new_width = image.get_width() * scale_factor
        new_height = image.get_height() * scale_factor
        return pygame.transform.scale(image, (new_width, new_height))

    def set_selected_image(self, selected_image, scale_factor=2):
        self.selected_image = AssetManager.load_image(selected_image).convert_alpha()
        self.isSelected = False
        self.selected_image = self.scale_image(self.selected_image, scale_factor)

    def toggle_selected(self):
        self.isSelected = not self.isSelected
        if not self.isSelected:
            self.text_surface = self.font.render(self.text, False, (255, 255, 255))
        else:
            self.text_surface = self.font.render(self.text, False, (200, 200, 200))

    def change_color(self,color):
        self.text_surface = self.font.render(self.text, False, color)

    def get_is_selected(self):
        return self.isSelected

    def get_text(self):
        return self.text


    def update(self):

        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery - 5))
        if self.selected_image is not None:
            if self.isSelected:
                self.current_image = self.selected_image
                self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery -1))
            else:
                self.current_image = self.normal_image
        return None

    def draw(self, surface):
        """Draw the button image and the text on top."""
        surface.blit(self.current_image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

