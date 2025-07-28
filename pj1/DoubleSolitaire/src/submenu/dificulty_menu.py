from operator import indexOf

import pygame

from src.ui.button import MenuButton
from src.utils.mouse import get_virtual_mouse_pos
from src.ui.selector import Selector
from src.utils.assets import AssetManager
from src.config import config_manager


class DifficultySelector:
    def __init__(self, x, y, width, height, font):
        """
        x, y: Top-left position of the difficulty selector.
        width, height: Dimensions of the area that holds the selector buttons.
        font: A pygame.font.Font object used to render text.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

        # Define difficulty options and their corresponding details.
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.details = {
            "Easy": {"time": "12:00", "stack_size": "Any", "stack_rules": "All Suits"},
            "Medium": {"time": "10:00", "stack_size": "Any", "stack_rules": "Alternating Colors"},
            "Hard": {"time": "08:00", "stack_size": "1", "stack_rules": "No Stacks"},
        }

        # List to hold difficulty buttons.
        self.buttons = []
        self.button_img_path = "assets/images/ui/SelectorButton.png"
        self.button_selected_img_path = "assets/images/ui/SelectorButtonPressed.png"

        button_x_offset = 121

        for i, difficulty in enumerate(self.difficulties):
            btn = MenuButton(
                x=self.rect.centerx - button_x_offset + (i * button_x_offset),
                y=self.rect.y + 24,
                text=difficulty,
                normal_image_path=self.button_img_path,
                font=self.font,
                scale_factor=2,
                y_offset=-2
            )
            btn.set_selected_image(self.button_selected_img_path, scale_factor=1)
            self.buttons.append(btn)

            # Create the hover selector instance.
            # Initially, place it at the center of the first button.
        init_center = self.buttons[0].rect.center if self.buttons else (x, y)
        self.selector = Selector(
            x=init_center[0],
            y=init_center[1],
            big_image_path="assets/images/ui/selector_0.png",
            medium_image_path="assets/images/ui/selector_1.png",
            small_image_path="assets/images/ui/selector_2.png",
            animation_speed=300,
            scale_factor=2
        )
        self.hovered_button = self.buttons[0]

    def handle_event(self,event):
        """
        Handles mouse events for hovering and clicking.
        When hovering over a button, updates the hovered difficulty to show details.
        """
        mouse_pos = get_virtual_mouse_pos(480, 270)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self._update_conf(self.hovered_button)
            curr_index = self.buttons.index(self.hovered_button)
            if event.key == pygame.K_LEFT:
                self.hovered_button = self.buttons[(curr_index -1 ) % len(self.buttons)]
            elif event.key == pygame.K_RIGHT:
                self.hovered_button = self.buttons[(curr_index +1 ) % len(self.buttons)]

        if event.type == pygame.MOUSEMOTION:
            for btn in self.buttons:
                if btn.rect.collidepoint(mouse_pos):
                    self.hovered_button = btn
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.rect.collidepoint(mouse_pos):
                    return self._update_conf(btn)
        return None

    def _update_conf(self, btn):
        config_manager.gameTimeLimit = int(self.details[btn.text]["time"].split(":")[0])
        config_manager.gameStackSize = 0 if self.details[btn.text]["stack_size"] == "Any" else int(
            self.details[btn.text]["stack_size"])
        config_manager.gameStackMovement = 0 if self.details[btn.text]["stack_rules"] == "All Suits" else 1
        return self._handle_press(btn)

    def _handle_press(self, btn):
        """
        Returns a string identifier based on the button pressed.
        """
        if btn.text in self.difficulties:
            print(btn.text.lower())
            return True
        return None

    def update(self):
        for btn in self.buttons:
            btn.update()

        if self.hovered_button:
            self.selector.update(new_center=self.hovered_button.rect.center)
        else:
            self.selector.update()  # No position update.

    def draw(self, surface):
        # Draw a background for the selector area.
        outer_color = pygame.Color("#321c00")
        middle_color = pygame.Color("#402810")
        inner_color = pygame.Color("#472f17")

        pygame.draw.rect(surface, outer_color, self.rect)

        middle_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4,
                                  self.rect.width - 8, self.rect.height - 8)
        pygame.draw.rect(surface, middle_color, middle_rect)

        # Draw inner layer: inset 4 more pixels (total 8 pixels from all sides).
        inner_rect = pygame.Rect(self.rect.x + 8, self.rect.y + 8,
                                 self.rect.width - 16, self.rect.height - 16)
        pygame.draw.rect(surface, inner_color, inner_rect)

        for btn in self.buttons:
            btn.draw(surface)

        self.selector.draw(surface)

        detail = self.details[self.hovered_button.text]

        # Prepare each line of text
        lines = [
            f"Time: {detail['time']}",
            f"Stack Size: {detail['stack_size']}",
            f"Stack Movement: {detail['stack_rules']}"
        ]

        # Starting y position (e.g., below the selector)
        start_y = self.rect.top + 45

        # Render each line and blit them one by one
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, False, (255, 255, 255))
            line_rect = line_surface.get_rect(centerx=self.rect.centerx, top=start_y + i * line_surface.get_height())
            surface.blit(line_surface, line_rect)