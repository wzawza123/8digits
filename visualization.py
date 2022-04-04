#this program will visulize the 8 digits game
import pygame
import random
import math
#size definitions
GAME_SIZE=3
BLOCK_SIZE = 80
PADDING_FRACTION=16
PADDING=BLOCK_SIZE//PADDING_FRACTION
BUTTON_HEIGHT=40
BUTTON_WIDTH=80
FPS=5
MIDDLE_EDGE=PADDING*(GAME_SIZE+1)+BLOCK_SIZE*(GAME_SIZE)
WINDOW_HEIGHT=PADDING*(GAME_SIZE+1)+BLOCK_SIZE*(GAME_SIZE)
WINDOW_WIDTH=640
#layout definition
BUTTON_1_Y=15
BUTTON_2_Y=BUTTON_1_Y+BUTTON_HEIGHT+PADDING
BUTTON_3_Y=BUTTON_2_Y+BUTTON_HEIGHT+PADDING
BUTTON_4_Y=BUTTON_3_Y+BUTTON_HEIGHT+PADDING

BUTTON_1_X=MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH*2-PADDING)/2
BUTTON_2_X=BUTTON_1_X+BUTTON_WIDTH+PADDING

TEXT_VIEW_X=MIDDLE_EDGE+50
TEXT_VIEW_Y=WINDOW_HEIGHT-50-PADDING

#color definitions
BOARD_BG_COLOR=(125,125,125)
RIGHT_BG_CLOOR=(200,200,200)
SPACE_BLOCK_COLOR=(200,200,200)
SELECTED_COLOR=(0,255,0)
UNSELECTED_COLOR=(255,0,0)
GRADIENT_START_COLOR=(0x30,0xCF,0xD0)
GRADIENT_END_COLOR=(0x66,0X0F,0XDF)
# GRADIENT_START_COLOR=(0xFA,0x70,0x9A)
# GRADIENT_END_COLOR=(0xFE,0XE1,0X40)
# GRADIENT_START_COLOR=(0xA6,0xC0,0xFE)
# GRADIENT_END_COLOR=(0xF6,0X80,0X84)
#block object
class Block:
    def __init__(self, x, y, number, color,size=BLOCK_SIZE,font_ratio=0.5):
        self.x = x
        self.y = y
        self.number = number
        self.color = color
        self.size=size
        self.font_ratio=font_ratio
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if(self.number!=0):
            font = pygame.font.SysFont('Arial', int(self.font_ratio*self.size))
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
    def setText(self, text):
        self.text = text
    def setColor(self, color):
        self.color = color
#create the board object to contain the block
class Board:
    block_list=[]
    def __init__(self, x, y,size=BLOCK_SIZE, color=BOARD_BG_COLOR,state=[1,2,3,4,5,6,7,8,0]):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.state=state
        self.block_list.append(Block(0,0,0,SPACE_BLOCK_COLOR,self.size))
        for i in range(1,9):
            self.block_list.append(Block(x+PADDING+i%3*(size+PADDING), y+PADDING+i//3*(size+PADDING), i, gradient_color_generator(GRADIENT_START_COLOR,GRADIENT_END_COLOR, i),self.size))
        arrange_block(self.block_list, self.state,self.x,self.y,self.size)
    #display the board
    def display(self, screen):
        #display the board background
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size*3+self.size*4//PADDING_FRACTION, self.size*3+self.size*4//PADDING_FRACTION))
        #display the blocks
        for block in self.block_list:
            block.display(screen)
    #update the state
    def updateState(self, state):
        self.state=state
        arrange_block(self.block_list, self.state,self.x,self.y,self.size)
        
class TextView:
    def __init__(self, x, y, text,size, color=(0,0,0)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size=size
        font = pygame.font.SysFont('Arial', self.size)
        self.textRendered = font.render(self.text, True, self.color)
    def display(self, screen):
        font = pygame.font.SysFont('Arial', self.size)
        self.textRendered = font.render(self.text, True, self.color)
        screen.blit(self.textRendered, (self.x, self.y))
    def setText(self, text):
        self.text = text
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    def setMiddleX(self,left,right):
        self.x = (left+right)/2-self.textRendered.get_width()/2
#arrange block depending on the state
def arrange_block(block_list:list[Block], state_list:list[int],offsetx=0,offsety=0,size=BLOCK_SIZE):
    padding_size=size//PADDING_FRACTION
    for i in range(len(state_list)):
        block_list[state_list[i]].x = i%3*(size+padding_size)+padding_size+offsetx
        block_list[state_list[i]].y = math.floor(i/3)*(size+padding_size)+padding_size+offsety

#generate random color
def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#generate color based on the start color and end color and the index
def gradient_color_generator(start_color, end_color, index):
    r_start, g_start, b_start = start_color
    r_end, g_end, b_end = end_color
    r_diff = r_end - r_start
    g_diff = g_end - g_start
    b_diff = b_end - b_start
    r = r_start + r_diff*index/10
    g = g_start + g_diff*index/10
    b = b_start + b_diff*index/10
    return (int(r), int(g), int(b))

#find the button by text
def find_button(button_list:list[Button], text:str):
    for button in button_list:
        if button.getText() == text:
            return button

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
        block_list.append(Block(PADDING+(i-1)%GAME_SIZE*(BLOCK_SIZE+PADDING),PADDING+math.floor((i-1)/GAME_SIZE)*(BLOCK_SIZE+PADDING), i, gradient_color_generator((0xA6,0xC0,0xFE),(0xF6,0X80,0X84), i)))
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

def main_board():
    #init pygame window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    isRunning=True
    board=Board(0,0,40)
    cur_state=[0,1,2,3,4,5,6,7,8]
    while isRunning:
        #process the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                random.shuffle(cur_state)
                board.updateState(cur_state)
        #draw background
        screen.fill((0,0,0))
        
        board.display(screen)
        pygame.display.update()

if __name__ == "__main__":
    main_board()
    # main()