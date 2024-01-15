# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from os.path import exists

from game import Game

# define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)


# game instance
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init() # initialize pygame library

fpsClock = pygame.time.Clock()     # keep track of time

# set up window
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

# load sound
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
button_sound = pygame.mixer.Sound('./sound/button_click.mp3')

# keeping track if the game ended
Crashed = False


# creates a text surface to add to screen
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# draws the text on screen
def message_display(text, x, y, color=black, font_size=50):
    large_text = pygame.font.SysFont('comicsansms', font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)   # sets the text position
    screen.blit(text_surf, text_rect)   # draws the text on screen


# creates a button
def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()  # gets mouse position
    click = pygame.mouse.get_pressed()  # check whether mouse is clicked

    # if clicked inside the button area
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))    # display the active color of the button
        if click[0] == 1 and action != None:
            if parameter != None:   # pass the arguments if not none
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    # play button sound
    pygame.mixer.Sound.play(button_sound)

    pygame.quit()   # quit the program
    quit()


# executed if the sprite hits the wall
def crash():
    global Crashed

    pygame.mixer.music.pause() # pause music
    Crashed = True
    pygame.mixer.Sound.play(crash_sound) # play crasho sound
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)  # display crashed message
    time.sleep(1) # hold thread for 1 second


# indicating that the back button
def back_to_main_window():
    global back_button_pressed
    back_button_pressed = True

    # play button sound
    pygame.mixer.Sound.play(button_sound)

# display the scoreboard and the score texts
def draw_score_board():

    board_surf = pygame.Surface((game.settings.height, game.settings.width))

    screen.blit(board_surf, (0, 0)) # draws the board surface at position (0, 0)

    # draw score texts
    smallText = pygame.font.SysFont('comicsansms', 30)
    TextSurf, TextRect = text_objects("Top 5 Scores:", smallText)
    TextRect.center = (game.settings.width / 2 * 15, game.settings.height / 4 * 10)
    screen.blit(TextSurf, TextRect)

    top_5_scores = ['None'] * 5

    # draw score numbers
    for i in range(5):
        # read top 5 score from file
        if exists("score.txt"):
            with open('score.txt', 'r') as f:
                lines = list(map(int, f.read().splitlines()))   # convert each element to integer
                lines.sort(reverse=True)
                for j in range(5):
                    if j >= len(lines): break
                    top_5_scores[j] = lines[j]
            TextSurf, TextRect = text_objects(f'{str(i + 1)}. {top_5_scores[i]}', smallText)    # each score text
            # adjust position depending on the text
            if top_5_scores[i] == 'None':
                TextRect.center = (game.settings.width / 2 * 12, game.settings.height / 4 * 13 + (i + 1) * 35)
            else:
                TextRect.center = (game.settings.width / 2 * 10, game.settings.height / 4 * 13 + (i + 1) * 35)

        screen.blit(TextSurf, TextRect)

def display_scoreboard(fps=10):
    global back_button_pressed
    back_button_pressed = False

    # play button sound
    pygame.mixer.Sound.play(button_sound)

    # background_image = pygame.image.load('./images/Aatrox_7.jpg')
    background_image = pygame.image.load('./images/Syndra_4.jpg')

    while not back_button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(background_image, (-300, -80))
        draw_score_board()
        button("Back", 0, 0, 80, 40, green, bright_green, back_to_main_window)  # create a back button
        pygame.display.flip()   # updates screen

# main window interface
def initial_interface():
    intro = True

    # main bg music
    main_bg_music = pygame.mixer.music.load('./sound/campfire.mp3')
    pygame.mixer.music.play(-1) # play music indefinetely
    pygame.mixer.music.set_volume(0.2)

    # draw background image to main screen
    background_image = pygame.image.load('./images/bgimage.webp')
    while intro:
        global Crashed

        # if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if Crashed:
            # replay music if the game ended
            main_bg_music = pygame.mixer.music.load('./sound/campfire.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
            Crashed = False

        screen.fill(white)
        screen.blit(background_image, (-700, -175))
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button('Go!', 50, 240, 80, 40, green, bright_green, game_loop, 'human')
        button("Scoreboard", 155, 240, 120, 40, blue, bright_blue, display_scoreboard)
        button('Quit', 300, 240, 80, 40, red, bright_red, quitgame)

        pygame.display.flip()   # updates the screen
        pygame.time.Clock().tick(30)

# helps managing the 3 sprite skins
def skin_manager(skinName):
    global play_button_pressed
    play_button_pressed = True

    # play button sound
    pygame.mixer.Sound.play(button_sound)

    game.snake.setSkin(skinName)  # set skin for the sprite

# displays the settings window after clicking on Go!
def display_settings():
    global play_button_pressed
    global back_button_pressed
    play_button_pressed = False
    back_button_pressed = False

    background_image = pygame.image.load('./images/TwistedFate_3.jpg')
    while not play_button_pressed and not back_button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(background_image, (-300, -80))


        # pick a skin message
        message_display('Pick a skin:', game.settings.width / 2 * 15, game.settings.height / 4 * 15, black, 40)

        # draw a button for each skin
        button('Fire', game.settings.width / 2 * 10.5, game.settings.height / 4 * 21, 120, 45, red, bright_red, skin_manager, 'Fire')
        button('Wind', game.settings.width / 2 * 10.5, game.settings.height / 4 * 30, 120, 45, blue, bright_blue, skin_manager, 'Wind')
        button('Lightning', game.settings.width / 2 * 10.5, game.settings.height / 4 * 39, 120, 45, yellow, bright_yellow, skin_manager, 'Lightning')

        button("Back", 0, 0, 80, 40, green, bright_green, back_to_main_window)  # create a back button
        pygame.display.flip()   # updates screen

    # determine whether the play button or the back button was pressed
    return play_button_pressed

def save_score(score):
    # save score in a file
    with open('score.txt', 'a') as f:
        f.write(str(score) + '\n')


def display_time():
    # display timer in top right corner
    # increment timer by 1 every second

    global timer
    split_time = timer.split(':')
    h, m, s = map(int, split_time)

    # add 1 to the seconds
    if s + 1 == 60:
        s = 0
        m += 1
    else:
        s += 1

    if m == 60:
        m = 0
        h += 1

    if s < 10:
        s = f'0{s}'
    if m < 10:
        m = f'0{m}'
    if h < 10:
        h = f'0{h}'
    timer = f'{h}:{m}:{s}'

    message_display(timer, game.settings.width / 2 * 15, 10, white, 20)     # center the timer

# executed after choosing the skin
def game_loop(player, fps=10):
    # play button sound
    pygame.mixer.Sound.play(button_sound)

    condition = display_settings()
    if not condition: return    # if condition is falsed, it means that back button was pressed instead of play button

    game.restart_game()

    # background image of game
    background_image = pygame.image.load('./images/bgimage.webp')

    # variables for implementing timer, and game speed
    global increased_speed, prev_game_score, timer
    increased_speed, prev_game_score, timer = False, 0, '00:00:00'

    while not game.game_end():

        pygame.event.pump() # handle internal actions

        move = human_move() # integer representing direction
        # {0 : 'up',
        #   1 : 'down',
        #   2 : 'left',
        #   3 : 'right'}
        # fps = 30

        game.do_move(move)

        screen.fill(black)
        screen.blit(background_image, (-400, -250))

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        display_time()

        #another condition to prevent keep on increasing speed after score becomes a multiple of 10
        if prev_game_score != game.snake.score:
            increased_speed = False

        # increase the speed of the game as the score increases by 10 (multiple of 10)
        if game.snake.score != 0 and game.snake.score % 10 == 0 and not increased_speed:
            prev_game_score = game.snake.score
            increased_speed = True
            fps += 3

        pygame.display.flip()   # updates screen

        fpsClock.tick(fps)

    crash()
    save_score(game.snake.score)


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        # if oen of the arrow keys are pressed, or escape key is pressed
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
