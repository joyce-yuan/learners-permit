# import pygame_textinput
# import pygame
# pygame.init()

# # class Input_Rectangle:
# #     def __init__(self, x, y, color=pygame.Color('lightskyblue3')):

# # Create TextInput-object
# rect1 = pygame.Rect(10, 10, 140, 32)
# textinput1 = pygame_textinput.TextInputVisualizer()
# textinput2 = pygame_textinput.TextInputVisualizer()
# rect2 = pygame.Rect(10, 20, 140, 32)

# screen = pygame.display.set_mode((1000, 500))
# clock = pygame.time.Clock()

# while True:
#     screen.fill((225, 225, 225))

#     events = pygame.event.get()

#     # Feed it with events every frame
#     textinput1.update(events)
#     textinput2.update(events)
#     # Blit its surface onto the screen
#     pygame.draw.rect(screen,pygame.Color('lightskyblue3'),rect1)
#     pygame.draw.rect(screen,pygame.Color('green'),rect2)
#     screen.blit(textinput1.surface, (10, 10))
#     screen.blit(textinput2.surface, (10, 30))

#     for event in events:
#         if event.type == pygame.QUIT:
#             exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if rect1.collidepoint(event.pos):
#                 active = True
#             else:
#                 active = False

#     pygame.display.update()
#     clock.tick(30)

# # import sys module
# import pygame
# import sys
  
  
# # pygame.init() will initialize all
# # imported module
# pygame.init()
  
# clock = pygame.time.Clock()
  
# # it will display on screen
# screen = pygame.display.set_mode([600, 500])
  
# # basic font for user typed
# base_font = pygame.font.Font(None, 32)

# def input_screen():
#     user_text = ''
  
#     # create rectangle
#     input_rect = pygame.Rect(200, 200, 140, 32)
    
#     # color_active stores color(lightskyblue3) which
#     # gets active when input box is clicked by user
#     color_active = pygame.Color('lightskyblue3')
    
#     # color_passive store color(chartreuse4) which is
#     # color of input box.
#     color_passive = pygame.Color('chartreuse4')
#     color = color_passive
    
#     active = False
    
#     while True:
#         for event in pygame.event.get():
    
#         # if user types QUIT then the screen will close
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
    
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if input_rect.collidepoint(event.pos):
#                     active = True
#                 else:
#                     active = False
#             if event.type == pygame.KEYDOWN:
        
#                     # Check for backspace
#                     if event.key == pygame.K_BACKSPACE:
        
#                         # get text input from 0 to -1 i.e. end.
#                         user_text = user_text[:-1]
        
#                     # Unicode standard is used for string
#                     # formation
#                     else:
#                         user_text += event.unicode
            
#             # it will set background color of screen
#             screen.fill((255, 255, 255))
        
#             if active:
#                 color = color_active
#             else:
#                 color = color_passive
          
#             # draw rectangle and argument passed which should
#             # be on screen
#             pygame.draw.rect(screen, color, input_rect)
        
#             text_surface = base_font.render(user_text, True, (255, 255, 255))
            
#             # render at position stated in arguments
#             screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            
#             # set width of textfield so that text cannot get
#             # outside of user's text input
#             input_rect.w = max(100, text_surface.get_width()+10)
            
#             # display.flip() will update only a portion of the
#             # screen to updated, not full area
#             pygame.display.flip()
            
#             # clock.tick(60) means that for every second at most
#             # 60 frames should be passed.
#             clock.tick(60)

import pygame as pg

pg.init()
screen = pg.display.set_mode((700, 600))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, label='', text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.label = FONT.render(label, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.label, (self.rect.x, self.rect.y - self.label.get_height()))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


# mainx, mainy, mainv, car1x, car1y, car1v, car2x, car2y, car2v
# def main():
#     clock = pg.time.Clock()
#     labels = ["Main Car Y: ", "Main Car V: ", "Car 1 Y: ", "Car 1 V: ", "Car 2 Y: ", "Car 2 V: "]
#     input_boxes = []
#     y = 100
#     for label in labels:
#         input_box = InputBox(400, y, 50, 32, label)
#         input_boxes.append(input_box)
#         y += 70

#     done = False

#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)

#         for box in input_boxes:
#             box.update()

#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)

#         pg.display.flip()
#         clock.tick(30)

# main()