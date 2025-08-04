import pygame, sys
from pygame.math import Vector2
import random

class Snake:
    def __init__(self):
        self.body = [Vector2(4,9),Vector2(5,9),Vector2(6,9)]
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_top_right = pygame.image.load('Graphics/body_topright.png').convert_alpha()
        self.body_top_left = pygame.image.load('Graphics/body_topleft.png').convert_alpha()
        self.body_bottom_right = pygame.image.load('Graphics/body_bottomright.png').convert_alpha()
        self.body_bottom_left = pygame.image.load('Graphics/body_bottomleft.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.direction = Vector2(0,0)
        self.score = 0
    
    def update_tail_graphics(self):
        tail_relation = self.body[1] - self.body[0]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def update_head_graphics(self):
        head_relation = self.body[-2] - self.body[-1]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if index == len(self.body) - 1:
                screen.blit(self.head, snake_rect)
            elif index == 0:
                screen.blit(self.tail, snake_rect)
            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if next_block.x == previous_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif next_block.y == previous_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                elif (previous_block.y == -1 and next_block.x == -1) or (previous_block.x == -1 and next_block.y == -1):
                    screen.blit(self.body_top_left, snake_rect)
                elif (next_block.y == -1 and previous_block.x == 1) or (next_block.x == 1 and previous_block.y == -1):
                    screen.blit(self.body_top_right, snake_rect)
                elif (next_block.x == -1 and previous_block.y == 1) or (next_block.y == 1 and previous_block.x == -1):
                    screen.blit(self.body_bottom_left, snake_rect)
                else:
                    screen.blit(self.body_bottom_right, snake_rect)
                

    def move_snake(self):
        if self.direction != Vector2(0,0):
            new_head = self.body[-1] + self.direction
            self.body.append(new_head)
            self.body.pop(0)
        
    
    def add_block(self):
        new_tail = self.body[0] + (self.body[0] - self.body[1])
        self.body.insert(0, new_tail)

class Fruit:        
    def __init__(self):
        self.x = random.randint(0,cell_number - 1) 
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
    
    def update_fruit(self):
        self.x = random.randint(0,cell_number - 1) 
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move_snake()
        self.eat_fruit()
    
    def draw_elements(self):
        self.draw_board()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def eat_fruit(self):
        if self.fruit.pos == self.snake.body[-1]:
            self.fruit.update_fruit()
            self.snake.add_block()
            self.snake.score += 1
        
        for block in self.snake.body[0:-1]:
            if block == self.fruit.pos:
                self.fruit.update_fruit()
        
    def draw_board(self):
        grass_color = (167,208,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def reset_game(self):
        self.snake.body = [Vector2(4,9),Vector2(5,9),Vector2(6,9)]
        self.snake.direction = Vector2(0,0)
        self.fruit.update_fruit()
        self.snake.score = 0
    
    def game_over(self):
        head = self.snake.body[-1]
        if head.x < 0 or head.x >= cell_number or head.y >= cell_number or head.y < 0:
            self.reset_game()
        if head in self.snake.body[:-1]:
            self.reset_game()
    def draw_score(self):
        frame_x = cell_size * cell_number - 100
        frame_y = cell_size * cell_number - 55
        frame_surface = pygame.Surface((100,50), pygame.SRCALPHA)
        frame_surface.fill((100, 100, 100, 150))
        screen.blit(frame_surface, (frame_x, frame_y))
        score_surface = my_font.render(f"x{str(self.snake.score)}", True, (56, 74, 12))
        score_rect = score_surface.get_rect(center =(cell_size*cell_number - 30,cell_size*cell_number - 30))
        screen.blit(score_surface,score_rect)
        screen.blit(apple,(cell_size*cell_number - 88,cell_size*cell_number - 45))

cell_size = 30
cell_number = 20
pygame.init()
screen = pygame.display.set_mode((cell_size* cell_number,cell_size* cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))
my_font = pygame.font.Font('Fonts/Sticky Chicken.ttf', 25)

main_game = Main()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,125)
running = True
pygame.font.init()

game_started = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_started:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        main_game.snake.direction = Vector2(0,-1)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        main_game.snake.direction = Vector2(0,1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        main_game.snake.direction = Vector2(1,0)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        main_game.snake.direction = Vector2(-1,0)
                    game_started = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)

            if event.type == SCREEN_UPDATE:
                main_game.update()
                main_game.game_over()

    screen.fill((175,215,70))
    if not game_started:
        main_game.draw_board()
        message = "Press any arrow key to start"
        message_surface = my_font.render(message, True, (80, 80, 80))
        message_rect = message_surface.get_rect(center=(cell_size*cell_number/2, cell_size*cell_number/2))
        screen.blit(message_surface, message_rect)
    else:
        main_game.draw_elements()
        main_game.draw_score()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()