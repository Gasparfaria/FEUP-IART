import pygame

from src.screens.menu_screen import MenuScreen
from src.screens.gameplay_screen import GameplayScreen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 36)

        self.current_screen = MenuScreen()
        #self.current_screen = GameplayScreen()
        

    def handle_event(self, event):
        result = self.current_screen.handle_event(event)
        self._handle_screen_change(result)

    def update(self):
        result = self.current_screen.update()
        self._handle_screen_change(result)


    def _handle_screen_change(self, result):
        if result == "start_game":
            self.current_screen = GameplayScreen()
        elif result == "back_to_menu":
            self.current_screen = MenuScreen()
        elif result == "restart_game":
            self.current_screen = GameplayScreen()
        elif result == "quit_game":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def render(self,surface):
        self.current_screen.render(surface)


