import pygame, random, board_generator


pygame.init()
fontSize = 80
font = pygame.font.SysFont("./Font/Lato-Light.ttf", fontSize)
fpsClock = pygame.time.Clock()
winx, winy = 720, 720
win = pygame.display.set_mode((winx, winy))


icon = pygame.image.load("./Icon/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Sudoku")


black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


#width of margins lines
lOutOfBoxes = 7
#width of lines in boxes
lInBoxes = 3
#find len of boxes
lengthOfBoxes = winx / 3
#length of square in boxes
lOfSqinBoxes = lengthOfBoxes / 3
def drawBackGround(winx, winy, lOutOfBoxes, lInBoxes, lengthOfBoxes, lOfSqinBoxes):
    #draw margins line
    pygame.draw.line(win, black, (0, 0), (winx, 0), lOutOfBoxes)
    pygame.draw.line(win, black, (0, 0), (0, winy), lOutOfBoxes)
    pygame.draw.line(win, black, (winx, 0), (winx, winy), lOutOfBoxes)
    pygame.draw.line(win, black, (0, winy), (winx, winy), lOutOfBoxes)

    #draw boxes
    pygame.draw.line(win, black, (lengthOfBoxes, 0), (lengthOfBoxes, winx), lOutOfBoxes)
    pygame.draw.line(win, black, (lengthOfBoxes * 2, 0), (lengthOfBoxes * 2, winx), lOutOfBoxes)
    pygame.draw.line(win, black, (0, lengthOfBoxes), (winx, lengthOfBoxes), lOutOfBoxes)
    pygame.draw.line(win, black, (0, lengthOfBoxes * 2), (winx, lengthOfBoxes * 2), lOutOfBoxes)

    #draw squares
    pygame.draw.line(win, black, (0, lOfSqinBoxes), (winx, lOfSqinBoxes), lInBoxes)
    pygame.draw.line(win, black, (0, lOfSqinBoxes * 2), (winx, lOfSqinBoxes * 2), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes, 0), (lOfSqinBoxes, winy), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes  * 2, 0), (lOfSqinBoxes * 2, winy), lInBoxes)

    pygame.draw.line(win, black, (0, lOfSqinBoxes * 4), (winx, lOfSqinBoxes * 4), lInBoxes)
    pygame.draw.line(win, black, (0, lOfSqinBoxes * 5), (winx, lOfSqinBoxes * 5), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes * 4, 0), (lOfSqinBoxes * 4, winy), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes  * 5, 0), (lOfSqinBoxes * 5, winy), lInBoxes)

    pygame.draw.line(win, black, (0, lOfSqinBoxes * 7), (winx, lOfSqinBoxes * 7), lInBoxes)
    pygame.draw.line(win, black, (0, lOfSqinBoxes * 8), (winx, lOfSqinBoxes * 8), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes * 7, 0), (lOfSqinBoxes * 7, winy), lInBoxes)
    pygame.draw.line(win, black, (lOfSqinBoxes  * 8, 0), (lOfSqinBoxes * 8, winy), lInBoxes)


#with this function i found wich square user selected
def choosingSq(sqDic, mx, my):
    #iterateing on sqDic items (key and values)
    for key, value in sqDic.items():
        #value[0] is start postion of square in x axis and value[1] is start postion of square in y axis.
        if mx > value[0] and mx < value[0] + lOfSqinBoxes and my > value[1] and my < value[1] + lOfSqinBoxes:
            sqXS, sqYS = value[0], value[1]
            #sqKeyNum is number of key for that square in dictionary
            sqKeyNum = key
            return sqXS, sqYS, sqKeyNum


#draw number on screen with numberDrawer function
def numberDrawer(sqDic):
    #iterateing on list of sqDic dictionary
    for list in sqDic.values():
        #with this i found if user can change number of this list
        if list[4] == False:
            #if user cant change number of selected square with this two line i draw number of this list
            text = font.render(str(list[3]), True, black)
            win.blit(text, (list[0] + 25, list[1] + 20))
        #if user can change number i check for user number of list if it was None i dont draw anything else i draw number of it
        else:
            if list[2] == None:
                pass
            else:
                text = font.render(str(list[2]), True, blue)
                win.blit(text, (list[0] + 25, list[1] + 20))


#with this function i check user answer.
def checker(sqDic):
    """
    i iterate on values of sqDic and if list[4](isUsr) == True i check if
    un(number that user choose for that square) is equal with real number of
    that square i draw number of that square with green else i draw number with
    red(becuse the user guess is incorrect)
    """
    for list in sqDic.values():
        if list[4] == True:
            #user guess is correct
            if list[2] == list[3]:
                text = font.render(str(list[3]), True, green)
                win.blit(text, (list[0] + 25, list[1] + 20))
            #user guess is incorrect
            else:
                text = font.render(str(list[3]), True, red)
                win.blit(text, (list[0] + 25, list[1] + 20))
        #if that number is not for user i draw it with black
        else:
            text = font.render(str(list[3]), True , black)
            win.blit(text, (list[0] + 25, list[1] + 20))


#with newGame function run sudoku algorithm and initialize new sqDic
def newGame():
    #running sudoku algorithm and making lists that program use
    #lonucchange = list of numbers user can change
    lOAllNums, lonucchange = board_generator.generate()
    #sqDic values are lists that contains information about squares of board
    sqDic = {}
    #i use sqNum for dictionary keys.
    sqNum = 1
    """
    sx and sy is start position of box in x and y axis. un is the number that
    the user chooses for the square. rn is the real number of that square
    isUsr is boolian variable if it was True user can put number in variable
    else user cant (the defualt value is True and it change in program)
    """
    sx, sy, un, isUsr = 0, 0, None, True
    for square in lOAllNums:
        rn = square
        sqDic[sqNum] = [sx, sy, un, rn, isUsr]
        if sx == winx - lOfSqinBoxes:
            sx = 0
            sy += lOfSqinBoxes
        else:
            sx += lOfSqinBoxes
        sqNum += 1
    """
    with this loop i iterate on lonucchange list if item != None i change
    list[4](isUsr) = False abd it mean user cant change number of that square
    """
    num = 1
    for item in lonucchange:
        if item != None:
            list = sqDic[num]
            list[4] = False
            sqDic[num] = list
        num += 1
    return sqDic


fps = 60
#click value is for finding is any square selected
click = False
#if user press space showAnswer change to True and if newGame() function run it change to False
showAnswer = False
#Generate sudoku board for first time
sqDic = newGame()
running = True
while running:
    fpsClock.tick(60)
    #fill background with white
    win.fill(white)
    #draw background
    drawBackGround(winx, winy, lOutOfBoxes, lInBoxes, lengthOfBoxes, lOfSqinBoxes)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #mx and my is mouse postion in x and y axis
                mx, my = pygame.mouse.get_pos()
                #find which square is selected
                """
                is use except becuse if player click on lines that is for drawing
                background becuse that line is not a part of square TypeError raise
                """
                try:
                    """
                    sqXS and sqYS is start position of square in x and y
                    axis and sqKeyNum is number of key of that square
                    """
                    sqXS, sqYS, sqKeyNum = choosingSq(sqDic, mx, my)
                    click = True
                except TypeError:
                    pass

        if event.type == pygame.KEYDOWN:
            #check if user click on one square game let user to change number of that square
            if click == True:
                list = sqDic[sqKeyNum]
                if list[4] == True:
                    #deleting the number of square
                    if event.key == pygame.K_BACKSPACE:
                        list[2] = None
                    #adding number to square
                    else:
                        try:
                            key = int(event.unicode)
                            if key != 0:
                                list[2] = key
                        except ValueError:
                            pass
                    sqDic[sqKeyNum] = list

            if event.key == pygame.K_SPACE:
                if showAnswer == True:
                    showAnswer = False
                else:
                    showAnswer = True

            if event.key == pygame.K_r:
                sqDic = newGame()
                showAnswer = False


    #if user click on one square game draw red square on that square
    if click == True:
        pygame.draw.rect(win, red, (sqXS, sqYS, lOfSqinBoxes, lOfSqinBoxes), 7)


    #draw numbers
    if showAnswer == False:
        numberDrawer(sqDic)
    if showAnswer == True:
        checker(sqDic)


    pygame.display.update()


pygame.quit()
