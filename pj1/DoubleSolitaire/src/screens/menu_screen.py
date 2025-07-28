from optparse import Option
from src.ai.algorithms import UniformCostSearch as ucs
from src.screens.gameplay_screen import GameplayScreen

import pygame

from src.config import config_manager
import src.config as config
from src.screens.base_screen import Screen
from src.submenu.dificulty_menu import DifficultySelector
from src.submenu.options_menu import OptionsMenu
from src.ui.button import MenuButton
from src.ui.selector import Selector
from src.ui.background import Background
from src.animations.object_move import ObjectMove
from src.utils.assets import AssetManager
from src.utils.mouse import get_virtual_mouse_pos


class MenuScreen(Screen):
    def __init__(self):
        self.load_game = config_manager.gameLoadGame
        bg_paths = [
            "assets/images/backgrounds/MMBackgroundAn0.png",
            "assets/images/backgrounds/MMBackgroundAn1.png",
            "assets/images/backgrounds/MMBackgroundAn0.png",
            "assets/images/backgrounds/MMBackgroundAn2.png"
        ]
        self.background = Background(bg_paths, animation_speed=3000, fade_duration=1000)

        self.icon = AssetManager.load_image("assets/images/icons/IconLarge.png")
        self.font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
        self.title_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 52)

        self.state = "waiting"
        self.next_scene = None

        # List of buttons and which one is selected
        self.buttons = []
        self.new_buttons = []
        self.selected_button = 0
        self.button_move_anims = []
        self.start_y = 160
        self.spacing = 45
        self.buttons_anim_speed = 300
        labels = ["PLAY", "OPTIONS", "LOAD GAME", "QUIT"]

        # Create each button
        for i, label in enumerate(labels):
            x_pos, y_pos = self._get_button_start(i, len(labels))
            button = MenuButton(
                x=x_pos,
                y=y_pos,
                text=label,
                normal_image_path="assets/images/ui/SelectorButton.png",
                font=self.font
            )
            self.buttons.append(button)

        self.buttons[2].set_selected_image("assets/images/ui/SelectorButtonPressed.png")

        if self.load_game:(
            self.buttons[2].toggle_selected())

        self.selector = Selector(
            x=self.buttons[self.selected_button].rect.centerx,
            y=self.buttons[self.selected_button].rect.centery,
            big_image_path="assets/images/ui/selector_0.png",
            medium_image_path="assets/images/ui/selector_1.png",
            small_image_path="assets/images/ui/selector_2.png",
            animation_speed=200  # milliseconds between frame changes
        )

        self.options = OptionsMenu()

        # Magic numbers xpp
        self.difficulty_selector = DifficultySelector(x = 55, y = 67, width=370, height=135, font=self.font)


    def handle_event(self, event):
        """
        Event handler

        if "changing_scene", "changing_options" does nothing

        updates selected button

        :param event: The event to be handled
        """
        if self.state == "options":
            should_close, _ = self.options.handle_event(event)
            if should_close:
                self.state = "menu"
            return

        if self.state in ["changing_scene","changing_options"]:
            return None
        if self.state == "waiting":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "menu"
                self._animate_buttons_in(self.buttons)
            return None

        button_list = self.buttons if self.state == "menu" else self.new_buttons

        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(button_list, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                self._handle_mouse_click(button_list, event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._handle_return_event(event)
            if self.state == "difficulty_selection":
                self.difficulty_selector.handle_event(event)
            if event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 2) % len(button_list)
            elif event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 2) % len(button_list)
            elif event.key == pygame.K_LEFT:
                self.selected_button = (self.selected_button - 1) % len(button_list)
            elif event.key == pygame.K_RIGHT:
                self.selected_button = (self.selected_button + 1) % len(button_list)
        return None


    def _handle_return_event(self, event):
        """
        Handles the return event

        Depending on state it does different actions
        Creates animations and changes states
        """
        if self.state == "menu":
            if self.selected_button == 0:
                self.state = "changing_options"
                self._animate_buttons_out(self.buttons)
            elif self.selected_button == 1:
                self.state = "options"
                self.options.set_num_states(0)
            elif self.selected_button == 2:
                self._toggle_load_game()
            elif self.selected_button == 3:
                self.state = "changing_scene"
                self.next_scene = "quit_game"
                self._animate_buttons_out(self.buttons)

        elif self.state == "game_options":
            if self.selected_button == len(self.new_buttons) - 1:
                self._animate_buttons_out(self.new_buttons)
                self.state = "returning_to_menu"
            else:
                self._animate_buttons_out(self.new_buttons)
                config_manager.gamePlayerType = self.selected_button
                self.state = "difficulty_selection"
        elif self.state == "difficulty_selection":
            if self.difficulty_selector.handle_event(event):
                print("xpp")
                self.state = "changing_scene"
                self.next_scene = "start_game"

    def _handle_mouse_motion(self, button_list, event):
        """
        Function to update the selected button

        Gives the user visual feedback as if selecting with the arrow keys
        :param button_list: The current list of buttons
        :return:
        """
        mouse_pos = get_virtual_mouse_pos(480, 270)
        if self.state == "difficulty_selection":
            self.difficulty_selector.handle_event(event)
            return
        for i, button in enumerate(button_list):
            if button.rect.collidepoint(mouse_pos):
                self.selected_button = i
                break

    def _handle_mouse_click(self, button_list, event):
        """
        Function to simulate a return input when m1 is clicked.
        :param button_list: The current button list
        :return:
        """
        if self.state == "difficulty_selection":
            if self.difficulty_selector.handle_event(event):
                self.state = "changing_scene"
                self.next_scene = "start_game"

        mouse_pos = get_virtual_mouse_pos(480, 270)
        for i, button in enumerate(button_list):
            if button.rect.collidepoint(mouse_pos):
                self.selected_button = i  # Ensure sync with keyboard selection
                self._handle_return_event(event)  # Activate button action
                break

    def update(self):
        """
        Updates the screen

        Function that handles every animation.
        Also creates the new buttons once you click play and depending on state might animate buttons into the screen
        """

        self.background.update()
        if self.state == "options":
            self.options.update()
            return
        if self.state == "difficulty_selection":
            self.difficulty_selector.update()

        if self.state in ["changing_scene", "changing_options", "returning_to_menu"]:
            if not self.button_move_anims:
                if self.state == "changing_options":
                    self._create_game_options_buttons()
                    self.state = "game_options"
                elif self.state == "returning_to_menu":
                    self.state = "menu"
                    self.selected_button = 0
                    self._animate_buttons_in(self.buttons)
                else:
                    return self.next_scene

        for anim in self.button_move_anims:
            if anim.active:
                anim.update()
            else:
               self.button_move_anims.remove(anim)

        ## Update text on buttons
        button_to_update = self.buttons if self.state in ["menu","changing_options", "changing_scene"] else self.new_buttons

        for i, button in enumerate(button_to_update):
            button.update()


        self.selector.update(new_center=button_to_update[self.selected_button].rect.center) if button_to_update else None


    def _create_game_options_buttons(self):
        """Creates new buttons for game mode selection."""
        self.new_buttons = []
        self.button_move_anims = []
        labels = ["Human", "Breath FS", "Depth FS", "Uniformed CS", "Placeholder", "Back"]

        for i, label in enumerate(labels):
            x_pos, y_pos = self._get_button_start(i, len(labels))

            start_y = 270 + 20 * i

            button = MenuButton(
                x=x_pos,
                y=start_y,
                text=label,
                normal_image_path="assets/images/ui/SelectorButton.png",
                font=self.font
            )
            self.new_buttons.append(button)
        self._animate_buttons_in(self.new_buttons)

    def _get_button_start(self, button_num, totalnum):
        """
        Calculate the starting position (x, y) for a button.
        """
        screen_width = 480
        middle = screen_width // 2

        if totalnum < 4:
            # Single column layout: center the button
            x_pos = middle
            row = button_num
        else:
            row = button_num // 2
            if button_num % 2 == 0:
                x_pos = middle - 70
            else:
                x_pos = middle + 70

        y_pos = self.start_y + row * self.spacing
        return x_pos, y_pos

    def render(self, screen):
        self.background.draw(screen)


        icon_rect = self.icon.get_rect()
        icon_rect.center = (int(screen.get_width() * 0.5), int(screen.get_height() * 0.45))
        screen.blit(self.icon, icon_rect)

        title_surface = self.title_font.render("Double Solitaire", False, (255, 255, 255))
        title_rect = title_surface.get_rect(midtop=(screen.get_width() // 2, 10))
        screen.blit(title_surface, title_rect)

        if self.state == "options":
            self.options.draw(screen)
            return



        if self.state == "waiting":
            prompt_surface = self.font.render("Press any key to continue", False, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - screen.get_height() // 9))
            screen.blit(prompt_surface, prompt_rect)

        buttons_to_draw = self.buttons if self.state in ["menu", "changing_options", "changing_scene"] else self.new_buttons
        if self.state == "changing_scene":
            buttons_to_draw += self.new_buttons

        for button in buttons_to_draw:
            button.draw(screen)
        self.selector.draw(screen) if buttons_to_draw else None

        if self.state == "difficulty_selection":
            self.difficulty_selector.draw(screen)

    def _animate_buttons_out(self, buttons):
        """
        Function to give an animations to buttons to exit the screen
        :param buttons: The current list of buttons
        """
        self.button_move_anims = []
        for i, button in enumerate(buttons):
            target_y = 285 + (i * self.spacing) + 20
            move_anim = ObjectMove(
                anim_obj=button,
                start_pos=(button.rect.centerx, button.rect.centery),
                target_pos=(button.rect.centerx, target_y),
                duration=self.buttons_anim_speed,
                top_left=False
            )
            self.button_move_anims.append(move_anim)

    def _animate_buttons_in(self, buttons):
        """
        Function to give an animations to buttons to entering the screen
        :param buttons: The current list of buttons
        """
        self.button_move_anims = []
        for i, button in enumerate(buttons):
            target_x, target_y = self._get_button_start(i, len(buttons))
            button.rect.y = 285 + (i * self.spacing) + 20  # Start off-screen
            move_anim = ObjectMove(
                anim_obj=button,
                start_pos=(button.rect.centerx, button.rect.centery),
                target_pos=(target_x, target_y),
                duration=self.buttons_anim_speed,
                top_left=False
            )
            self.button_move_anims.append(move_anim)


    def _toggle_load_game(self):
        self.buttons[2].toggle_selected()
        self.load_game = not self.load_game
        config_manager.update_config("LoadGame", self.load_game)

