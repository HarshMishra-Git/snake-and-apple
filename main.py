import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y)) # this method is showing apple on the window
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,39)* SIZE
        self.y = random.randint(1,19)* SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]
   
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'


    def move_down(self):
        self.direction = 'down'
    
    def walk(self):

        for i in range(self.length-1,0,-1): # reverse the direction of the object
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]


        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i])) # this method is showing block on the window      
        pygame.display.flip()
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
class Game:
    def __init__(self):
        pygame.init() #to initialise the module
        pygame.mixer.init()
        pygame.display.set_caption("NOKIA GAME IN PC")
        self.surface = pygame.display.set_mode((1600,900)) # to display the game window
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.play_BG_music()
        pygame.draw.rect(self.surface,(255,255,255),(0,0,1600,900),2)
    def render_BG(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
    
    
    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2 + SIZE:
            if y1>=y2 and y1<y2 + SIZE:
                return True
        return False
    def play(self):
        self.render_BG()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()


        # snake self collison
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision detected"

                    # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1600 and 0 <= self.snake.y[0] <= 900):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"score : {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (1450,10))
    


    def play_BG_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")    
        pygame.mixer.Sound.play(sound)


    def show_game_over(self):
        self.render_BG()
        font = pygame.font.SysFont('arial',30)
        line1= font.render(f"Game is over ! your score is : {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (300,500))
        line2= font.render(f"To play game press ENTER. To exit game press ESC!", True, (255,255,255))
        self.surface.blit(line2, (300,550))
        pygame.mixer.music.pause()

        pygame.display.flip()
       

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get(): # this method is use to get all the events which are performed by the keyboard or mouse
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                    
                elif event.type == QUIT:
                    running = False


            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                

            time.sleep(.2)

if __name__ == "__main__":
    game = Game()
    game.run()
    
