import pygame

from aerforge.shape import *
from aerforge.color import *
from aerforge.error import *
from aerforge.vec2 import *

class Entity(pygame.Rect):
    def __init__(self, window, shape = Rect, width = 200, height = 200, x = 0, y = 0, color = Color(240, 240, 240), alpha = 255, fill = True, add_to_objects = True):
        self.window = window

        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.alpha = alpha

        self.fill = not fill

        self.shape = shape
        self.color = color

        self.scripts = []

        self.destroyed = False

        self.add_to_objects = add_to_objects

        if self.add_to_objects:
            self.window.objects.append(self)

    def _update(self):
        for script in self.scripts:
            script.update(self)

    def draw(self):
        if not self.destroyed:
            if self.shape == Rect:
                if self.alpha != 255:
                    shape_surf = pygame.Surface(pygame.Rect(self).size, pygame.SRCALPHA)
                    pygame.draw.rect(shape_surf, (self.color.r, self.color.g, self.color.b, self.alpha), shape_surf.get_rect(), self.fill)
                    self.window.window.blit(shape_surf, self)

                else:
                    pygame.draw.rect(self.window.window, self.color, self, self.fill)

            elif self.shape == Circle:
                if self.alpha != 255:
                    shape_surf = pygame.Surface(pygame.Rect(self).size, pygame.SRCALPHA)
                    pygame.draw.ellipse(shape_surf, (self.color.r, self.color.g, self.color.b, self.alpha), shape_surf.get_rect(), self.fill)
                    self.window.window.blit(shape_surf, self)

                else:
                    pygame.draw.ellipse(self.window.window, self.color, self, self.fill)

            else:
                raise ForgeError("Invalid shape")

    def set_fill(self, fill):
        self.fill = not fill

    def get_fill(self):
        return self.fill

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_alpha(self):
        return self.alpha

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def center(self):
        self.x = self.window.width / 2 - self.width / 2
        self.y = self.window.height / 2 - self.height / 2

    def center_x(self):
        self.x = self.window.width / 2 - self.width / 2

    def center_y(self):
        self.y = self.window.height / 2 - self.height / 2

    def hit(self, entity):
        if isinstance(entity, Vec2):
            return self.collidepoint((entity.x, entity.y))

        else:
            return self.colliderect(entity)

    def hit2(self, entity, collision_tolreance = 10):
        if self.hit(entity):
            if abs(entity.top - self.bottom) < collision_tolreance:
                return "bottom"

            elif abs(entity.bottom - self.top) < collision_tolreance:
                return "top"

            elif abs(entity.right - self.left) < collision_tolreance:
                return "left"

            elif abs(entity.left - self.right) < collision_tolreance:
                return "right"

            else:
                return "unknown"
        
        else:
            return ""

    def destroy(self):
        self.destroyed = True

        if self.add_to_objects:
            try:
                self.window.objects.pop(self.window.objects.index(self))

            except:
                pass

    def add_script(self, script):
        self.scripts.append(script)

    def remove_script(self, script):
        self.scripts.pop(self.scripts.index(script))