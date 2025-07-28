import pygame
import math

class ObjectMove:
    """
    Generic object move animation
    """
    def __init__(self, anim_obj, start_pos, target_pos, duration, on_complete=None, top_left=True):
        """
        Initializing the animation object
        :param anim_obj: Object with rect attribute
        :param start_pos: Start position
        :param target_pos: End position
        :param duration: Animation duration
        """
        self.anim_obj = anim_obj
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.duration = duration
        self.on_complete = on_complete
        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.top_left = top_left

    def update(self):
        """
        Update the object's position based on the elapsed time.
        """
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.start_time) / self.duration

        if progress >= 1:
            self.active = False
            if self.top_left:
                self.anim_obj.rect.topleft = self.target_pos
            else:
                self.anim_obj.rect.center = self.target_pos

            if self.on_complete:
                self.on_complete()
            return

        # exaggerated ease-in-out (extreme acceleration & deceleration)
        if progress < 0.5:
            smooth_progress = 8 * progress ** 4
        else:
            smooth_progress = 1 - (-2 * progress + 2) ** 4 / 2

        # Compute position
        new_x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * smooth_progress
        new_y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * smooth_progress

        if self.top_left:
            self.anim_obj.rect.topleft = (new_x, new_y)
        else:
            self.anim_obj.rect.center = (new_x, new_y)