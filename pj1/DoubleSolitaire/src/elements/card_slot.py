import pygame

from src.utils.card_order import is_next_rank, is_prev_rank, is_prev_dif_colour


class CardSlot:
    """
    Represents a card slot in the game

    Manages position and rendering
    """
    def __init__(self, position, vertical_offset=25, is_foundation=False, bg_sprite=None, mv_rules=0, sk_size=0):
        """
        Initializes a new cardSlot object
        :param position: Position of the slot
        :param vertical_offset: Offset of each card vertically
        :param is_foundation: True if the card is foundation (offset = 0)
        :param bg_sprite: Background sprite optional
        """
        self.position = position  # Top-left position on the screen
        self.cards = []           # List of Card instances
        self.vertical_offset = vertical_offset
        self.is_foundation = is_foundation
        self.background = bg_sprite
        self.mv_rules = mv_rules
        self.sk_size = 100 if sk_size == 0 else sk_size

    def __lt__(self, other):
        return len(self.cards) < len(other.cards) 

    def push_king_to_top(self):

        kings = [card for card in self.cards if card.rank == 'King']
        non_kings = [card for card in self.cards if card.rank != 'King']

        self.cards = kings + non_kings

        self.reposition_cards()

    def update(self):
        """
        No use right now, might have some animations in the future
        """
        for card in self.cards:
            card.update()

    def add_card(self, card, to_animate=False):
        """
        Adds a card to the cardSlot object and recalculates positions

        If an animation is to be played then, to_animate is set to True, since the repositioning
        should only be made after the animation is played.

        :param to_animate: Boolean
        :param card: The card to add
        """
        self.cards.append(card)
        if not to_animate:
            self.reposition_cards()

    def reposition_cards(self):
        """
        Recalculates positions of each card.

        If the card number reaches a first threshold, the offset starts decreasing, if the second threshold is reached
        the offset decrease for each card is reduced since its multiplicative.
        """
        x, y = self.position
        length = len(self.cards)
        scale_factor = max(length - 5,1)

        for i, card in enumerate(self.cards):
            new_offset = 0
            if not self.is_foundation:
                new_offset = -1 * scale_factor

                if scale_factor > 4:
                    new_offset = -1 * 4
                    new_offset += int(-0.5 * (scale_factor - 4))
            card.rect.topleft = (x, y + i * (self.vertical_offset + new_offset))

    def remove_card(self):
        """
        Removes a card from the cardSlot object.
        :return:  The removed card if available, None otherwise
        """
        if self.cards:
            return self.cards.pop()
        return None

    def top_card(self):
        """
        Returns the top card of the cardSlot object.
        :return:  the top card if available, None otherwise
        """
        return self.cards[-1] if self.cards else None

    def draw_background(self, surface):
        """
        Draw the slot's background.
        """
        if self.background:
            x, y = self.position
            surface.blit(self.background, (x - 1, y - 1))

    def draw_cards(self, surface):
        """
        Draw  the slot's cards.
        """
        for card in self.cards:
            surface.blit(card.image, card.rect.topleft)

    def get_stack_from_card(self, card, max_stack=0):
        """
        Retrieves a valid stack of cards from the cardSlot object.

        Checks if the supposed stack size is below the max stack and then starts at the selected card and goes until it
        reaches the bottom. If the cards are each 1 rank apart (descending order), then its valid.

        :param card: The starting card
        :return: List of cards forming a stack, or empty list if it's not a valid stack exists
        """
        if card not in self.cards:
            return []

        if max_stack == 0:
            max_stack = self.sk_size

        index = self.cards.index(card)
        stack = self.cards[index:]
        stack = stack[:max_stack]  # Limit max length



        if index + max_stack < len(self.cards):
            return []

        for i in range(len(stack) - 1):
            if not is_prev_rank(stack[i].rank, stack[i + 1].rank):
                return []
            if self.mv_rules == 1:
                if not is_prev_dif_colour(stack[i].suit, stack[i + 1].suit):
                    return []

        return stack

    def get_hitbox(self):
        """
        Compute and return the hitbox of the cardSlot object

        The hitbox is calculated by the dimensions of the card Object + the number of cards * offset
        :return: Rectangle of the hitbox
        """
        if len(self.cards) > 0:
            card_width = self.cards[0].image.get_width()
            card_height = self.cards[0].image.get_height()
        else:
            card_width = 48
            card_height = 64

        if self.cards:
            height = card_height + (len(self.cards) - 1) * self.vertical_offset
        else:
            height = card_height  # Default height for empty slot

        return pygame.Rect(self.position[0], self.position[1], card_width, height)

    def can_accept_card(self, card):
        """
        Determines if the card can be accepted by the cardSlot object

        If foundation:
            - Only accepts Aces if empty
            - If not empty, they must have the same suit and be the next rank of the top card
        If slot (not foundation):
            - The slot can't be empty and the card must be the previous rank of the top card

        :param card: The card
        :return: True if the card can be accepted, False otherwise
        """
        if self.is_foundation:
            if len(self.cards) == 0:
                return card.rank == 'Ace'
            elif card.suit != self.top_card().suit:
                return False
            else:
                return is_next_rank(self.top_card().rank, card.rank)

        elif not self.cards:
            return False
        else:
            return is_prev_rank(self.top_card().rank, card.rank)

    def check_if_can_drop(self, card, from_slot):
        moving_stack = from_slot.get_stack_from_card(card, max_stack=len(from_slot.cards))
        if not moving_stack:
            return None
        if not self.can_accept_card(card):
            return None
        if self.is_foundation and len(moving_stack) > 1:
            return None
        return moving_stack

    def drop_card(self, card, from_slot, to_animate=False):
        """
        Drops a card or an entire stack from another slot into the current slot.

        For non-foundation slots, an entire valid stack of cards can be moved.
        For foundation slots, only a single card is allowed; thus, if the moving stack contains more than one card,
        the drop is rejected

        :param card: Top card to drop
        :param from_slot: The slot were the top card came from
        :param to_animate: If True, the card is dropped in animation mode
        :return: True if successful, False otherwise
        """
        moving_stack = self.check_if_can_drop(card, from_slot)

        if moving_stack is None:
            return False

        for moving_card in moving_stack:
            from_slot.cards.remove(moving_card)
            self.add_card(moving_card, to_animate=to_animate)
        return True

    def undo_drop_card(self, card, from_slot):

        moving_stack = from_slot.get_stack_from_card(card, max_stack=len(from_slot.cards))
        for moving_card in moving_stack:
            from_slot.cards.remove(moving_card)
            self.add_card(moving_card, to_animate=False)
        return True


    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

    def __repr__(self):
        return self.__str__()