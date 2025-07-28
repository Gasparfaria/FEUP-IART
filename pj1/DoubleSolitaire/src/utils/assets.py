import pygame

class AssetManager:
    """
    Simple AssetManager class.

    Caches assets to avoid loading them multiple times.
    """
    _images = {}
    _fonts = {}

    @classmethod
    def load_image(cls, path):
        if path not in cls._images:
            cls._images[path] = pygame.image.load(path).convert_alpha()
        return cls._images[path]

    @classmethod
    def load_font(cls, path, size):
        key = f"{path}_{size}"
        if key not in cls._fonts:
            cls._fonts[key] = pygame.font.Font(path, size)
        return cls._fonts[key]

# Usage:
# image = AssetManager.load_image("assets/images/icons/IconLarge.png")
# font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
