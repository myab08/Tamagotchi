import pygame
class Button():
    def __init__(self, x, y, img):
        self.x, self.y  = x, y
        self.img = img
        self.rect = self.img.get_rect(topleft = (x, y))
        self.mouse_detec = False
        
    def click(self, action): 
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_detec = True 
            if action:
                return True   
        else: 
            self.mouse_detec = False
            
    def render(self, surface):
        if self.mouse_detec:
            surface.blit(self.img, self.rect)