from main import *
from utility import scale_image, blit_rotate_center, blit_text_center
white = (255, 255, 255)# white car colour
green = (0, 255, 0)# green car colour of car

splashscreen = scale_image(pygame.image.load("imgs/Splash.png"), 0.72)# splash screen image
screen=pygame.display.set_mode((780,550))# size of screen


run= True


while run:# basic code for splash screen to run
    screen.blit(splashscreen,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:# if u click down the main code runs
            main()


    pygame.display.update()# pygame display updated.


