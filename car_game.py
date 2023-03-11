import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()
font = pygame.font.Font(None, 25)

from button import Button

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
DEFAULT_SPEED = 1
INCREMENT = 0.25

# Car = namedtuple('Car','x , y , speed')
class Car:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class CarGame:
    def __init__(self,w=900,h=600):
        self.w=w
        self.h=h
        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Car')
        self.clock = pygame.time.Clock()
        
        #init game state
        self.direction = Direction.NONE
        # self.head = Point(self.w/2,self.h/2)
        # self.snake = [self.head,
        #               Point(self.head.x-BLOCK_SIZE,self.head.y),
        #               Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]
        self.score = 0
        self.game_over = False
        self.quit_button = pygame.Rect(600, 500, 50, 20)

        self._reset()
        # self.food = None
        # self._place__food()
    def _reset(self):
        # self.main.x = self.w/2
        # self.main.y = self.h - 10 * BLOCK_SIZE
        self.car1 = Car(self.w/2,self.h/2 + 5 * BLOCK_SIZE, DEFAULT_SPEED)
        self.car2 = Car(self.w/2 - 2 * CAR_WID, 0, -DEFAULT_SPEED)
        self.main = Car(self.w/2, self.h/2 + 15 * BLOCK_SIZE, DEFAULT_SPEED)


    # def _place__food(self):
    #     x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    #     y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    #     self.food = Point(x,y)
    #     if(self.food in self.snake):
    #         self._place__food()


    def play_step(self):
        # 1. Collect the user input
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    self.direction = Direction.LEFT
                elif(event.key == pygame.K_RIGHT):
                    self.direction = Direction.RIGHT
                elif(event.key == pygame.K_UP):
                    self.direction = Direction.UP
                elif(event.key == pygame.K_DOWN):
                    self.direction = Direction.DOWN
            else:
                self.direction = Direction.NONE
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if self.quit_button.collidepoint(x, y):
                        self.end_game()
        # 2. Move
        self._move(self.direction)
        # self.snake.insert(0,self.head)

        # 3. Check if game Over
        # game_over = False 
        if(self._is_collision()):
            self.game_over=True
            return self.game_over,self.score
        
        if(self._score()):
            self.score += 1
            self._reset()
        # 4. Place new Food or just move
        # if(self.head == self.food):
        #     self.score+=1
        #     self._place__food()
        # else:
        #     self.snake.pop()
        # 5. Update UI and clock
        self._update_ui()
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
        # for pt in self.snake:
        #     pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
        #     pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        # pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.score)+'\n',True,WHITE)
        # text = font.render("Your speed: "+str(self.main.speed) +'\n',True,WHITE,)
        # text = font.render("Other speed: "+str(self.car1.speed)+'\n',True,WHITE)
        self.display.blit(text,[0,0])
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
        self.main.y -= (self.main.speed - self.car1.speed) * BLOCK_SIZE

        #update opposing car
        self.car2.y += (self.main.speed) * BLOCK_SIZE
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