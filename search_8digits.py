#this program will visulize the 8 digits game
import pygame
import random
import math
#size definitions
PADDING=5
GAME_SIZE=3
BLOCK_SIZE = 80
BUTTON_HEIGHT=40
BUTTON_WIDTH=80
MIDDLE_EDGE=PADDING*(GAME_SIZE+1)+BLOCK_SIZE*(GAME_SIZE)
WINDOW_HEIGHT=PADDING*(GAME_SIZE+1)+BLOCK_SIZE*(GAME_SIZE)
WINDOW_WIDTH=640
#layout definition
BUTTON_1_Y=100
#color definitions
BOARD_BG_COLOR=(125,125,125)
RIGHT_BG_CLOOR=(200,200,200)
SPACE_BLOCK_COLOR=(200,200,200)

#block object
class Block:
    def __init__(self, x, y, number, color,size=BLOCK_SIZE):
        self.x = x
        self.y = y
        self.number = number
        self.color = color
        self.size=size
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if(self.number!=0):
            font = pygame.font.SysFont('Arial', 40)
            text = font.render(str(self.number), True, (0,0,0))
            screen.blit(text, (self.x+self.size/2-text.get_width()/2, self.y+self.size/2-text.get_height()/2))
    def getNumber(self):
        return self.number
#button object
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(self.text, True, (0,0,0))
        screen.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))
    def isClicked(self, mouse):
        if mouse[0] > self.x and mouse[0] < self.x+self.width:
            if mouse[1] > self.y and mouse[1] < self.y+self.height:
                return True
        return False
    def getText(self):
        return self.text

#arrange block depending on the state
def arrange_block(block_list, state_list):
    for i in range(len(state_list)):
        block_list[state_list[i]].x = i%3*(BLOCK_SIZE+PADDING)+PADDING
        block_list[state_list[i]].y = math.floor(i/3)*(BLOCK_SIZE+PADDING)+PADDING

#generate random color
def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

#main function
def main():
    #init pygame window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    #init blocks
    block_list = []
    #create SPACE block
    block_list.append(Block(0,0,0,SPACE_BLOCK_COLOR))
    for i in range(1,GAME_SIZE**2):
        block_list.append(Block(PADDING+(i-1)%GAME_SIZE*(BLOCK_SIZE+PADDING),PADDING+math.floor((i-1)/GAME_SIZE)*(BLOCK_SIZE+PADDING), i, random_color()))
    arrange_block(block_list, [7, 5, 4, 1, 2, 6, 3, 8, 0])
    #init buttons
    button_list = []
    button_list.append(Button(MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH)/2,BUTTON_1_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"solve",(255,0,0)))
    button_list.append(Button(MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH)/2,BUTTON_1_Y+BUTTON_HEIGHT+PADDING,BUTTON_WIDTH,BUTTON_HEIGHT,"reset",(0,255,0)))

    #game loop
    running = True
    while running:
        #check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_list:
                    if button.isClicked(pygame.mouse.get_pos()):
                        if button.getText() == "solve":
                            #solve the game
                            pass
        #draw background
        screen.fill(BOARD_BG_COLOR)
        pygame.draw.rect(screen,RIGHT_BG_CLOOR, (MIDDLE_EDGE,0,640-MIDDLE_EDGE,WINDOW_HEIGHT))
        #draw blocks
        for block in block_list:
            block.display(screen)
        #draw buttons
        for button in button_list:
            button.display(screen)
        #update screen
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()