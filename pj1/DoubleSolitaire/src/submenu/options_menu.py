import pygame

from src.config import config_manager
from src.ui.dropdown import Dropdown
from src.ui.time_bar import TimeBar
from src.utils.assets import AssetManager
from src.ui.button import MenuButton
from src.utils.mouse import get_virtual_mouse_pos


class OptionsMenu:
    def __init__(self):
        self.bg_img = AssetManager.load_image('assets/options/OptionsSubMenu.png').convert_alpha()
        self.button_img_path = ('assets/options/Button.png')
        self.button_selected_img_path = ('assets/options/ButtonSelected.png')
        self.dropdown1_img = AssetManager.load_image('assets/options/Dropdown1.png').convert_alpha()
        self.dropdown2_img = AssetManager.load_image('assets/options/Dropdown2.png').convert_alpha()
        self.xbutton_img = AssetManager.load_image('assets/options/XButton.png').convert_alpha()

        self.number_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf",13)
        self.font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
        self.title_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 52)

        self.bg_rect = self.bg_img.get_rect(center=(480 // 2, 270 // 2))

        self.xbutton_rect = self.xbutton_img.get_rect(topright=(self.bg_rect.right - 29, self.bg_rect.top + 17))

        self.time_bar = TimeBar(
            x = self.bg_rect.centerx - 155,
            y = self.bg_rect.bottom -38,
            font = self.number_font,
            visible_count=11,
            spacing=6

        )
        self.time_bar.set_num_states(1) # Test

        self.title = self.title_font.render("Options",False,(255,255,255))

        self.title_rect = self.title.get_rect(topleft=(self.bg_rect.top +100, self.bg_rect.top + 18))


        self.buttons = []
        self._create_buttons()

        self.dropdowns = []
        self._create_dropdowns()

        self.state_number = -1

    def _create_buttons(self):
        bg_x, bg_y = self.bg_rect.center
        fullscreen_button = MenuButton(
            x = bg_x -82,
            y = bg_y + 14,
            text = 'Fullscreen',
            normal_image_path=self.button_img_path,
            font=self.font,
            scale_factor=1)
        fullscreen_button.set_selected_image(self.button_selected_img_path, scale_factor=1)
        if config_manager.gameFullscreen :
            fullscreen_button.toggle_selected()

        self.buttons.append(fullscreen_button)

        fast_mode = MenuButton(
            x = bg_x -82,
            y = bg_y + 58,
            text = 'Fast Mode',
            normal_image_path=self.button_img_path,
            font=self.font,
            scale_factor=1
        )
        fast_mode.set_selected_image(self.button_selected_img_path, scale_factor=1)

        if config_manager.gameFastMode:
            fast_mode.toggle_selected()

        self.buttons.append(fast_mode)

        glints = MenuButton(
            x = bg_x +82,
            y = bg_y + 14,
            text = 'Glints',
            normal_image_path=self.button_img_path,
            font=self.font,
            scale_factor=1
        )
        glints.set_selected_image(self.button_selected_img_path, scale_factor=1)

        if config_manager.gameGlints:
            glints.toggle_selected()

        self.buttons.append(glints)

        animation = MenuButton(
            x = bg_x + 82,
            y = bg_y + 58,
            text = 'No Anims',
            normal_image_path=self.button_img_path,
            font=self.font,
            scale_factor=1
        )
        animation.set_selected_image(self.button_selected_img_path, scale_factor=1)

        if config_manager.gameNoAnims:
            animation.toggle_selected()

        self.buttons.append(animation)

    def _create_dropdowns(self):
        bg_x, bg_y = self.bg_rect.center
        current_resolution = f'{config_manager.gameResWidth}x{config_manager.gameResHeight}'
        resolution_items = ["1920x1080", "1600x900", "1280x720","480x270"]
        resolution_dropdown = Dropdown(
            x=bg_x - 82,
            y=bg_y - 30,
            width=110,
            items= resolution_items,
            selected_index= resolution_items.index(current_resolution),
            option="Resolution",
            normal_image_path="assets/options/Dropdown1.png",
            open_image_path="assets/options/Dropdown2.png",
            font=self.font,
            scale_factor=1
        )
        current_ai = config_manager.gameAiHelper
        ai_items = ["Placehold1", "Placehold2", "Placehold3", "Placehold4", "Placehold5", "Placehold6", "Placehold7", "Placehold8", "Placehold9"]

        ai_dropdown = Dropdown(
            x=bg_x + 82,
            y=bg_y - 30,
            width=110,
            items= ai_items,
            selected_index= current_ai,
            option="Ai_Helper",
            normal_image_path="assets/options/Dropdown1.png",
            open_image_path="assets/options/Dropdown2.png",
            font=self.font,
            scale_factor=1
        )
        self.dropdowns.append(resolution_dropdown)
        self.dropdowns.append(ai_dropdown)

    def handle_event(self, event):
        """
        Handle events specific to the Options screen.
        Returns True if the options should be closed.
        """
        mouse_pos = get_virtual_mouse_pos(480, 270)
        for dd in self.dropdowns:
            hitbox = dd.rect
            if dd.is_open:
                extended_hitbox = pygame.Rect(dd.rect.x, dd.rect.y, dd.rect.width, dd.rect.height + 80)
                hitbox = extended_hitbox
            if hitbox.collidepoint(mouse_pos):
                dd.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.xbutton_rect.collidepoint(mouse_pos):
                return True, self.state_number
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                     self._change_but_config(button)
            if self.time_bar.rect.collidepoint(mouse_pos):
                self.state_number = self.time_bar.handle_event(event) # returns the number clicked



        return False, -1


    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self, surface):
        surface.blit(self.bg_img, self.bg_rect)

        surface.blit(self.xbutton_img, self.xbutton_rect)

        surface.blit(self.title, self.title_rect)

        for btn in self.buttons:
            btn.draw(surface)

        for dd in self.dropdowns:
            dd.draw(surface)

        self.time_bar.draw(surface)

    def _change_but_config(self, button):
        button.toggle_selected()
        new_state = button.get_is_selected()
        key = button.get_text()

        # Update configuration for this button.
        config_manager.update_config(key, new_state)

        if key.lower() == "fast mode" and new_state:
            for btn in self.buttons:
                if btn.get_text().lower() == "no anims" and btn.get_is_selected():
                    btn.toggle_selected()
                    config_manager.update_config(btn.get_text(), btn.get_is_selected())
                    break
        elif key.lower() == "no anims" and new_state:
            for btn in self.buttons:
                if btn.get_text().lower() == "fast mode" and btn.get_is_selected():
                    btn.toggle_selected()
                    config_manager.update_config(btn.get_text(), btn.get_is_selected())
                    break

        CONFIG_RELOAD = pygame.USEREVENT + 2
        pygame.event.post(pygame.event.Event(CONFIG_RELOAD))

    def set_num_states(self, num):
        self.time_bar.set_num_states(num)

