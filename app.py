import random

def create_subgrid():
   subgrid = []
   for i in range(3):
    row = []
    for j in range(3):
        row.append(0)  
    subgrid.append(row)
   return subgrid


def create_board():
   board = []
   for i in range(3):
        row=[]
        for j in range(3):
            row.append(create_subgrid())
        board.append(row)
   return board

def get_value(board, row, col):
    return board[row//3][col//3][row%3][col%3]

def set_value(board, row, col, num):
    board[row//3][col//3][row%3][col%3] = num

    
def number_is_valid(board, row, col, num):
    for c in range(9):
        if get_value(board, row, c) == num:
            return False
    for r in range(9):
        if get_value(board, r, col) == num:
            return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    for r in range(start_row, start_row+3):
        for c in range(start_col, start_col+3):
            if get_value(board, r, c) == num:
                return False
    return True

def random_complet_board(board):
    for row in range(9):
        for col in range(9):
            if get_value(board, row, col) == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if number_is_valid(board, row, col, num):
                        set_value(board, row, col, num)
                        if random_complet_board(board):
                            return True
                        set_value(board, row, col, 0)  # backtrack
                return False
    return True

##-----------------------
subgrid = create_subgrid()
board = create_board()
boardRandom = random_complet_board(board)

for big_row in range(3):
    for small_row in range(3):
        row = []
        for big_col in range(3):
            row.extend(board[big_row][big_col][small_row])
        print(row)
    print()

##print(boardRandom)

