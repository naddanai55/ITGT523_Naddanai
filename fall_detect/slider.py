import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, height)  # Slider bar rectangle
        self.min_val = min_val  # Minimum value of the slider
        self.max_val = max_val  # Maximum value of the slider
        self.value = start_val  # Current value of the slider
        self.knob_rect = pygame.Rect(
            x + (start_val - min_val) / (max_val - min_val) * width - 10, y - 5, 20, height + 10
        )  # Knob rectangle
        self.dragging = False  # Whether the knob is being dragged

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, (200, 200, 200), self.rect)  # Light gray bar
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border

        # Draw the knob
        pygame.draw.rect(screen, (255, 165, 0) if self.dragging else (0, 0, 255), self.knob_rect)

        # Draw the current value as text
        font = pygame.font.Font(None, 24)
        value_text = font.render(f"{int(self.value)}", True, (0, 0, 0))
        screen.blit(value_text, (self.rect.x + self.rect.width + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update the knob position
            new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.knob_rect.x = new_x - self.knob_rect.width // 2

            # Update the value based on the knob position
            self.value = self.min_val + (new_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.value