import pygame
import sys

from src.config import config_manager
from src.game import Game

def main():
    pygame.init()

    #Load the Icon and set it
    icon = pygame.image.load("assets/images/icons/IconScalled.png")
    pygame.display.set_icon(icon)

    # Define the virtual (base) resolution
    base_width, base_height = 480, 270
    # Create the actual window; starting with the base resolution and allowing resizing

    initial_window_width, initial_window_height = config_manager.gameResWidth, config_manager.gameResHeight

    screen = pygame.display.set_mode((initial_window_width, initial_window_height), pygame.RESIZABLE)
    fullscreen = config_manager.gameFullscreen
    if fullscreen:
        pygame.display.toggle_fullscreen() # Janky in linux

    pygame.display.set_caption("Double Solitaire")

    clock = pygame.time.Clock()

    # Create a base surface for rendering (the virtual resolution)
    base_surface = pygame.Surface((base_width, base_height))

    # Create your game instance (its render method should accept a surface)
    game = Game(base_surface)

    CONFIG_RELOAD = pygame.USEREVENT + 2

    # Variables for scaling and resizing
    last_window_size = screen.get_size()

    # Variables to control pausing during resizing
    resizing = False
    RESIZE_DONE = pygame.USEREVENT + 1  # Custom event for finishing resizing
    RESIZE_DELAY = 300  # milliseconds to wait after last resize event

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                # Update the window size when resizing occurs
                resizing = True
                # Restart the timer: if no VIDEORESIZE events occur for RESIZE_DELAY ms,
                # a RESIZE_DONE event will be fired.
                pygame.time.set_timer(RESIZE_DONE, RESIZE_DELAY)

            elif event.type == RESIZE_DONE:
                screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
                # The resize delay has passed, so resume normal game updates
                resizing = False
                pygame.time.set_timer(RESIZE_DONE, 0)  # Stop the timer


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
                    last_window_size = screen.get_size()

            elif event.type == CONFIG_RELOAD:
                print("Reload")
                new_window_width, new_window_height = config_manager.gameResWidth, config_manager.gameResHeight
                current_width, current_height = pygame.display.get_surface().get_size()
                if new_window_width != current_width or new_window_height != current_height:
                    screen = pygame.display.set_mode((new_window_width, new_window_height), pygame.RESIZABLE)
                    last_window_size = screen.get_size()

                new_fullscreen = config_manager.gameFullscreen
                if new_fullscreen != fullscreen:
                    if new_fullscreen:
                        print("Xpp")
                        pygame.display.toggle_fullscreen()
                fullscreen = new_fullscreen

                if hasattr(game, "reload_config"):
                    game.reload_config()

            # Pass events to the game instance for handling
            game.handle_event(event)

        # Only update game logic if we're not resizing
        if not resizing:
            game.update()

        # Clear the virtual (base) surface
        base_surface.fill((0, 0, 0))

        # Render game content or a "paused" message depending on whether we're resizing
        if not resizing:
            game.render(base_surface)
        else:
            # Display a pause message during resizing
            pause_font = pygame.font.Font(None, 36)
            pause_text = pause_font.render("Paused for Resizing...", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(base_width // 2, base_height // 2))
            base_surface.blit(pause_text, pause_rect)

        # Scale the virtual surface to the current window size
        current_size = screen.get_size()
        if current_size != last_window_size:
            scaled_surface = pygame.transform.scale(base_surface, current_size)
            last_window_size = current_size
        else:
            scaled_surface = pygame.transform.scale(base_surface, current_size)

        # Blit the scaled surface to the display and update the screen
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()



        # Maintain 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
