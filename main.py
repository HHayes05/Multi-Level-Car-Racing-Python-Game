import pygame
import time
import math
import pandas as pd
from utility import scale_image, blit_rotate_center, blit_text_center


def main():
    pygame.font.init()
    menu=pygame.image.load("imgs/menu1.png")
    track = scale_image(pygame.image.load("imgs/track3.png"), 0.5)
    grass = scale_image(pygame.image.load("imgs/grass.jpg"), 1.1)
    finish = scale_image(pygame.image.load("imgs/finish.png"), 1.0)
    finish_position = (710, 280)
    finish_mask = pygame.mask.from_surface(finish)
    greencar = scale_image(pygame.image.load("imgs/green-car.png"), 0.025)
    bluecar = scale_image(pygame.image.load("imgs/blue-car.png"), 0.025)
    yellowcar = scale_image(pygame.image.load("imgs/yellow-car.png"), 0.025)
    pinkcar = scale_image(pygame.image.load("imgs/pink-car.png"), 0.077)

    trackborder = scale_image(pygame.image.load("imgs/trackborder3.png"), 0.5)
    trackborder_mask = pygame.mask.from_surface(trackborder)

    trackborder_lvl2 = scale_image(pygame.image.load("imgs/trackborder2.png"), 0.5)
    track_lvl2 = scale_image(pygame.image.load("imgs/track2.png"), 0.5)
    trackborder_lvl2_mask = pygame.mask.from_surface(trackborder_lvl2)

    trackborder_lvl3 = scale_image(pygame.image.load("imgs/track-border.png"), 0.5)
    track_lvl3 = scale_image(pygame.image.load("imgs/track.png"), 0.5)
    trackborder_lvl3_mask = pygame.mask.from_surface(trackborder_lvl3)

    trackborder_lvl4 = scale_image(pygame.image.load("imgs/trackborder4.png"), 0.5)
    track_lvl4 = scale_image(pygame.image.load("imgs/track4.png"), 0.5)
    trackborder_lvl4_mask = pygame.mask.from_surface(trackborder_lvl4)

    splashscreen=("imgs/Splash.png")

    whitecar = scale_image(pygame.image.load("imgs/white-car.png"), 0.55)

    WIDTH, HEIGHT = track.get_width(), track.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("HAYES RACING")

    MAIN_FONT = pygame.font.SysFont('comicsand', 44)# font used
    FPS = 60
    PATH3 = [(736, 91), (640, 59), (545, 63), (494, 210), (424, 276), (320, 155),
             (255, 68), (128, 79), (48, 261), (112, 496), (491, 504), (744, 414), (726, 286)]

    PATH2 = [(736, 100), (110, 70), (70, 450), (300, 460), (390, 250), (520, 235), (590, 480), (720, 470), (720, 0)]

    PATH = [(736, 110), (150, 70), (130, 460), (720, 460), (720, 91)]

    PATH4 = [(736, 110), (150, 70), (70, 160), (150, 240), (470, 240), (560, 460), (730, 440), (710, 0)]


    class GameInfo:
        LEVELS = 4# amount of levels in our game

        def __init__(self, level=1): 
            self.level = level
            self.started = False
            self.level_start_time = 0
            self.init_level = level
            self.finished = False

            self.trackborder_imgs = [trackborder, trackborder_lvl2, trackborder_lvl3, track_lvl4]
            self.trackborder_masks = [trackborder_mask, trackborder_lvl2_mask, trackborder_lvl3_mask, trackborder_lvl4_mask]
            self.tracks = [track, track_lvl2, track_lvl3, track_lvl4]
            self.paths = [PATH, PATH2, PATH3, PATH4]
            self.best_time = None

            self.new_best()

        def next_level(self, computer_car):# function for what happens when we beat a level and go to a next level
            self.level += 1
            if self.game_finished():
                self.finished = True
                self.level -= 1
            self.update_best()
            self.new_best()
            self.started = False
            try:
                computer_car.path = self.paths[self.level - 1]
            except:
                pass

        def reset(self, computer_car):# this resets our variables such as path when you go to a new level.
            self.level = self.init_level
            self.started = False
            self.level_start_time = 0
            computer_car.path = self.paths[self.level - 1]

            self.new_best()

        def game_finished(self):# when game finished
            return self.level > self.LEVELS

        def start_level(self):
            self.started = True
            self.level_start_time = time.time()

        def get_level_time(self):
            if not self.started:
                return 0# when level starts timer starts aswell
            return round(time.time() - self.level_start_time)

        def new_best(self):# pd is what stores our data for the best time
            df = pd.read_csv("score.csv")
            self.best_time = df["score"][self.level - 1]

        def update_best(self):# updated best score if we are faster than current best time.
            dfw = pd.read_csv("score.csv")

            if self.get_level_time() < int(dfw["score"][self.level - 2]):
                dfw["score"][self.level - 2] = self.get_level_time()

                dfw.to_csv("score.csv", index=False)


    class AbstractCar:# this class focuses on our rotation and velocity of our car.
        def __init__(self, max_vel, rotation_vel):
            self.img = self.IMG
            self.max_vel = max_vel
            self.vel = 0#these variables set up our rotation, speed and starting position
            self.rotation_vel = rotation_vel
            self.angle = 0
            self.x, self.y = self.START_POS
            self.acceleration = 0.1

        def rotate(self, left=False, right=False):# this is our code for turning right and left.
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

        def draw(self, win):
            blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

        def move_forward(self):# code for car moving fowrard
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.move()

        def move_backward(self):# code for car moving backward
            self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
            self.move()

        def move(self):# angle for our car moving
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical
            self.x -= horizontal

        def collide(self, mask, x=0, y=0):# this code is for when our car collides with the border. It bumps off the border when it happend.
            car_mask = pygame.mask.from_surface(self.img)
            offset = (int(self.x - x), int(self.y - y))
            poi = mask.overlap(car_mask, offset)
            return poi

        def reset(self):# this is a reset function for our car
            self.x, self.y = self.START_POS
            self.angle = 0
            self.vel = 0
            self.current_point = 0
            self.vel = self.max_vel


    class PlayerCar(AbstractCar):#class for the players car
        IMG = greencar# car we use
        START_POS = (730, 230)# start position for our car

        def reduce_speed(self):# this is what happens when re reduce our speed.
            self.vel = max(self.vel - self.acceleration / 2, 0)
            self.move()

        def bounce(self):# this is the code for when we hit the wall the car bounces and doesnt just stop
            self.vel = -self.vel
            self.move()


    class ComputerCar(AbstractCar):# class for our computer car
        IMG = pinkcar# the car we use is the pink car
        START_POS = (760, 230)# start position for pinc car

        def __init__(self, max_vel, rotation_vel, level, path=[]):
            super().__init__(max_vel, rotation_vel)#these lines deal with the path and velocity and rotation for computer car
            self.path = path
            self.current_point = 0
            self.vel = max_vel + (level - 1) * 0.25
            self.i_vel = self.vel

        def draw_points(self, win):# this was code i used for drawing points when creating path
            for point in self.path:
                pygame.draw.circle(win, (255, 0, 0), point, 5)

        def draw(self, win):# draws things onto screen
            super().draw(win)


        def calculate_angle(self):# calculates angle for our rotation in retrospect to points
            target_x, target_y = self.path[self.current_point]
            x_diff = target_x - self.x
            y_diff = target_y - self.y

            if y_diff == 0:
                desired_radian_angle = math.pi / 2
            else:
                desired_radian_angle = math.atan(x_diff / y_diff)

            if target_y > self.y:
                desired_radian_angle += math.pi

            difference_in_angle = self.angle - math.degrees(desired_radian_angle)
            if difference_in_angle >= 180:
                difference_in_angle -= 360

            if difference_in_angle > 0:
                self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            else:
                self.angle += min(self.rotation_vel, abs(difference_in_angle))

        def update_path_point(self):# This updates our path in our code
            target = self.path[self.current_point]
            rect = pygame.Rect(
                self.x, self.y, self.img.get_width(), self.img.get_height())
            if rect.collidepoint(*target):
                self.current_point += 1

        def move(self):#moves the car
            if self.current_point >= len(self.path):
                return

            self.calculate_angle()
            self.update_path_point()
            super().move()

        def next_level(self, level):# when next level comes we reset our velocity and position
            self.reset()
            self.vel = self.max_vel + (level - 1) * 0.25
            self.current_point = 0

        def reset(self):# this resets the self car and currrent angles
            self.x, self.y = self.START_POS
            self.angle = 0
            self.current_point = 0
            self.vel = self.i_vel


    def draw(win, images, player_car, computer_car, game_info):# this draws what we see on our screen
        for img, pos in images:
            win.blit(img, pos)

        level_text = MAIN_FONT.render(# this shows the level we are on
            f"Level {game_info.level}", 1, (255, 0, 0))
        win.blit(level_text, (3, HEIGHT - level_text.get_height() - 70))

        time_text = MAIN_FONT.render(# this shows our time
            f"Time: {game_info.get_level_time()}s", 1, (255, 0, 0))
        win.blit(time_text, (3, HEIGHT - time_text.get_height() - 40))

        vel_text = MAIN_FONT.render(# this shows our velocity
            f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 0, 0))
        win.blit(vel_text, (3, HEIGHT - vel_text.get_height() - 10))

        try:
            best_time_text = MAIN_FONT.render(# this shows our best time
                f"Best Time: {game_info.best_time}s", 1, (255, 0, 0))
            win.blit(best_time_text, (190, HEIGHT - best_time_text.get_height() - 10))

        except:
            pass

        player_car.draw(win)
        computer_car.draw(win)# draws computer car on screen


    def move_player(player_car):# this function represent what to move key when pressed
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:# if a is pressed car turns left
            player_car.rotate(left=True)
        if keys[pygame.K_d]:# if d is pressed code turns left
            player_car.rotate(right=True)
        if keys[pygame.K_w]:# if w is pressed code goes fowrard
            moved = True
            player_car.move_forward()
        if keys[pygame.K_s]:# if s is pressed
            moved = True
            player_car.move_backward()

        if not moved:# if nothing is pressed car goes backwards
            player_car.reduce_speed()


    def handle_collision(player_car, computer_car, game_info):
        if player_car.collide(game_info.trackborder_masks[game_info.level - 1]) != None:
            player_car.bounce()

        computer_finish_poi_collide = computer_car.collide(
            finish_mask, *finish_position)

        if computer_finish_poi_collide != None:# if cpu car beats ur car the game shows that u lost
            blit_text_center(WIN, MAIN_FONT, "You lost. Back to level " + str(game_info.init_level))
            pygame.display.update()
            pygame.time.wait(1200)
            game_info.reset(computer_car)
            player_car.reset()
            computer_car.reset()

        player_finish_poi_collide = player_car.collide(finish_mask, *finish_position)
        if player_finish_poi_collide != None:# if you back into finish line car bounces
            if player_finish_poi_collide[1] == 0:
                player_car.bounce()
            else:
                game_info.next_level(computer_car)
                player_car.reset()
                computer_car.next_level(game_info.level)


    class Button:
        def __init__(self, x, y, width, height, color, text, outline=None, r=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height# these 10 or so lines represent the functions size text an
            self.color = color
            self.text = text
            self.text_surf = MAIN_FONT.render(self.text, 1, (0, 0, 0))
            self.outline = outline
            self.r = r

            self.rect = pygame.Rect(x, y, width, height)
            self.outline_width = 3

        def draw(self, surface):
            if self.r:
                pygame.draw.rect(surface, self.color, self.rect, 0, self.r)
                if self.outline:
                    pygame.draw.rect(surface, self.outline, self.rect, self.outline_width, self.r)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
                if self.outline:
                    pygame.draw.rect(surface, self.outline, self.rect, self.outline_width)

            surface.blit(self.text_surf, (self.x + self.width / 2 - self.text_surf.get_width() / 2,
                                          self.y + self.height / 2 - self.text_surf.get_height() / 2))

        def click(self):# this lines of codes show what happens when you click screen in code
            m = pygame.mouse.get_pos()
            if self.rect.collidepoint(m):
                return True

            return False


    class Text:# this code represrnts the font of the code we used
        def __init__(self, x, y, text):
            self.x = x
            self.y = y
            self.text = text
            self.text_surf = MAIN_FONT.render(self.text, 1, (0, 0, 0))

        def draw(self):
            WIN.blit(self.text_surf, (self.x, self.y))


    def main(level):# this shows the clock
        run = True
        clock = pygame.time.Clock()# code for clock

        # not used
        images = [(grass, (0, 0)),# code for grass and finish position and where they will be
                  (finish, finish_position)]

        game_info = GameInfo(level)
        player_car = PlayerCar(3, 4)# this is the pseed and velocity of our player car
        computer_car = ComputerCar(2.2, 4, game_info.level, game_info.paths[game_info.level - 1])
        # this is our speed and velocity for our computer car
        while run:
            clock.tick(FPS)

            draw(WIN, [(grass, (0, 0)), (game_info.trackborder_imgs[game_info.level - 1], (0, 0)),# this code is for when you go to new level all the images
                                    # update
                       (game_info.tracks[game_info.level - 1], (0, 0)), (finish, finish_position)], player_car,
                 computer_car, game_info)
            pygame.display.update()# updates display

            while not game_info.started:
                blit_text_center(# this is the text that appears before the game starts
                    WIN, MAIN_FONT, f"You are the green car. Press any key to start level {game_info.level}")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break
                    if event.type == pygame.KEYDOWN:# when user presses escape it goes back to main menu
                        if event.key == pygame.K_ESCAPE:
                            return main_menu()

                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()

            for event in pygame.event.get():#this is similar to previos functuon
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:# if user presses escape u return to main menu
                        return main_menu()

            move_player(player_car)# this makes it so the car can move
            computer_car.move()# needed so computer car can move

            handle_collision(player_car, computer_car, game_info)#code that initiates collisions

            if game_info.finished:# when game is won
                blit_text_center(WIN, MAIN_FONT, "Game Over. You won the game!")# this message appears
                pygame.display.update()
                pygame.time.wait(2200)# waits this long so message can be read
                return main_menu()  # going back to main menu




    def main_menu():# this is the code for our meny
        run = True
        clock = pygame.time.Clock()


        BUTTON_WIDTH = 170# button height and width
        BUTTON_HEIGHT = 50

        lvl1 = Button(WIDTH / 2 - BUTTON_WIDTH / 2, 120, BUTTON_WIDTH, BUTTON_HEIGHT, (200, 0, 0), "Level 1", (0, 0, 0))# the button for lvl 1
        lvl2 = Button(WIDTH / 2 - BUTTON_WIDTH / 2, lvl1.y + BUTTON_HEIGHT / 4 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,# button for lvl 2
                      (200, 0, 0), "Level 2", (0, 0, 0))
        lvl3 = Button(WIDTH / 2 - BUTTON_WIDTH / 2, lvl2.y + BUTTON_HEIGHT / 4 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,# button for lvl 3
                      (200, 0, 0), "Level 3", (0, 0, 0))
        lvl4 = Button(WIDTH / 2 - BUTTON_WIDTH / 2, lvl3.y + BUTTON_HEIGHT / 4 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,# button for lvl 4
                      (200, 0, 0), "Level 4", (0, 0, 0))
        tutorial = Button(WIDTH / 2 - BUTTON_WIDTH / 2, lvl4.y + BUTTON_HEIGHT / 4 + BUTTON_HEIGHT, BUTTON_WIDTH,# tutorial button
                          BUTTON_HEIGHT, (200, 0, 0), "Tutorial", (0, 0, 0))

        heading = MAIN_FONT.render("HAYES RACING", 1, (0, 0, 0))# this is the heading in our main meny

        while run:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:# if user presses the red quit button the game quits and closes
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if lvl1.click():
                        return main(1)# if user clicks down the game starts
                    elif lvl2.click():
                        return main(2)
                    elif lvl3.click():
                        return main(3)
                    elif lvl4.click():
                        return main(4)
                    elif tutorial.click():
                        return tutorial_menu()

            WIN.fill((220, 14, 172))# the colour the window is


            WIN.blit(heading, (WIDTH / 2 - heading.get_width() / 2, 40))

            lvl1.draw(WIN)
            lvl2.draw(WIN)# draws the buttons for each level
            lvl3.draw(WIN)
            lvl4.draw(WIN)
            tutorial.draw(WIN)

            pygame.display.update()


    def tutorial_menu():# this represents our tutorial
        clock = pygame.time.Clock()

        popup = pygame.Surface((WIDTH // 2, HEIGHT // 2))# height for our pop up

        x = Button(popup.get_width() - 50, 10, 40, 40, (200, 30, 30), "x", (0, 0, 0), 10)# x at top of tutorial menu

        try_it = Button((WIDTH / 2) / 2 - 100, (HEIGHT / 2) - 70, 200, 50, (30, 200, 30), "Try It!", (0, 0, 0), 10)# try is button

        message1 = MAIN_FONT.render("Press 'W' to accelerate", 1, (0, 0, 0))
        message2 = MAIN_FONT.render("Press 'S' to drive back", 1, (0, 0, 0))
# these are all the messages that appear in tutorial
        message3 = MAIN_FONT.render("Press 'D' to go right", 1, (0, 0, 0))
        message4=MAIN_FONT.render("Press 'A' to go left",1,(0,0,0))
        message5=MAIN_FONT.render("Use ESC to return to menu",1,(0,0,0))
        message6=MAIN_FONT.render("Beat the PINK car to win!",1,(214, 17, 178))



        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    m = pygame.mouse.get_pos()
                    x_rect = pygame.Rect(WIDTH / 4 + x.x, HEIGHT / 4 + x.y, x.width, x.height)
                    try_it_rect = pygame.Rect(WIDTH / 4 + try_it.x, HEIGHT / 4 + try_it.y, try_it.width, try_it.height)# try it button in depth code

                    if x_rect.collidepoint(m):# this returns to the main menu if u press the x button
                        return main_menu()
                    elif try_it_rect.collidepoint(m):
                        return main(1)

                elif event.type == pygame.KEYDOWN:# if u press x return to main menu
                    return main_menu()

            popup.fill((150, 150, 150))
            popup.blit(message1, (10, 10))
            popup.blit(message2, (10, 41))# this is the positions that the message fills
            popup.blit(message3, (10, 72))
            popup.blit(message4, (10, 103))
            popup.blit(message5, (10, 134))
            popup.blit(message6, (10, 165))



            x.draw(popup)# draws the x on to menu
            try_it.draw(popup)# draws try it on to mento

            WIN.blit(popup, (WIDTH / 4, HEIGHT / 4))

            pygame.display.update()


    main_menu()

    pygame.quit()
