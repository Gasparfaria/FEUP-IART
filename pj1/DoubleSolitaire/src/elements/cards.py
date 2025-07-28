import random

import pygame

def load_card_images(filename, rows=4, cols=13):
    """
    Loads the sprite sheet and slices it

    The sprite sheet is divided into grids and columns in a grid where each card have a set size

    :param filename: The filepath to the sprite sheet
    :param rows: Number of rows in the sprite sheet
    :param cols: Number of columns in the sprite sheet
    :return: List of pygame.Surface objects each with 1 card image
    """
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    card_width = 48
    card_height = 64
    card_images = []

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * card_width, row * card_height, card_width, card_height)
            # .copy() creates a new Surface from the subsurface
            card_image = sprite_sheet.subsurface(rect).copy()
            card_images.append(card_image)
    return card_images


class Card(pygame.sprite.Sprite):
    """
    Class representing a card

    Atributes:
        suit: The suit of the card
        rank: The rank of the card
        image: The card image
        rect: The card rect for positioning
    """
    def __init__(self, suit, rank, image, position=(0, 0)):
        """
        Initializes the card

        :param suit: The suit of the card
        :param rank: The rank of the card
        :param image: The card image
        :param position: The position of the card
        """
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def __lt__(self, other):
        return len(self.rank) < len(other.rank)

    def update(self):
        """
        Updates the card

        Might be used for animations
        PLACEHOLDER
        """
        pass

    def flip(self):
        """
        PLACEHOLDER
        Might be used for animations
        """
        pass

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    # Método para desenhar o destaque ao redor da carta
    def draw_hint(self, surface, foundation=None):
        """
        Desenha um destaque ao redor da carta para indicar que ela é uma dica.
        :param surface: A superfície onde o destaque será desenhado.
        :param foundation: O slot de destino (opcional, pode ser usado para mais lógica no futuro).
        """
        highlight_color = (255, 215, 0)  # Cor dourada
        border_thickness = 4
        pygame.draw.rect(
            surface,
            highlight_color,
            self.rect.inflate(10, 10),  # Aumenta o tamanho do retângulo para criar bordas
            border_thickness,
            border_radius=8  # Bordas arredondadas
        )

class Cards:
    """
    Class representing the card deck
    """
    def __init__(self,cards_path):
        """
        Initializes the card deck
        :param cards_path: The filepath to the sprite sheet
        """
        self.cards = []
        card_images = load_card_images(cards_path)
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

        for row, suit in enumerate(suits):
            for col, rank in enumerate(ranks):
                image_index = row * 13 + col
                card_image = card_images[image_index]
                card = Card(suit,rank,card_image)
                self.cards.append(card)

    def shuffle(self):
        """
        Shuffles the cards randomly
        :return:
        """
        self.all_cards = self.cards[:]
        random.shuffle(self.cards)

    def is_in_deck(self, card):
        if card in self.cards:
            return True
        return False

    def pop(self, suit, rank):
        """
        Removes the specified card from the deck based on its suit and rank
        :param suit: The suit of the card
        :param rank: The rank of the card
        :return: The card
        """
        for card in self.cards:
            if card.suit == suit and card.rank == rank:
                self.cards.remove(card)
                return card
        return None

    def deal(self, num_cards):
        """
        Deals num_cards cards from the deck
        :param num_cards: The number of cards to deal
        :return: List of cards dealt
        """
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def restore(self):
        self.cards = self.all_cards[:]

    def __repr__(self):
        return str([card for card in self.all_cards])