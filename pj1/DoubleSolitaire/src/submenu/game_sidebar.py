import pygame
from src.ui.button import MenuButton
from src.utils.assets import AssetManager
from src.utils.mouse import get_virtual_mouse_pos


class Sidebar:
    def __init__(self, x, y, width, height, font):
        """
        x, y: Top-left position of the sidebar.
        width, height: Dimensions of the sidebar.
        font: A pygame.font.Font object used to render text.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

        # Info fields
        self.time_left = "00:00"
        self.score = "0"
        self.moves_left = "0"

        self.buttons = []
        self.button_img_path = "assets/options/Button.png"
        self.button_selected_img_path = "assets/options/ButtonSelected.png"

        button_texts = ["Main Menu", "Undo", "Options", "Hint", "Save", "Print heuristics"]

        for text in button_texts:
            btn = MenuButton(
                x=self.rect.centerx,
                y=self.rect.bottom + len(self.buttons) * -26 - 16,
                text=text,
                normal_image_path=self.button_img_path,
                font=self.font,
                scale_factor=0.5,
                y_offset=-2
            )
            btn.set_selected_image(self.button_selected_img_path, scale_factor=1)
            self.buttons.append(btn)

    def set_time_left(self, time_str):
        self.time_left = time_str

    def set_moves_left(self, moves_str):
        self.moves_left = moves_str

    def set_score(self, score):
        self.score = score

    def handle_event(self, event):
        """
        Handle events for the sidebar.
        This delegates event handling to each button.
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = get_virtual_mouse_pos(480, 270)
            if self.rect.collidepoint(mouse_pos):
                for btn in self.buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        return self._handle_press(btn)
        return None

    def _handle_press(self, btn):
        if btn.text == "Main Menu":
            return "back_to_menu"
        elif btn.text == "Go Back":
            return "go_back"
        elif btn.text == "Options":
            return "options"
        elif btn.text == "Undo":
            return "undo"
        elif btn.text == "Hint":
            return "hint"
        elif btn.text == "Save":
            return "save"
        

    def update(self):
        for btn in self.buttons:
            btn.update()

    def draw(self, surface):
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


        # Render info texts and center them horizontally.
        time_text = self.font.render("Time Left", False, (255, 255, 255))
        time_text_rect = time_text.get_rect(centerx=self.rect.centerx, top=self.rect.y + 10)
        time_value = self.font.render(str(self.time_left), False, (255, 255, 255))
        time_value_rect = time_value.get_rect(centerx=self.rect.centerx, top=time_text_rect.bottom + 5)

        score_text = self.font.render("Score", False, (255, 255, 255))
        score_text_rect = score_text.get_rect(centerx=self.rect.centerx, top=time_value_rect.bottom + 10)
        score_value = self.font.render(str(self.score), False, (255, 255, 255))
        score_value_rect = score_value.get_rect(centerx=self.rect.centerx, top=score_text_rect.bottom + 5)

        surface.blit(time_text, time_text_rect)
        surface.blit(time_value, time_value_rect)
        surface.blit(score_text, score_text_rect)
        surface.blit(score_value, score_value_rect)

        for btn in self.buttons:
            btn.draw(surface)
