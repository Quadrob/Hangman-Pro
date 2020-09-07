# An extreme Hangman game 
#
# Author: Robert Zeelie
#
# version: 1.0.0

import pygame, os, random, sys, math
from nltk.corpus import words




# a function to draw to window
#---------------------------------------------------------------------------------------------------------------------------
def draw():
    gameWindow.fill(WHITE)  # fill window

    # draw version info
    version = ("Robert Zeelie | V: 1.0.0")
    versionText = INFOFONT.render(version, 1, BLACK)
    gameWindow.blit(versionText, (5, 5))

    # draw the word to be guessed
    displayWord = ""
    for letter in secretWord:
        if letter in guessed:  # check if the letters guessed match a letter in the desired word
            displayWord += (letter + " ")
        else:
            displayWord += "_ "#if not leave blank
            
    # render word and display
    wordText = WORDFONT.render(displayWord, 1, BLACK)
    gameWindow.blit(wordText, (300, 210))

    # check if game over
    userLose = False
    WON = True
    for letter in secretWord:
        if letter not in guessed:#if user hasnt guessed all the words
            WON = False
            # if there are chances left draw everything
            if 6 - hangmanStatus >= 1:
                        # draw buttons
                for letter in letters:
                    x, y, character, charVisible = letter
                    if charVisible:
                        pygame.draw.circle(gameWindow, BLACK, (x, y), RADIUS, 3)#draw circle
                        text = LETTERFONT.render(character, 1, BLACK)
                        gameWindow.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))#add text
                        
                # display text
                chancesLeft = ("You have " + str(6 - hangmanStatus) + " chances left!")
                chancesLeftText = NORMALFONT.render(chancesLeft, 1, BLACK)
                gameWindow.blit(chancesLeftText, (360, 30))
                
            else:#else if no more chanses game lost
                userLose = True

    # if user loses perform action
    if userLose:
        # make buttons invisible
        for letter in letters:
            letter[3] = False
        # display text
        gameOver = ("You Lose!")
        gameOverText = NORMALFONT.render(gameOver, 1, RED)
        gameWindow.blit(gameOverText, (460, 5))
        answerWord = ("The answer was: " + secretWord)
        answerWordText = NORMALFONT.render(answerWord, 1, BLACK)
        gameWindow.blit(answerWordText, (250, 60))
        
    #if user won perform action
    if WON:
        # make buttons invisible
        for letter in letters:
            letter[3] = False
        #draw text
        gameOver = ("You Saved Him This Time...")
        gameOverText = NORMALFONT.render(gameOver, 1, GREEN)
        gameWindow.blit(gameOverText, (360, 50))

    gameWindow.blit(images[hangmanStatus], (50, 150))  # draw hangman image

    pygame.display.update()  # update window

#---------------------------------------------------------------------------------------------------------------------------



#Game variables


# set game window properties
pygame.init()
WIDTH, HEIGHT = 1200, 600
filepath = os.path.dirname(__file__)  # get file directory
# join to image name to get image path
logo = pygame.image.load(os.path.join(filepath, "icon.jpg"))
pygame.display.set_icon(logo)
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Pro")


# get a list of words using nltk and select one
wordList = words.words()
randWord = random.choice(wordList)
secretWord = randWord.upper()
#uncomment the line below to test program
#secretWord = "TEST"


# Game fonts
LETTERFONT = pygame.font.SysFont('Comic Sans MS', 34)
WORDFONT = pygame.font.SysFont('Comic Sans MS', 60)
NORMALFONT = pygame.font.SysFont('Comic Sans MS', 40)
INFOFONT = pygame.font.SysFont('Impact', 16)


# load game images of the stick man
images = []
for i in range(7):
    image = pygame.image.load(os.path.join(
        filepath, ("hangman" + str(i) + ".png")))
    images.append(image)


# set max frames per second
FPS = 60
clock = pygame.time.Clock()


# game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# variables
hangmanStatus = 0
guessed = []


# button variables
RADIUS = 34
GAP = 20
letters = []
# start postion coordinates for buttons
startPosX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
startPosY = 440
A = 65  # letter index
visible = True
# loop to calculate the postion of each button
for i in range(26):
    x = startPosX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startPosY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), visible])


# begin game loop
runGame = True
while runGame:
    clock.tick(FPS)
    draw()  # call draw method

    # loop to check for actions performed by user
    for event in pygame.event.get():

        # if the exit (X) on the window is clicked
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        # mouse click event listener
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClickX, mouseClickY = pygame.mouse.get_pos()  # get mouse click coordinates
            for letter in letters:
                # go through button letters for its information
                x, y, character, charVisible = letter
                if charVisible:  # if letter visible calculate distance from button radious
                    distance = math.sqrt(
                        (x - mouseClickX)**2 + (y - mouseClickY)**2)
                    if distance < RADIUS:  # if within radious perform actions
                        letter[3] = False  # make invisible
                        guessed.append(character)  # add to guessed letters
                        if character not in secretWord:  # if not in the disired word perform action
                            hangmanStatus += 1

#exit game
pygame.quit()
sys.exit()
