import pygame

from src.config import config_manager
from src.utils.assets import AssetManager
from src.utils.mouse import get_virtual_mouse_pos

class Dropdown:
    def __init__(
        self, x, y, width, items, normal_image_path, open_image_path, option,
        font, selected_index=0, scale_factor=2, selected_text_color=(255,215,0), normal_text_color=(255,255,255),
        visible_count=3, dropdown_offset=-7
    ):
        """
        x, y: Center position of the main dropdown button.
        width: The width of the dropdown list area.
        items: A list of option strings.
        normal_image_path: Path to the closed state image.
        open_image_path: Path to the open state image.
        font: A pygame.font.Font object to render text.
        scale_factor: Factor to scale the images.
        selected_text_color: Text color for the selected option.
        normal_text_color: Text color for the other options.
        visible_count: Number of items visible in the dropdown at once.
        dropdown_offset: Vertical offset to adjust dropdown list position relative to the main button.
        """
        self.font = font
        self.items = items
        self.selected_index = selected_index
        self.is_open = False
        self.option = option

        self.selected_text_color = selected_text_color
        self.normal_text_color = normal_text_color

        self.normal_image = AssetManager.load_image(normal_image_path).convert_alpha()
        self.open_image = AssetManager.load_image(open_image_path).convert_alpha()
        self.normal_image = self._scale_image(self.normal_image, scale_factor)
        self.open_image = self._scale_image(self.open_image, scale_factor)

        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect(center=(x, y))

        self._update_text_surface()

        self.width = width
        self.item_height = self.font.get_linesize() + 2  # + padding
        self.dropdown_offset = dropdown_offset
        self.visible_count = visible_count
        self.scroll_offset = 0  # Amount to scroll (in pixels).
        self._calculate_item_rects()

    def _scale_image(self, image, scale_factor):
        new_width = image.get_width() * scale_factor
        new_height = image.get_height() * scale_factor
        return pygame.transform.scale(image, (new_width, new_height))

    def _calculate_item_rects(self):
        """Generate a list of rects for each dropdown item, stacked vertically below the main button."""
        self.dropdown_rects = []
        x = self.rect.left
        y = self.rect.bottom + self.dropdown_offset
        for i in range(len(self.items)):
            rect = pygame.Rect(x +2, y + i * self.item_height, self.width, self.item_height)
            self.dropdown_rects.append(rect)

    def is_open(self):
        return self.is_open

    def _update_text_surface(self):
        """Render the main button text as just the selected option."""
        display_text = self.items[self.selected_index]
        self.text_surface = self.font.render(display_text, False, self.normal_text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def _toggle_open(self):
        """Toggle the open/closed state of the dropdown."""
        self.is_open = not self.is_open
        self.current_image = self.open_image if self.is_open else self.normal_image

    def handle_event(self, event):
        """
        Handle click and scroll events.
        - If the main button is clicked, toggle the dropdown.
        - If the dropdown is open and an item is clicked, update the selection and close the dropdown.
        - Handle mouse wheel events for scrolling.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = get_virtual_mouse_pos(480, 270)
            if self.rect.collidepoint(mouse_pos):
                self._toggle_open()
            elif self.is_open:
                for idx, rect in enumerate(self.dropdown_rects):
                    shifted_rect = rect.copy()
                    shifted_rect.y -= self.scroll_offset
                    if shifted_rect.collidepoint(mouse_pos):
                        self.selected_index = idx
                        self._change_config()
                        self._toggle_open()  # Close dropdown after selection.
                        self._update_text_surface()
                        break

        if event.type == pygame.MOUSEWHEEL and self.is_open:
            total_height = len(self.items) * self.item_height
            visible_height = self.visible_count * self.item_height
            max_scroll = max(0, total_height - visible_height)
            self.scroll_offset -= event.y * (self.item_height // 2)
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def _change_config(self):
        if self.option == "Resolution":
            res_str = self.items[self.selected_index]

            width_str, height_str = res_str.lower().split('x')
            res_width = int(width_str.strip())
            res_height = int(height_str.strip())

            config_manager.update_config("reswidth", res_width)
            config_manager.update_config("resheight", res_height)

            CONFIG_RELOAD = pygame.USEREVENT + 2
            pygame.event.post(pygame.event.Event(CONFIG_RELOAD))

        # Add functionality for Ai_Helper, just replace with 0,1,2 based on index +1
        elif self.option == "Ai_Helper":
            config_manager.update_config("Ai_Helper", self.selected_index + 1)


    def update(self):
        pass

    def draw(self, surface):
        """
        Draw the main dropdown button and, if open, the list of options with scrolling.
        The currently selected option in the list is rendered in a different text color.
        """
        surface.blit(self.current_image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

        if self.is_open:
            # Define a clipping region for visible items.
            visible_rect = pygame.Rect(self.rect.left, self.rect.bottom + self.dropdown_offset,
                                       self.width, self.visible_count * self.item_height)
            prev_clip = surface.get_clip()
            surface.set_clip(visible_rect)
            for idx, rect in enumerate(self.dropdown_rects):
                shifted_rect = rect.copy()
                shifted_rect.y -= self.scroll_offset
                # Render text; use a different color for the selected option.
                text_color = self.selected_text_color if idx == self.selected_index else self.normal_text_color
                item_text = self.font.render(self.items[idx], False, text_color)
                item_text_rect = item_text.get_rect(center=shifted_rect.center)
                surface.blit(item_text, item_text_rect)
            surface.set_clip(prev_clip)
