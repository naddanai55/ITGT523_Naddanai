# filepath: c:\Users\Nai\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\fall_detect\button.py
import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, sound=None):
        self.text = text  
        self.rect = pygame.Rect(x, y, width, height)  
        self.color = color  
        self.hover_color = hover_color  
        self.action = action  
        self.sound = sound

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(screen, color, self.rect)
        text_surface = pygame.font.Font(None, 36).render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.sound:
                self.sound.play()  # Play the sound effect
            if self.action:
                self.action()