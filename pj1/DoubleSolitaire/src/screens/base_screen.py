class Screen:
    """Abstract base class for screens."""
    def handle_event(self, event):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError
