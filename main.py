import pygame
import random
import os

pygame.mixer.init()

pygame.init()


#color
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
purple=(128,0,128)
green=(0,255,0)
grey=(128,128,128)

#create window
screen_width=900
screen_height=500
gamewindow=pygame.display.set_mode((screen_width,screen_height))

#create background
screen=pygame.image.load("mid.jpeg")
screen=pygame.transform.scale(screen,(screen_width,screen_height)).convert_alpha()

screen1=pygame.image.load("front.jpg")
screen1=pygame.transform.scale(screen1,(screen_width,screen_height)).convert_alpha()

screen2=pygame.image.load("end.jpg")
screen2=pygame.transform.scale(screen2,(screen_width,screen_height)).convert_alpha()



#game title
pygame.display.set_caption("snakeBoom")
pygame.display.update()


clock=pygame.time.Clock()
font1=pygame.font.Font("LoveYaLikeASister.ttf",55)
font2=pygame.font.Font("last.ttf",44)

def text_screen(text,color,x,y):
    screen_text=font1.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])

def text_screen2(text, color, x, y):
    screen_text2 = font2.render(text, True, color)
    gamewindow.blit(screen_text2, [x, y])

def plot_snake(gamewindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow,color,[x,y,snake_size,snake_size])


def welcome():
    exit_game=False
    while not exit_game:
        gamewindow.fill(purple)
        gamewindow.blit(screen1, (0, 0))
        #text_screen("Welcome To Saap Wala Khel",black,200,200)
        #text_screen("Press Space Bar To Khela Hobe",black,180,240)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            pygame.mixer.music.load("go.mp3")
            pygame.mixer.music.play()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.load("bgm.mp3")
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()

#game loop
def gameloop():

#game specific variable
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 60
    velocity_x = 0
    velocity_y = 0
    score = 0
    init_velocity = 1
    snake_size = 20
    fps = 60

    # check if high score file doest exist
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                 f.write(str(hiscore))
            gamewindow.fill(white)
            gamewindow.blit(screen2, (0, 0))
            #text_screen2("Game Over! Press Enter To Continue" ,red,100,230)
            text_screen2("HighScore: "+str(hiscore), white, 260, 370)
            text_screen2("score: " + str(score), white, 350, 410)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key==pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                    if event.key==pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_q:
                        score+=50
                    if event.key == pygame.K_w:
                        snk_length+=5
                        init_velocity += 1 / 4

            snake_x=snake_x + velocity_x
            snake_y=snake_y + velocity_y

            if abs(snake_x-food_x)<7 and abs(snake_y-food_y)<7:
                    score +=10
                    init_velocity+=1/4

                    food_x = random.randint(40, screen_width / 2)
                    food_y = random.randint(40, screen_height / 2)


                    snk_length+=5

            if score > int(hiscore):
                hiscore = score

            gamewindow.fill(white)
            gamewindow.blit(screen, (0, 0))
            text_screen("score: "+str(score),grey,5,5)
            pygame.draw.rect(gamewindow,red, [food_x, food_y, snake_size, snake_size])

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list)>snk_length:
               del snk_list[0]

            if head in snk_list[:-1]:
                game_over= True
                pygame.mixer.music.load("bomb.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load("bomb.mp3")
                pygame.mixer.music.play()

            plot_snake(gamewindow, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()