# gameplay_events.py
import pygame
from src.utils.mouse import get_virtual_mouse_pos

def handle_keydown(gameplay_screen, event):
    """
    Processes KEYDOWN events for the gameplay screen.
    Returns a command string if an action is triggered, or None.
    """
    if event.key == pygame.K_m:
        return "back_to_menu"
    elif event.key == pygame.K_ESCAPE:
        return "quit_game"
    return None

def human_handle_mouse_button_down(gameplay_screen, event):
    """
    Processes mouse button down events. This handles:
    - Double-click detection.
    - Initiating card dragging.
    """
    if event.button != 1:
        return

    mouse_pos = get_virtual_mouse_pos(gameplay_screen.base_width, gameplay_screen.base_height)
    current_time = pygame.time.get_ticks()

    if current_time - gameplay_screen.last_click_time < gameplay_screen.double_click_delay:
        gameplay_screen._handle_double_click(mouse_pos)
        gameplay_screen.last_click_time = 0
        return

    gameplay_screen.last_click_time = current_time

    # Iterate slots in reverse order so that top-most cards get priority.
    for slot in reversed(gameplay_screen.slots):
        if slot.cards:
            for card in reversed(slot.cards):
                if card.rect.collidepoint(mouse_pos):
                    gameplay_screen.selected_card = card
                    gameplay_screen.original_slot = slot
                    gameplay_screen.drag_offset = (mouse_pos[0] - card.rect.x,
                                                    mouse_pos[1] - card.rect.y)
                    gameplay_screen.selected_stack = slot.get_stack_from_card(card)
                    if not gameplay_screen.selected_stack:
                        _reset_selection(gameplay_screen)
                        break
                    for i, c in enumerate(gameplay_screen.selected_stack):
                        c.rect.topleft = (mouse_pos[0] - gameplay_screen.drag_offset[0],
                                          mouse_pos[1] - gameplay_screen.drag_offset[1] + i * slot.vertical_offset)
                    break
            if gameplay_screen.selected_card:
                break

def human_handle_mouse_motion(gameplay_screen, event):
    """
    Process mouse motion events for dragging cards.
    """
    if gameplay_screen.selected_card:
        mouse_pos = get_virtual_mouse_pos(gameplay_screen.base_width, gameplay_screen.base_height)
        for i, card in enumerate(gameplay_screen.selected_stack):
            card.rect.topleft = (mouse_pos[0] - gameplay_screen.drag_offset[0],
                                 mouse_pos[1] - gameplay_screen.drag_offset[1] + i * gameplay_screen.original_slot.vertical_offset)

def human_handle_mouse_button_up(gameplay_screen, event):
    """
    Processes mouse button up events to drop cards.
    """
    if event.button != 1 or not gameplay_screen.selected_card:
        return

    mouse_pos = get_virtual_mouse_pos(gameplay_screen.base_width, gameplay_screen.base_height)
    dropped = False

    for slot in gameplay_screen.slots + gameplay_screen.foundations:
        if slot.get_hitbox().collidepoint(mouse_pos):
            if slot.can_accept_card(gameplay_screen.selected_card):
                if slot.is_foundation and len(gameplay_screen.selected_stack) > 1:
                    continue
                if slot.drop_card(gameplay_screen.selected_card, gameplay_screen.original_slot):
                    dropped = True
                    break

    if not dropped and gameplay_screen.original_slot:
        gameplay_screen.original_slot.reposition_cards()

    _reset_selection(gameplay_screen)


def _reset_selection(gameplay_screen):
    """
    Reset the card selection and movement variables.
    """
    gameplay_screen.selected_card = None
    gameplay_screen.selected_stack = []
    gameplay_screen.original_slot = None