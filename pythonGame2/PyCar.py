import pygame
import random
from time import sleep

window_width = 480
window_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (150, 150 ,150)
red = (255, 0, 0)

class Car:
    image_car = ['RacingCar01.png', 'RacingCar02.png', 'RacingCar03.png', 'RacingCar04.png', 'RacingCar05.png',
                'RacingCar06.png', 'RacingCar07.png', 'RacingCar08.png', 'RacingCar09.png', 'RacingCar10.png',
                'RacingCar11.png', 'RacingCar12.png', 'RacingCar13.png', 'RacingCar14.png', 'RacingCar15.png',
                'RacingCar16.png', 'RacingCar17.png', 'RacingCar18.png', 'RacingCar19.png', 'RacingCar20.png']

    def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        self.image = pygame.image.load(random.choice(self.image_car))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])
    
    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy
    
    def check_out_of_screen(self):
        if self.x + self.width > window_width or self.x < 0:
            self.x -= self.dx

    def check_crash(self, car):
        if (self.x + self.width > car.x) and (self.x < car.x + car.width) and (self.y < car.y + car.height) and (self.y + self.height > car.y):
            return True
        else:
            return False
    
def draw_main_menu():
    draw_x = (window_width / 2) - 200
    draw_y = (window_height / 2)
    image_intro = pygame.image.load('PyCar.png')
    screen.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("PyCar : Racing Car Game", True, black)
    screen.blit(text_title, [draw_x, draw_y])
    text_scroe = font_40.render("Score : " + str(score), True, white)
    screen.blit(text_scroe, [draw_x, draw_y + 70])
    text_start = font_30.render("Press Space Key to Start!", True, red)
    screen.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()

def draw_score():
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_scroe = font_30.render("Score : " + str(score), True, white)
    screen.blit(text_scroe, [15, 15])

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("PyCar : Racing Car Game")
    clock = pygame.time.Clock()

    pygame.mixer.music.load('race.wav')
    sound_crash = pygame.mixer.Sound('crash.wav')
    sound_engine = pygame.mixer.Sound('engine.wav')

    player = Car((window_width / 2), (window_height - 150), 0, 0)
    player.load_image()

    cars = []
    car_count = 3
    for i in range(car_count):
        x = random.randrange(0, window_width - 55)
        y = random.randrange(-150, -50)
        car = Car(x, y, 0 ,random.randint(5, 10))
        car.load_image()
        cars.append(car)

    lanes = []
    lane_width = 10
    lane_height = 80
    lane_magin = 20
    lane_count = 20
    lane_x = (window_width - lane_width) / 2
    lane_y = -10

    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_magin
    
    score = 0
    crash = True
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                game_on = False

            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0, window_width-cars[i].width)
                        cars[i].y = random.randrange(-150, -50)
                        cars[i].load_image()

                    player.load_image()
                    player.x = window_width / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(5)
                    pygame.mixer.music.play(-1) #ずっと再生

            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0

        screen.fill(gray)

        if not crash:
            for i in range(lane_count):
                pygame.draw.rect(screen, white, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10
                if lanes[i][1] > window_height:
                    lanes[i][1] = -40 - lane_height
            
            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            for i in range(car_count):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > window_height:
                    score += 10
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].x = random.randrange(0, window_width - cars[i].width)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].load_image()
            
            for i in range(car_count):
                if player.check_crash(cars[i]):
                    crash = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break
                    
            draw_score()
            pygame.display.flip()

        else:
            draw_main_menu()
        
        clock.tick(60)
    
    pygame.quit()