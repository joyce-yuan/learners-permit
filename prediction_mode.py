import pygame
import random
from enum import Enum
from collections import namedtuple
import csv
from input import InputBox
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
import pickle



pygame.init()
font_heading = pygame.font.Font('arial/arial.ttf',25)
font_text = pygame.font.Font('arial/arial.ttf',15)

# Reset 
# Reward
# Play(action) -> Direction
# Game_Iteration
# is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    NONE = 5
 

BLOCK_SIZE=10
SPEED =10
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

CAR_LEN = 20
CAR_WID = 20
DEFAULT_SPEED = 40
INCREMENT = 5

#used for recording
SECONDS_PER_DATA = 15
RECORD_INTERVAL = 1

#Data stuff
RECORD = False
DATA = []
if RECORD:
    with open('car_passing_data-1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',',quoting = csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            DATA.append(row)

WRITE_FILE = '11-23-2022-example-3.csv'

#Model Machine Learning Stuff
# load model
filename = "./models/first.pickle"
model = pickle.load(open(filename, "rb"))

# Pause / Play Button
PAUSE_IMG = pygame.transform.scale(pygame.image.load("./assets/pause.png").convert(), (50, 50))
PLAY_IMG = pygame.transform.scale(pygame.image.load("./assets/play.png").convert(), (50, 50))

#PASSING

# Car = namedtuple('Car','x , y , speed')
class Car:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.dragging = False

class CarGame:
    def __init__(self,write_file,w=900,h=600):
        self.w=w
        self.h=h
        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Car')
        self.clock = pygame.time.Clock()
        
        #init game state
        self.direction = Direction.NONE
        self.score = 0
        self.game_over = False
        self.quit_button = pygame.Rect(800, 500, 50, 30)

        #timer options
        self.seconds = 0
        self.pause = False #this will double as play function
        self.success = "None"
        self.pause_button = pygame.Rect(40, 200, 50, 50)

        #labels on the side
        self.labels = ["Main Car Y: ", "Main Car V: ", "Car 1 Y: ", "Car 1 V: ", "Car 2 Y: ", "Car 2 V: "]
        self.input_boxes = []
        y = 100
        for label in self.labels:
            input_box = InputBox(500, y, 50, 32, label)
            self.input_boxes.append(input_box)
            y += 70

        #model_prediction
        self.prediction = None
        
        self._reset()

        #data index
        if RECORD:
            self.data_index = 1
            temp = DATA[self.data_index]
            self._set_scene(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8])
            
        #setting up the write file
        self.WRITE_FILE = write_file


    def _reset(self):
        #starting positions
        self.car1 = Car(self.w/2,self.h/2 + 15 * BLOCK_SIZE, DEFAULT_SPEED)
        self.car2 = Car(self.w/2 - 2 * CAR_WID, 0, -DEFAULT_SPEED)
        self.main = Car(self.w/2, self.h/2 + 20 * BLOCK_SIZE, DEFAULT_SPEED)
        self.pause = False

    def _set_scene(self, mainy, mainv, car1y, car1v, car2y, car2v):
        self.car1 = Car(self.w/2, car1y, car1v)
        self.car2 = Car(self.w/2 - 2 * CAR_WID, car2y, -car2v)
        self.main = Car(self.w/2, mainy, mainv)
        self.pause = False
        self.success = "None"

    def record(self, record_string):
        with open (self.WRITE_FILE,"a") as f:
                f.write(record_string) 
        return


    def play_step(self):
        cars = [self.main, self.car1, self.car2]

        # 1. Collect the user input
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                temp = '1,\n' if (self.success == "Passed") else '0,\n'
                self.record(temp)
                pygame.quit()
                quit()
            if self.pause:
                for box in self.input_boxes:
                    box.handle_event(event)
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT)) or \
                (event.type == pygame.MOUSEBUTTONDOWN and self.pause_button.collidepoint(pygame.mouse.get_pos())):
                    #TODO: fix logic completely
                    #record the last pass or fail
                    temp = '1,\n' if (self.success == "Passed") else '0,\n'
                    self.record(temp)

                    temp = []
                    for box in self.input_boxes:
                        if box.text:
                            temp.append(int(box.text))
                        
                        #hack
                        else:
                            print("apending default value")
                            temp.append(0)

                    # hack for adding drag and drop functionality
                    # instead of changing the input, I will change the actual values before set scene
                    # TODO: actually fix set scene to be more versatile
                    temp[0] = self.main.y
                    temp[2] = self.car1.y
                    temp[4] = self.car2.y

                    # model makes a prediction here
                    self.prediction = model.predict(np.array([484, 50, 450.0, 50, 10.0, 40]).reshape(1, -1))
                    print(f"Model Predicted: {self.prediction}")

                    self._set_scene(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5])
                    self.record(f'{temp[0]},{temp[1]},{temp[2]},{temp[3]},{temp[4]},{temp[5]},')
                    pygame.time.wait(500)
            if(event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    self._reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if self.quit_button.collidepoint(x, y):
                        self.end_game()

            # drag and drop logic
                if event.button == 1: 
                    for car in cars:
                        if pygame.Rect(car.x, car.y, CAR_LEN , CAR_WID).collidepoint(event.pos):
                            car.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   
                    for car in cars:         
                        car.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                for car in cars:
                    if car.dragging:
                        car.x, car.y = event.pos
                    
            #     if (event.key == pygame.K_RIGHT):
            #         self.record()
            #         self.data_index += 1
            #         temp = DATA[self.data_index]
            #         self._set_scene(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8])
            #         pygame.time.wait(500)
                    
            # if(event.type == pygame.KEYDOWN):
            #     if(event.key == pygame.K_LEFT):
            #         self.direction = Direction.LEFT
            #     elif(event.key == pygame.K_RIGHT):
            #         self.direction = Direction.RIGHT
            #     elif(event.key == pygame.K_UP):
            #         self.direction = Direction.UP
            #     elif(event.key == pygame.K_DOWN):
            #         self.direction = Direction.DOWN
            # else:
            #     self.direction = Direction.NONE
        self.direction = self._passing()
        # 2. Move

        if not self.pause:
            self._move(self.direction)
        # self.snake.insert(0,self.head)

        # 3. Check if game Over
        if(self._is_collision()):
            # game_over=True
            # return game_over,self.score
            self.success = "Failed"
            # self.record('0,\n')
            # self.data_index += 1
            # temp = DATA[self.data_index]
            # self._set_scene(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8])
            # pygame.time.wait(500)
            self.pause = True
        
        if(self._score()):
            self.success = "Passed"
            # self.record('1,\n')
            # self.data_index += 1
            # temp = DATA[self.data_index]
            # self._set_scene(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8])
            # pygame.time.wait(500)
            self.pause = True
            # self.score += 1
        #     self._reset()

        # 5. Update UI and clock
        self._update_ui()
        # self.record()
        self.clock.tick(SPEED)
        # 6. Return game Over and Display Score
        
        return self.game_over,self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        pygame.draw.line(self.display, WHITE, (self.w/2 - 3*CAR_WID, 0),(self.w/2 - 3*CAR_WID, self.h))
        pygame.draw.line(self.display, WHITE, (self.w/2 + 2*CAR_WID, 0),(self.w/2 + 2*CAR_WID, self.h))
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.main.x, self.main.y, CAR_LEN , CAR_WID))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.car1.x, self.car1.y, CAR_LEN, CAR_WID))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.car2.x, self.car2.y, CAR_LEN, CAR_WID))
        pygame.draw.rect(self.display, "pink", self.quit_button)
        self.display.blit(font_text.render("Menu",True, BLACK), [self.quit_button.x+5, self.quit_button.y+5])

        text = font_heading.render("Score: "+str(self.score)+'\n',True,WHITE)

        stats = [font_text.render(f'Main Car: {self.main.speed} mph ({self.main.x}, {self.main.y})',True, WHITE),
        font_text.render(f'Car 1: {self.car1.speed} mph ({self.car1.x}, {self.car1.y})', True, WHITE), 
        font_text.render(f'Car 2: {self.car2.speed} mph ({self.car2.x}, {self.car2.y})', True, WHITE), 
        font_text.render(f'Prediction: {self.prediction}', True, WHITE),
        font_text.render(f'Status: {self.success}', True, WHITE)
        ]

        cursor = 25

        self.display.blit(text,[0,0])
        for i in range(len(stats)):
            self.display.blit(stats[i], [10, cursor])
            cursor += 20

        # pause and play button
        self.display.blit(font_heading.render("Play Button", True, WHITE), [10, cursor])
        cursor += 20
        temp_button = PLAY_IMG if self.pause else PAUSE_IMG
        self.display.blit(temp_button, self.pause_button)

        for index, box in enumerate(self.input_boxes):
            #hack for velocity input
            #TODO: fix this
            if index % 2 == 1:
                box.draw(self.display)
        pygame.display.flip()

    def end_game(self):
        self.game_over = True
    
    def _score(self):
        return self.main.y < self.car1.y and self.main.x >= self.car1.x

    def _move(self,direction):
        # x = self.main.x
        # y = self.main.y
        if(direction == Direction.RIGHT):
            # x+=BLOCK_SIZE
            self.main.x += BLOCK_SIZE
        elif(direction == Direction.LEFT):
            self.main.x -= BLOCK_SIZE
        elif(direction == Direction.DOWN):
            # y+=BLOCK_SIZE
            self.main.speed -= INCREMENT
        elif(direction == Direction.UP):
            # y-=BLOCK_SIZE
            self.main.speed += INCREMENT
        self.main.y -= (self.main.speed - self.car1.speed) * BLOCK_SIZE / 40

        #update opposing car
        self.car2.y += (self.main.speed) * BLOCK_SIZE / 40
        #probability another car shows up is around 50%
        if (self.car2.y > self.h and random.randint(1, 10) <= 5):
            self.car2.y = 0

    def _is_collision(self):
        #hit boundary
        if(self.main.x>(self.w/2 + 1 * CAR_WID) or self.main.x<(self.w/2 - 3 *CAR_WID) or self.main.y>self.h - BLOCK_SIZE or self.main.y<0):
            return True
        right = self.car1.x + (CAR_WID * 3/2)
        left = self.car1.x - (CAR_WID * 3/2)
        top = self.car1.y - (CAR_LEN * 3/2)
        bottom = self.car1.y + (CAR_LEN * 3/2)
        if (left < self.main.x and self.main.x < right):
            if (top < self.main.y and self.main.y < bottom):
                return True

        right = self.car2.x + (CAR_WID * 3/2)
        left = self.car2.x - (CAR_WID * 3/2)
        top = self.car2.y - (CAR_LEN * 3/2)
        bottom = self.car2.y + (CAR_LEN * 3/2)
        if (left < self.main.x and self.main.x < right):
            if (top < self.main.y and self.main.y < bottom):
                return True
        # if(self.head in self.snake[1:]):
        #     return True
        return False

    def _passing(self):
        if self.main.x > self.car1.x - 3/2 * CAR_WID and self.main.y > self.car1.y - CAR_LEN:
            # print(self.main.x, self.main.y, self.car1.x)
            # print("go left")
            return Direction.LEFT
        elif self.main.y > self.car1.y - 3/2 *CAR_LEN:
            if self.main.speed >= self.car1.speed + 15:
                # print("cruisin to pass")
                return Direction.NONE
            else:
                # print("go up")
                return Direction.UP
        elif self.main.x < self.car1.x:
            # print("go right")
            return Direction.RIGHT

        #successfully passed
        elif self.main.speed > self.car1.speed:
            # print("nothing")
            return Direction.DOWN
        else:
            return Direction.NONE


if __name__=="__main__":
    game = CarGame()

    #Game loop
    #game_over=False
    while True:
        game_over,score=game.play_step()
        if(game_over == True):
            break
    print('Final Score',score)

    pygame.quit()