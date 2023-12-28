import pygame, sys, random  #mengimport library pygame
from pygame.math import Vector2 #mengambil library vector

class SNAKE: #membuat ular
    def __init__(self):
        try:

            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
            self.direction = Vector2(0,0)
            self.new_block = False

            self.head_up = pygame.image.load('Graphics/Hatas.png').convert_alpha()
            self.head_down = pygame.image.load('Graphics/Hbawah.png').convert_alpha()
            self.head_right = pygame.image.load('Graphics/Hkanan.png').convert_alpha()
            self.head_left = pygame.image.load('Graphics/Hkiri.png').convert_alpha()

            self.tail_up = pygame.image.load('Graphics/Eatas.png').convert_alpha()
            self.tail_down = pygame.image.load('Graphics/Ebawah.png').convert_alpha()
            self.tail_right = pygame.image.load('Graphics/Ekanan.png').convert_alpha()
            self.tail_left = pygame.image.load('Graphics/Ekiri.png').convert_alpha()

            self.body_vertical = pygame.image.load('Graphics/Bvertikal.png').convert_alpha()
            self.body_horizontal = pygame.image.load('Graphics/Bhorizontal.png').convert_alpha()

            self.body_tr = pygame.image.load('Graphics/Katas.png').convert_alpha()
            self.body_tl = pygame.image.load('Graphics/kiriatas.png').convert_alpha()
            self.body_br = pygame.image.load('Graphics/Kbawah.png').convert_alpha()
            self.body_bl = pygame.image.load('Graphics/kiribawah.png').convert_alpha()
            self.crunch_sound = pygame.mixer.Sound('Sound/crunch.mp3')

        except FileNotFoundError as e:
            print(f"File not found: {e}")
            sys.exit()

    def draw_snake(self): #menggambar ular
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                 screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self): #membuat pergerakan ular
        if self.new_block == True:
             body_copy = self.body[:]
             body_copy.insert(0,body_copy[0] + self.direction)
             self.body = body_copy[:]
             self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self): #menambahkan badan ular
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT: #membuat object buah
    def __init__(self):
        self.randomize()

    def draw_fruit(self):    #mengambar buah
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size) ,cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:  #membuat logika permainan ular   
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self): 
        self.draw_grass()   
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:   
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (240, 210, 30) #warna rumput tampilan
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                 for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 40)
        score_y = int(cell_size * cell_number - 30)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width,apple_rect.height)

        pygame.draw.rect(screen,(240, 210, 30),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()   #mendefinikan modul pygame
cell_size = 20  #membuat tampilan pengguna
cell_number = 30
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha() # menampilkan
game_font = pygame.font.Font('Font/kenneyFuture.ttf', 25) #menampilkan score


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:    #membuat loop untuk user bisa berinteraksi seperti tekan tombol
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)        
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((255, 221, 51))  #untuk mengatur rgb tampilan latar belakang     
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)