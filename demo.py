from cmath import exp
from Searching_expanded import *
from visualization import *

#input number list
def input_number_list(prompt):
    print(prompt)
    number_list = []
    number_list = list(map(int, input().split(" ")))
    return number_list

doneSearching=False

#main function
def visualization_main():
    #init states
    start_states = [1,2,3,4,5,6,7,8,0]
    end_states = [8,7,6,5,4,3,2,1,0]
    
    # input states
    start_states=input_number_list(prompt="Input initial states(like:1 2 3 4 5 6 7 8 0): ")
    end_states=input_number_list(prompt="Input end states(like:8 7 6 5 4 3 2 1 0): ")
    print("start with")
    print(start_states)
    print("end with")
    print(end_states)
    #init pygame window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("8 digits", "8 digits")
    
    
    #init solution
    solClass=Solution(start_states,end_states)
    #init board
    board=Board(0,0)
    current_states = start_states
    board.updateState(current_states)
    #init buttons
    control_button_list = []
    control_button_list.append(Button(MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH)/2,BUTTON_3_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"solve",(255,0,0)))
    control_button_list.append(Button(MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH)/2,BUTTON_4_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"reset",(0,255,0)))
    control_button_list.append(Button(MIDDLE_EDGE+(WINDOW_WIDTH-MIDDLE_EDGE-BUTTON_WIDTH)/2,BUTTON_5_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"tree",(105,105,105)))
    #initilize the algorithm selection
    algorithm_selection_button_list=[]
    algorithm_selection_button_list.append(Button(BUTTON_1_X,BUTTON_1_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"BFS",UNSELECTED_COLOR))
    algorithm_selection_button_list.append(Button(BUTTON_2_X,BUTTON_1_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"DFS",UNSELECTED_COLOR))
    algorithm_selection_button_list.append(Button(BUTTON_1_X,BUTTON_2_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"A*",SELECTED_COLOR))
    algorithm_selection_button_list.append(Button(BUTTON_2_X,BUTTON_2_Y,BUTTON_WIDTH,BUTTON_HEIGHT,"GREEDY",UNSELECTED_COLOR))
    selectedAlgorithm="A*"
    #init the text view
    text_view=TextView(TEXT_VIEW_X,TEXT_VIEW_Y,"total generated:Nan,total expanded:Nan,total steps:Nan,time consumed:Nan",15)
    #some flag definitions
    isSolving=False
    stepCnt=0
    totStep=0
    answer_list=[]
    root=TreeNode(current_states,None)
    expand_cnt=0
    fpsclock=pygame.time.Clock()
    #game loop
    running = True
    while running:
        #control the fps
        fpsclock.tick(FPS)
        #check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in control_button_list:
                    #process the control button
                    if button.isClicked(pygame.mouse.get_pos()):
                        if button.getText() == "solve":
                            #solve the game
                            isSolving=True
                            stepCnt=0
                            button.setText("searching")
                            button.display(screen)
                            pygame.display.update()
                            # solClass.Astar(start_states,end_states)
                            #choose algorithm to solve the game
                            if selectedAlgorithm=="BFS":
                                iternum,cost,answer_list,root,expand_cnt=solClass.BFS()
                            elif selectedAlgorithm=="DFS":
                                iternum,cost,answer_list,root,expand_cnt=solClass.DFS()
                            elif selectedAlgorithm=="A*":
                                iternum,cost,answer_list,root,expand_cnt=solClass.Astar(solClass.Manhattan)
                            elif selectedAlgorithm=="GREEDY":
                                iternum,cost,answer_list,root,expand_cnt=solClass.Greedy()
                            totStep=len(answer_list)
                            if totStep==0:
                                button.setText("no solution")
                                isSolving=False
                            else:
                                button.setText("solving")
                            text_view.setText("total generated:{},total expanded:{},total steps:{},time consumed:{:.1f}".format(iternum,expand_cnt,totStep,cost))
                            doneSearching=True
                            find_button(control_button_list,"tree").setColor((0,255,0))
                        elif button.getText() == "reset":
                            if isSolving:
                                isSolving=False
                                find_button(control_button_list,"solving").setText("solve")
                            current_states=start_states
                            board.updateState(current_states)
                        elif button.getText() == "tree":
                            if not isSolving and doneSearching:
                                solClass.Display(root)

                    #process the algorithm selection buttons
                    for button in algorithm_selection_button_list:
                        if button.isClicked(pygame.mouse.get_pos()):
                            selectedAlgorithm=button.getText()
                        #update color of the selected button
                        if button.getText()==selectedAlgorithm:
                            button.setColor(SELECTED_COLOR)
                        else:
                            button.setColor(UNSELECTED_COLOR)
        #if the game is solving, update the state
        if isSolving:
            current_states=answer_list[stepCnt]
            board.updateState(current_states)
            stepCnt+=1
            if stepCnt==totStep:
                isSolving=False
                control_button_list[0].setText("solve")
        #draw background
        screen.fill(BOARD_BG_COLOR)
        pygame.draw.rect(screen,RIGHT_BG_CLOOR, (MIDDLE_EDGE,0,WINDOW_WIDTH-MIDDLE_EDGE,WINDOW_HEIGHT))
        #draw board
        board.display(screen)
        #draw buttons
        for button in control_button_list:
            button.display(screen)
        for button in algorithm_selection_button_list:
            button.display(screen)
        #draw text view
        text_view.setMiddleX(MIDDLE_EDGE,WINDOW_WIDTH)
        text_view.display(screen)
        #update screen
        pygame.display.update()
    pygame.quit()

# def input_test():
#     number_list = []
#     number_list=input_number_list()
#     print(number_list)

if __name__ == '__main__':
    visualization_main()
    # input_test()