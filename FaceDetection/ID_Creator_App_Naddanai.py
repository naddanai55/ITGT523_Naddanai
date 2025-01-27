import pygame  
import cv2     
import numpy as np  
from tkinter import Tk  
from tkinter.filedialog import askopenfilename, asksaveasfilename  

pygame.init()
screen = pygame.display.set_mode((800, 600))  
pygame.display.set_caption("ID Creator App")

WHITE = (255, 255, 255)
GREY = (242, 239, 231)
TEAL = (72, 166, 167)
BLUE = (41, 115, 178)
SKY = (154, 203, 208)
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

sound_start_path = 'sound/startup.mp3'
sound_button_click_path = 'sound/click.mp3'
sound_process_done_path = 'sound/process.mp3'

pygame.mixer.music.load(sound_start_path)
pygame.mixer.music.play(0, 0.0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text  
        self.rect = pygame.Rect(x, y, width, height)  
        self.color = color  
        self.hover_color = hover_color  
        self.action = action  

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                pygame.mixer.music.load(sound_button_click_path)
                pygame.mixer.music.play()
                self.action()

def load_image():
    global input_image, message
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.destroy()
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            message = "Invalid image path."
            return
        input_image = img
        message = "Image loaded! Press 'Process' to continue."

def process_image():
    global input_image, processed_card, message, cartoon_filter_enabled
    if input_image is None:
        message = "No image loaded."
        return

    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)  
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        message = "No face detected."
        return

    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    face_img = input_image[y:y+h, x:x+w]
    face_img = cv2.resize(face_img, (250, 250))
    
    if cartoon_filter_enabled:
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        face_blur = cv2.medianBlur(face_gray, 5)
        getEdge = cv2.adaptiveThreshold(face_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color_img = cv2.bilateralFilter(face_img, 9, 300, 300)
        face_img = cv2.bitwise_and(color_img, color_img, mask=getEdge)
    # cv2.imshow("Cartoon", cartoon_img)

    card_template = cv2.imread('bg.png')
    x_offset = 688  
    y_offset = 228  
    card_template[y_offset:y_offset + face_img.shape[0], x_offset:x_offset + face_img.shape[1]] = face_img  

    processed_card = card_template  
    message = "Image processed!"
    pygame.mixer.music.load(sound_process_done_path) 
    pygame.mixer.music.play()

def save_image():
    global processed_card, message
    if processed_card is None:
        message = "No processed image to save."
        return

    root = Tk()
    root.withdraw()
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])  # Ask user where to save the file
    root.destroy()

    if file_path:
        cv2.imwrite(file_path, processed_card)
        message = f"Image saved to {file_path}"

def convert_cv_to_pygame(cv_img):
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return pygame.surfarray.make_surface(np.transpose(rgb_img, (1, 0, 2)))

def toggle_cartoon_filter():
    global cartoon_filter_enabled, message
    cartoon_filter_enabled = not cartoon_filter_enabled
    # message = f"Cartoon filter {'enabled' if cartoon_filter_enabled else 'disabled'}."

buttons = [
    Button("Load Image", 50, 500, 150, 50, TEAL, BLUE, load_image),
    Button("Process", 205, 500, 150, 50, TEAL, BLUE, process_image),
    Button("Export", 535, 500, 150, 50, TEAL, BLUE, save_image),
    Button("Filter", 205, 555, 100, 40, TEAL, BLUE, toggle_cartoon_filter),
]

running = True
cartoon_filter_enabled = True 
input_image = None  
processed_card = None  
message = "Welcome! to ID Creator Load an image to get started."

while running:
    screen.fill(GREY)
    name_text = title_font.render("ID Creator", True, BLUE)
    screen.blit(name_text, (50, 30))
    
    pygame.draw.rect(screen, SKY, (0, 150, 800, 300)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            button.is_clicked(event)

    for button in buttons:
        button.draw(screen)

    if input_image is not None:
        input_surface = convert_cv_to_pygame(input_image) 
        screen.blit(pygame.transform.scale(input_surface, (300, 300)), (50, 150))
        img_text = font.render("Your image!", True, BLUE)
        screen.blit(img_text, (140, 460))  

    if processed_card is not None:
        card_surface = convert_cv_to_pygame(processed_card)  
        screen.blit(pygame.transform.scale(card_surface, (300, 300)), (450, 150))
        card_text = font.render("Your card!", True, BLUE)
        screen.blit(card_text, (550, 460)) 
        
    message_surface = font.render(message, True, BLUE)
    screen.blit(message_surface, (50, 100))
    
    filter_status = font.render(f": {'On' if cartoon_filter_enabled else 'Off'}", True, BLUE)
    screen.blit(filter_status, (310, 565))

    pygame.display.flip()
    # key = cv2.waitKey(0)
    # cv2.destroyAllWindows()
pygame.quit()
