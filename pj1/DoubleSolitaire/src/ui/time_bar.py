import pygame
from src.utils.assets import AssetManager
from src.utils.mouse import get_virtual_mouse_pos


class TimeBar:
    def __init__(self, x, y, font, visible_count=11, spacing=5):
        """
        x, y: Top-left position for the time bar.
        visible_count: Maximum number of states to display at once.
        spacing: Space between state images.
        font: Font for the Numbers.
        """
        self.x = x
        self.y = y
        self.visible_count = visible_count
        self.spacing = spacing
        self.font = font

        self.text_color = (255, 255, 255)

        self.timebar_img = AssetManager.load_image('assets/options/TimeBar.png').convert_alpha()
        self.state_img = AssetManager.load_image('assets/options/State.png').convert_alpha()
        self.selected_state_img = AssetManager.load_image('assets/options/SelectedState.png').convert_alpha()

        self.rect = self.timebar_img.get_rect(topleft=(x, y))
        self.state_rect = self.state_img.get_rect()
        self.state_width = self.state_rect.width
        self.state_height = self.state_rect.height

        # Instead of a list of states, we now track the total count.
        self.num_states = 0
        self.selected_index = 0
        self.scroll_offset = 0

    def set_num_states(self, num_states):
        """
        Sets the number of states.
        The states are assumed to be consecutive numbers starting from 1.
        The last state is selected by default.
        """
        self.num_states = num_states
        if num_states:
            self.selected_index = num_states - 1
        else:
            self.selected_index = 0
        self.scroll_offset = 0

    def set_selected_state(self, index):
        """
        Set the selected state index.
        """
        if 0 <= index < self.num_states:
            self.selected_index = index

    def get_selected_state(self):
        """
        Return the currently selected state (as its number, starting from 1).
        """
        if self.num_states:
            return self.selected_index + 1
        return None

    def handle_event(self, event):
        """
        Handle mouse click events.
        If the user clicks inside the visible area of the time bar,
        determine which state was clicked and update the selection accordingly.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = get_virtual_mouse_pos(480, 270)
            hitbox_x = self.x + 16
            hitbox_y = self.y - 4
            hitbox_width = self.visible_count * (self.state_width + self.spacing) - self.spacing
            hitbox_height = self.state_height
            visible_area = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

            if visible_area.collidepoint(mouse_pos):
                relative_x = mouse_pos[0] - hitbox_x
                clicked_index_within_window = int(relative_x // (self.state_width + self.spacing))

                total_states = self.num_states
                if total_states <= self.visible_count:
                    window_start = 0
                else:
                    window_start = self.selected_index - self.visible_count // 2
                    if window_start < 0:
                        window_start = 0
                    if window_start > total_states - self.visible_count:
                        window_start = total_states - self.visible_count

                actual_index = window_start + clicked_index_within_window
                if actual_index < total_states:
                    self.selected_index = actual_index
                    return actual_index
        return -1

    def draw(self, surface):
        """
        Draw the time bar.
        Up to visible_count states are drawn.
        The selected state is drawn with the selected_state_img.
        The view is adjusted so that the selected state is centered if possible,
        or shifted to the left if there aren’t enough states.
        """
        total_states = self.num_states
        if total_states == 0:
            return

        if total_states <= self.visible_count:
            window_start = 0
        else:
            window_start = self.selected_index - self.visible_count // 2
            if window_start < 0:
                window_start = 0
            if window_start > total_states - self.visible_count:
                window_start = total_states - self.visible_count

        surface.blit(self.timebar_img, self.rect)

        for i in range(self.visible_count):
            state_index = window_start + i
            if state_index >= total_states:
                break
            rect_x = self.x + 16 + i * (self.state_width + self.spacing)
            rect_y = self.y - 4
            dest_rect = pygame.Rect(rect_x, rect_y, self.state_width, self.state_height)

            asset = self.selected_state_img if state_index == self.selected_index else self.state_img
            surface.blit(asset, dest_rect)

            # The number text is now the state number (1-indexed)
            number_text = str(state_index + 1)
            text_surf = self.font.render(number_text, False, self.text_color)
            text_rect = text_surf.get_rect(center=dest_rect.center)
            surface.blit(text_surf, text_rect)
