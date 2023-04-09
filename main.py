import pygame
from pygame.locals import *
import time
import random

size = 30
# background_color = 5, 99, 22


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load(
            'resources/apple2.jpg').convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 31) * size
        self.y = random.randint(1, 17) * size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/snake_block.jpg').convert()
        self.x = [size]*length
        # y coordinate of starting position of snake block
        self.y = [size]*length
        self.direction = 'right'  # selecting a random direction for the snake to move

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()   # creating the game window
        self.display = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Bhashu's Game 🐍🍎")
        pygame.mixer.init()
        self.background_music()
        # setting the background color of the window
        self.display.fill((5, 99, 22))
        pygame.display.flip()
        self.snake = Snake(self.display, 1)
        self.snake.draw()
        self.apple = Apple(self.display)
        self.apple.draw()

    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def play(self):
        self.background_image()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/eating_apple.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        for i in range(1, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/game_over.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"

    def game_over(self):
        self.background_image()
        self.font = pygame.font.SysFont('arial', 20)
        line1 = self.font.render(
            f"Game Over. Your score is {self.snake.length}", True, (255, 255, 255))
        self.display.blit(line1, (360, 100))
        line2 = self.font.render(
            f"To replay, press ENTER. To exit, press ESC", True, (255, 255, 255))
        self.display.blit(line2, (290, 140))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        self.font = pygame.font.SysFont('arial', 20)
        self.score = self.font.render(
            f"Score: {self.snake.length}", True, (255, 255, 255))
        self.display.blit(self.score, (720, 10))

    def background_music(self):
        pygame.mixer.music.load("resources/background_music.mp3")
        pygame.mixer.music.play()

    def background_image(self):
        bg = pygame.image.load("resources/razor_background2.jpeg")
        bg = pygame.transform.scale(bg, (960, 540))
        self.display.blit(bg, (0, 0))

    def reset(self):
        self.snake = Snake(self.display, 1)
        self.apple = Apple(self.display)

    def run(self):
        open = True
        pause = False
        while open:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:   # enabling to close the window when 'esc' key is pressed
                        open = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                if event.type == pygame.QUIT:  # enabling to close window when 'x' is pressed
                    open = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.15)

    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
