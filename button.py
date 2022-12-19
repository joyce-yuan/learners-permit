# Imports
import sys
import pygame

# Configuration
# pygame.init()
# fps = 60
# fpsClock = pygame.time.Clock()
# width, height = 640, 480
# screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 20)

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, x, y, text = "None", font = pygame.font.SysFont("Arial", 20), bg="black", feedback=""):
        self.x, self.y = x, y
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        """Change the text when you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))
 
    def click(self, event, onClick):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    onClick()
        return True

# class Button():
#     def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.onclickFunction = onclickFunction
#         self.onePress = onePress

#         self.fillColors = {
#             'normal': '#ffffff',
#             'hover': '#666666',
#             'pressed': '#333333',
#         }

#         self.buttonSurface = pygame.Surface((self.width, self.height))
#         self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

#         self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

#         self.alreadyPressed = False

#         # objects.append(self)

#     def process(self, screen):

#         mousePos = pygame.mouse.get_pos()
        
#         self.buttonSurface.fill(self.fillColors['normal'])
#         if self.buttonRect.collidepoint(mousePos):
#             self.buttonSurface.fill(self.fillColors['hover'])

#             if pygame.mouse.get_pressed(num_buttons=3)[0]:
#                 self.buttonSurface.fill(self.fillColors['pressed'])

#                 if self.onePress:
#                     self.onclickFunction()

#                 elif not self.alreadyPressed:
#                     self.onclickFunction()
#                     self.alreadyPressed = True

#             else:
#                 self.alreadyPressed = False

#         self.buttonSurface.blit(self.buttonSurf, [
#             self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
#             self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
#         ])
#         screen.blit(self.buttonSurface, self.buttonRect)

# def myFunction():
#     print('Button Pressed')

# import pygame

# class Button:
#     """Create a button, then blit the surface in the while loop"""
#     # def __init__(self, x, y, length, width, label, font)
 
#     def __init__(self, x, y, font, bg="black", feedback=""):
#         self.x, self.y = x, y
#         self.font = pygame.font.SysFont("Arial", font)
#         if feedback == "":
#             self.feedback = "text"
#         else:
#             self.feedback = feedback
#         self.change_text(text, bg)
 
#     def change_text(self, text, bg="black"):
#         """Change the text whe you click"""
#         self.text = self.font.render(text, 1, pygame.Color("White"))
#         self.size = self.text.get_size()
#         self.surface = pygame.Surface(self.size)
#         self.surface.fill(bg)
#         self.surface.blit(self.text, (0, 0))
#         self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
#     def show(self, screen):
#         screen.blit(button1.surface, (self.x, self.y))
 
#     def click(self, event):
#         x, y = pygame.mouse.get_pos()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.mouse.get_pressed()[0]:
#                 if self.rect.collidepoint(x, y):
#                     self.change_text(self.feedback, bg="red")