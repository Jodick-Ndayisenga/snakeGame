import pygame
from settings import *
import Sprites as Raja
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.orientation = 0
        self.paused = False
        self.playing = True
        self.score = 0
        self.high_score = self.get_high_score()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.head = Raja.Snake(self, 0, 0)
        self.snake_parts = []
        self.snake_parts.append(Raja.Snake(self, 4, 5))
        self.snake_parts.append(Raja.Snake(self, 3, 5))

        self.food = Raja.Foods(self, 10, 5)

    def is_body_part(self):
        #changing the position of the food
        x = random.randint(0, GRIDWIDTH-1)
        y = random.randint(0, GRIDHEIGHT-1)
        for body in self.snake_parts:
            if x == body.x and y == body.y:
                x, y = self.is_body_part()
            else:
                return x, y

    def run(self):
        # this function is actually our game loop
        self.playing = True
        while self.playing:
            self.clock.tick(SPEED)
            self.events()
            self.update()
            self.draw()


    def quit(self):
        pygame.quit()
        quit(0)

    def update(self):
        if not self.paused:
            if self.food.food_collision():
                x, y = self.is_body_part()
                self.food.x = x
                self.food.y = y
                self.snake_parts.append(Raja.Snake(self, self.snake_parts[-1].x, self.snake_parts[-1].y))
                self.score +=1

            self.all_sprites.update()
            #track and move body parts
            x, y = self.head.x, self.head.y
            for body in self.snake_parts:
                temp_x, temp_y = body.x, body.y
                body.x, body.y = x, y
                x, y = temp_x, temp_y
            
            if self.orientation == 0:
                self.head.x += 1

            elif self.orientation == 1:
                self.head.y -=1

            elif self.orientation == 2:
                self.head.x -=1

            elif self.orientation == 3:
                self.head.y +=1

            #check for body collision
            for body in self.snake_parts:
                if body.body_collision():
                    self.playing = False
    #send the snake to the other side of the screen if it disappear from one side
            if self.head.x > GRIDWIDTH:
                self.head.x = 0

            elif self.head.x < 0:
                self.head.x = GRIDWIDTH

            elif self.head.y > GRIDHEIGHT:
                self.head.y = 0

            elif self.head.y <0:
                self.head.y = GRIDHEIGHT

    def draw_grid(self):
        for row in range(0, WIDTH, TELESIZE):
            pygame.draw.line(self.screen, LIGHTGREY,(row, 0),(row, HEIGHT))
        for column in range(0, HEIGHT, TELESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, column), (WIDTH, column))

    def draw(self):
        self.screen.fill(BACKGROUNDCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        if self.paused:
            Raja.Uielements(10, 10, 'PAUSED').draw(self.screen,  100)
        pygame.display.flip()

    def events(self):
        # track all the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_UP or event.key == pygame.K_w:
                    if not self.orientation == 3:
                        self.orientation = 1

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.orientation == 1:
                        self.orientation = 3

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not self.orientation == 0:
                        self.orientation = 2

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not self.orientation == 2:
                        self.orientation = 0

                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def wait(self):
        waiting = True
        while waiting:
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                mouce_x, mouce_y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_button.is_over(mouce_x, mouce_y):
                        self.start_button.colour = LIGHTGREY
                    else:
                        self.start_button.colour = BACKGROUNDCOLOR

                    if self.quit_button.is_over(mouce_x, mouce_y):
                        self.quit_button.colour = LIGHTGREY
                    else:
                        self.quit_button.colour = BACKGROUNDCOLOR

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(mouce_x, mouce_y):
                        waiting = False
                
                elif self.quit_button.is_over(mouce_x, mouce_y):
                    self.quit()

    def get_high_score(self):
        with open ('High_score.txt', 'r') as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open ('High_score.txt', 'w') as file:
            if int(self.score) > int(self.high_score):
                file.write(str(self.score))
            else:
                file.write(str(self.high_score))


    def main_screen(self):
        self.save_score()
        self.screen.fill(BACKGROUNDCOLOR)
        if not self.playing:
            Raja.Uielements(8, 7, 'GAME OVER!').draw(self.screen, 100)
            Raja.Uielements(14, 13, f'You scored: {self.score}!').draw(self.screen, 30)

        else:
            Raja.Uielements(8, 7, 'SNAKE GAME').draw(self.screen, 100)

        Raja.Uielements(13, 11, f'High Score: {self.high_score if self.high_score > self.score else self.score}!').draw(self.screen, 30)

        self.start_button = Raja.Button(self, BACKGROUNDCOLOR, WHITE, WIDTH/2-(150/2), 470, 150, 50 , 'START')
        self.quit_button = Raja.Button(self, BACKGROUNDCOLOR, WHITE, WIDTH/2-(150/2), 545, 150, 50 , 'QUIT')
        
        self.wait()


game = Game()

while True:# this loop here is to keep the window open and running
    game.main_screen()
    game.new()
    game.run()