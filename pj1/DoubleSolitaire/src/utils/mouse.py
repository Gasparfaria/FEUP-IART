import pygame

def get_virtual_mouse_pos(base_width, base_height):
    """
    Converts actual mouse position to virtual resolution coordinates.
    """
    screen_width, screen_height = pygame.display.get_surface().get_size()
    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    real_mouse_x, real_mouse_y = pygame.mouse.get_pos()
    virtual_mouse_x = real_mouse_x / scale_x
    virtual_mouse_y = real_mouse_y / scale_y

    return virtual_mouse_x, virtual_mouse_y
