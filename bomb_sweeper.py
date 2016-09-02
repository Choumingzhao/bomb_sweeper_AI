# -*- encoding:utf-8 -*-

"""This python code for the classic windows game Bomb Sweeper.

    I have no GUI experience before. So I just try to learn while coding.
    
    Please run it with IDLE if you are on Windows.
    Every move need 3 instructions:
        1. 'L'(or 'l') or 'R'(or 'r') for left click and right click in the pixel in the panel.
        2,3. two integers between the 1-10, the row and column number of the panel.
"""

import random
import sys


# def the new Class for each pixel of the panel
class Pixel:

    """The Class Pixel has these attributes:

    bool 'showable':   the status whether the pixel can be seen by the player.
    bool 'isbomb':     tell me whether this pixel has a bomb.
    int 'status':      record the number of the bomb near the pixel.
    int mark_status':  record the mark player has made,0 indicates the player
    have done nothing, 1 indicates the player think this is a bomb, 2 indicate
    the player think this has to be considered later.
    """
    def __init__(self):
        self.showable = False
        self.isbomb = False
        self.status = None
        self.mark_status = 0
        self.x = None
        self.y = None

    def getindex(self):
        return self.x, self.y


def num2tuple(num):
    """This function convert a number to a 2-D tuple in the panel.
    """
    r = num // N
    c = num % N
    return r, c


def tuple2num(*args):
    """Function to convert a 2-D tuple to a number.
    """
    r, c = args[0], args[1]
    return r*N+c


def surr2(panel_name, num):
    """surr2 is a generator that return the object in each panel and a improved
    version of surr.
    """
    r, c = num2tuple(num)
    neighbor_tuple = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1),
                      (r+1, c-1), (r+1, c), (r+1, c+1)]
    for neighbor in neighbor_tuple:
        if neighbor[0] in range(M) and neighbor[1] in range(N):
            yield panel_name[neighbor[0]][neighbor[1]]


def count_surr(panel_name, num):
    """ This function calculate the bombs in the near the selected pixel.
    """
    count = 0
    for pixel in surr2(panel_name, num):
        if pixel.isbomb:
            count += 1
    return count


def endgame():
    """The function to end the game
    """
    refresh(panel)
    print("Game Over")
    for j in range(N):
        for i in range(M):
            print(panel[i][j].status, end=' ')
        print()
    sys.exit()


def refresh(panel_name):
    """Function refresh is used to reprint the current panel in the screen.
    """
    for j in range(N):
        for i in range(M):
            if panel_name[i][j].showable:
                print(panel_name[i][j].status, end=' ')
            elif panel_name[i][j].mark_status == 1:
                print('\u2691', end=' ')
            elif panel_name[i][j].mark_status == 2:
                print('?', end=' ')
            else:
                print('■', end=' ')
        print()


def l_click(m, n):
    """Simulating the effect when left click on the pixel (m,n).
    """
    pixel = panel[m][n]
    if pixel.showable:
        print("This pixel is unclickable!")
        return None
    if pixel.isbomb:
        pixel.showable = True
        endgame()
    else:
        pixel.showable = True


def handleStatus0(args):
    """Handle the situation when you left click a pixel, the pixel.status happend
    to be 0.
    """
    r, c = args[0], args[1]
    for pixel in surr2(panel, tuple2num(r, c)):
        if pixel.showable is False:
            pixel.showable = True
            if pixel.status == 0:
                handleStatus0(pixel.getindex())


def r_click(m1, m2, m3):
    """Simulating the effect when left click on the pixel (m1, m2).
    msg3 is the mark_status player set.
    """
    pixel = panel[m1][m2]
    if pixel.showable:
        print("This pixel is unclickable！")
    else:
        pixel.mark_status = m3
# set the panel and the number of bombs
M = 10
N = 10
bomb_num = 6

# generate the M*N panel using a 2-D list
panel = []
for mm in range(M):
    sublist = []
    for nn in range(N):
        sublist.append(Pixel())
    panel.append(sublist)

# generate the bombs
bomb_list = random.sample(range(M*N), bomb_num)
bomb_list.sort()
no_bomb_list = [i for i in range(M*N) if i not in bomb_list]
no_bomb_list.sort()

# fill the pixel in the panel using bomb_list above
for number in range(M*N):
    row, col = num2tuple(number)
    if number in bomb_list:
        panel[row][col].isbomb = True
        panel[row][col].status = 'x'
        panel[row][col].x = row
        panel[row][col].y = col
# fill the empty pixel
for numb in no_bomb_list:
    row, col = num2tuple(numb)
    panel[row][col].status = count_surr(panel, numb)
    panel[row][col].x = row
    panel[row][col].y = col

# Wait for user input and do something using functions.
while True:
    refresh(panel)
    msg0 = input('>')
    msg1 = int(input('>'))-1
    msg2 = int(input('>'))-1
    if msg0 == 'L' or msg0 == 'l':
        l_click(msg1, msg2)
        if panel[msg1][msg2].status == 0:
            handleStatus0((msg1, msg2))
    elif msg0 == 'R' or msg0 == 'r':
        msg3 = int(input("Input your mark status of this pixel:\n>"))
        r_click(msg1, msg2, msg3)
    else:
        print("Please input right instructions！")
    # check whether all no-bomb area have been found(shown) by the player.
    if all(panel[num2tuple(i)[0]][num2tuple(i)[1]].showable for i in
           no_bomb_list):
        print("You won!")
        endgame()
