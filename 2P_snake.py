from random import randint

from text import Text

import pygame

pygame.init()

SPEED = 9

WHITE = 255, 255, 255
BLACK = 50, 50, 50

DARK_RED = 255, 50, 50
DARK_GREEN = 0, 150, 50
PURPLE = 150, 0, 255
BLUE = 100, 130, 230 
YELLOW = 255, 200, 0
ORANGE = 255, 100, 0

GREEN = 0, 205, 50
RED = 255, 0, 0

BLOCK_SIZE = 20
WIDTH = 1000
HEIGHT = 900

RIGHT =  1,  0
LEFT  = -1,  0
UP    =  0, -1
DOWN  =  0,  1


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, color):
        rect = (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE,
                BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, color, rect)


class Snake:
    start_size = 10
    
    def __init__(self, pattern, y):
        self.direction = RIGHT
        self.pattern = pattern
        self.blocks = []
        self.moves = 0
        
        for i in range(Snake.start_size):
            block = Block(i + 3, y)
            self.blocks.append(block)

    def get_score(self):
        return len(self.blocks) - Snake.start_size

    def render(self):
        for i, block in enumerate(self.blocks):
            block.render(index(self.pattern, i))

    def move(self, grow, i):
        global game_over, score_text
        
        x, y = (self.blocks[-1].x + self.direction[0],
                self.blocks[-1].y + self.direction[1])

        snake = snake1 if i == snake2 else snake2
        for block in snake.blocks:
            if block.x >= WIDTH // BLOCK_SIZE or block.x < 0:
                game_over = True  
            if block.y >= HEIGHT // BLOCK_SIZE or block.y < 0:
                game_over = True   
            if x == block.x and y == block.y:
                game_over = True
        
        self.blocks.append(Block(x, y))

        if not grow:
            del self.blocks[0]

    def change_direction(self, direction):
        new_pos = (self.blocks[-1].x + direction[0],
                   self.blocks[-1].y + direction[1])

        block = self.blocks[-2]
        if new_pos[0] == block.x and new_pos[1] == block.y:
            return
        
        self.direction = direction


class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self):
        rect = (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE,
                BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, GREEN, rect)


def index(L, i):
    return L[i % len(L)]


def get_highscore():
    with open('highscore.txt') as file:
        score = file.read()
    
    if score == '':
        score = '0'
    
    return score


def set_highscore(score):
    with open('highscore.txt', 'w+') as file:
        file.write(str(score))


def get_rand_pos():
    return [randint(0, WIDTH // BLOCK_SIZE - 1),
            randint(0, WIDTH // BLOCK_SIZE - 1)]


def pos_exists(pos):
    for pellet in pellets:
        if pellet.x == pos[0] and pellet.y == pos[1]:
            return True
    return False


def find_pellet_pos():
    pos = get_rand_pos()
    while pos_exists(pos):
        pos = get_rand_pos()
    return pos


pygame.display.set_caption('Snake 2')
screen = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()

font = pygame.font.Font('assets/8bitFontBold.ttf', 34)
large_font = pygame.font.Font('assets/8bitFontBold.ttf', 54)

game_over_text = Text('GAME OVER!', large_font, (WIDTH // 2, HEIGHT // 2), center=True, color=RED)
play_again_text = Text('Press SPACEBAR to play again.', font, (WIDTH // 2, HEIGHT // 2 + 60), center=True, color=BLACK)

pygame.mixer.music.load('assets/sonic_attack.wav')
pygame.mixer.music.play(-1)

controls1 = {
    pygame.K_RIGHT: RIGHT,
    pygame.K_LEFT: LEFT,
    pygame.K_DOWN: DOWN,
    pygame.K_UP: UP,
}

controls2 = {
    pygame.K_d: RIGHT,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_w: UP
}

pellets = []

foo = 200
for i in range(foo):
    pos = find_pellet_pos()
    pellets.append(Pellet(pos[0], pos[1]))

snake1 = Snake([RED, ORANGE, YELLOW], 5)
snake2 = Snake([DARK_GREEN, BLUE, PURPLE], HEIGHT//BLOCK_SIZE-5)

frame = 0

game_over = False

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                snake1.__init__([RED, ORANGE, YELLOW], 5)
                snake2.__init__([DARK_GREEN, BLUE, PURPLE], HEIGHT//BLOCK_SIZE-5)
                pellets = []
                for i in range(foo):
                    pos = find_pellet_pos()
                    pellets.append(Pellet(pos[0], pos[1]))
            
            if event.key in controls1:
                snake1.change_direction(controls1[event.key])

            if event.key in controls2:
                snake2.change_direction(controls2[event.key])

    screen.fill(WHITE)

    if game_over:
        game_over_text.render(screen)
        play_again_text.render(screen)
    
    if not game_over:
        grow = False
        for pellet in pellets:
            pellet.render()

            for snake in [snake1,snake2]:
                block = snake.blocks[-1] 
                if pellet.x == block.x and pellet.y == block.y:
                    grow = True
                    pellets.remove(pellet)

        for snake in [snake1,snake2]:
            snake.render()
            snake.move(grow, snake)

        if frame >= 3:
            frame = 0
            pos = find_pellet_pos()
            pellets.append(Pellet(pos[0], pos[1]))
    
        frame += 1
    
    pygame.display.update()
    
    clock.tick(SPEED)

pygame.quit()
