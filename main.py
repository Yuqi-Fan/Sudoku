import numpy as np
import random

def convert_s():

    print("""***********************************************
* Enter the number of the sudoku of each row. *
* If it is an empty space, enter '0' instead. *
* Separate each number of a row by space.     *
***********************************************""")
    print('Enter the number, separated by space and press enter to start to enter next row.')
    sudoku = []
    for i in range(9):
        r = (input()).split()
        row = []
        for n in r:
            row.append(int(n))
        sudoku.append(row)
    return sudoku

def checker(sudoku):
    valid = True

    for row in range(9):
        num1=[]
        num2=set()

        for c in range(9):
            if sudoku[row][c] !=0:
                num1.append(sudoku[row][c])
                num2.add(sudoku[row][c])

        if len(num1) != len(num2):
            valid = False

    for col in range(9):
        num1 = []
        num2 = set()

        for r in range(9):
            if sudoku[r][col] != 0:
                num1.append(sudoku[r][col])
                num2.add(sudoku[r][col])

        if len(num1) != len(num2):
            valid = False

    num1 = []
    num2 =set()
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            for b in range(0,3,1):
                for a in range(0,3,1):
                    if sudoku[i+b][j+a]!=0:
                        num1.append(sudoku[i+b][j+a])
                        num2.add(sudoku[i+b][i+a])
                        if len(num1) != len(num2):
                            valid = False
    return valid

def get_row(sudoku,row):
    return sudoku[row,:]

def get_col(sudoku,col):
    return sudoku[:,col]

def get_block(sudoku,row,col):
    row_start = row // 3 * 3
    col_start = col // 3 * 3
    return sudoku[row_start:row_start+3,col_start:col_start+3]

def generate_board():
    """
    generate the board for the sudoku
    :return:
    """
    random.seed()
    sample = np.array(range(1, 10))
    sudoku=np.zeros((9,9),dtype=int)
    for row in range(9):
        for col in range(9):
            sudoku_row = get_row(sudoku,row)
            sudoku_col = get_col(sudoku,col)
            sudoku_block = get_block(sudoku,row,col)

            used_n = np.union1d(np.union1d(sudoku_row, sudoku_col), sudoku_block)
            rest_n = np.setdiff1d(sample, used_n)

            if len(rest_n) == 0:
                return sudoku
                raise Exception('wrong, no number could be used')

            rand_n = random.sample(rest_n.tolist(),1)[0]
            sudoku[row,col]=rand_n

    return sudoku

def generate_game(sudoku):
    """
    generate the game of the sudoku with different levels by call the function generate_board
    :param sudoku:
    :return:
    """
    sudo=sudoku
    print("""**********************
* Level 1: 30 spaces *
* Level 2: 40 spaces *
* Level 3: 50 spaces *
**********************""")
    level = int(input('Enter the difficulty level you want to play:'))
    if level == 1:
        len=30
    elif level == 2:
        len=40
    elif level == 3:
        len=50
    else:
        print('enter a valid number')
    lenth=len
    for i in range(lenth):
        row=random.randint(0,8)
        col=random.randint(0,8)
        while sudo[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        sudo[row][col] = 0
    print(sudo)
    print('Try to solve it.')
    i=0
    for i in range(9):
        for j in range(9):
            if sudo[i][j] == 0:
                print(f'which number would be suitable to fill the position ({i},{j})?')
                num=int(input('Number you want to fill:'))
                while -1 < i < 4:
                    if num != sudoku[i][j]:
                        i+=1
                        print(f'try again!')
                        num=int(input('Number you want to fill:'))
                    else:
                        print('this value is right. next')
                        break
                if i > 3:
                    print('you have used all of the chance. lose the game.')
                    value=False
                    break
                else:
                    sudo[i][j] = num
                    print(sudo)
        if not value:
            break

    if i<4:
        print('you solved all of the positions. Win the game!')

def get_next(sudoku,row,col):
    """
    :param sudoku: the matrix of the sudoku needed to be solved
    :param row: the row number of the empty space
    :param col: the col number of the empty space
    :return: get the row and col of next empty space
    """
    for next_col in range(col+1,9):
        if sudoku[row][next_col] == 0:
            return row,next_col
    for next_row in range(row+1,9):
        for next_col in range(0,9):
            if sudoku[next_row][next_col] == 0:
                return next_row,next_col

    return -1,-1 # if there is no next empty space

def possible_value(sudoku,row,col):
    """the possible values could be put into the position
    :param sudoku: the matrix of the sudoku needed to be solved
    :param row: the row number of the empty space
    :param col: the col number of the empty space
    :return: the list of the possible value for the empty space
    """
    i,j = row//3,col//3
    grid = [sudoku[i*3+r][j*3+c] for r in range(3) for c in range(3)]
    value = set([x for x in range(1,10)])-set(grid)-set(sudoku[row])-set(list(zip(*sudoku))[col])#from blog
    return list(value)

def start_position(sudoku):
    """to get the start position of the sudoku
    :param sudoku: the matrix of the sudoku needed to be solved
    :return: the position of the first empty space
    """
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                return row, col
    return False,False #if the sudoku is already solved, return false,false

def try_solve_sudo(sudoku,row,col):
    """
    :param sudoku: the matrix of the sudoku needed to be solved
    :param row: the row number of the empty space
    :param col: the col number of the empty space
    :return: bool
    """
    for v in possible_value(sudoku,row,col):
        sudoku[row][col] = v
        next_row,next_col = get_next(sudoku,row,col)
        if next_row == -1:
            return True
        else:
            end = try_solve_sudo(sudoku,next_row,next_col)
            if end:
                return True
            sudoku[row][col] = 0

def solve_sudo(sudoku):
    """the sovling part of the sudoku
    :param sudoku: the matrix of the sudoku needed to be solved
    :return: none
    """
    row,col = start_position(sudoku)
    try_solve_sudo(sudoku,row,col)
    for i in range(9):
        print(sudoku[i])

#main part
def sudoku():
    """the main part of the application
    :return:none
    """
    print("""*******************************************
* Choose which mode you want to enter:    *
* 1. check and get the result of a sudoku *
* 2. play to solve sudoku                 *
*******************************************
""")
    op=int(input('Enter the mode you want to choose:'))
    while (op != 1) & (op != 2):
        op = int(input('You enter the wrong number, Please enter again:'))

    if op == 1:
        sudoku=convert_s()
        value=checker(sudoku)
        if value:
            solve_sudo(sudoku)
        else:
            print('The sudoku could not be solved.')
    elif op == 2:
        sudoku_value = generate_board()
        generate_game(sudoku_value)


sudoku()


