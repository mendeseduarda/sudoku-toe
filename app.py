import random

def create_board():
    return [0] * 81

def number_is_valid(board, index, num):
    row = index // 9
    col = index % 9
    
    for i in range(9):
        if board[row * 9 + i] == num:
            return False
            
    for i in range(9):
        if board[i * 9 + col] == num:
            return False
            
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r * 9 + c] == num:
                return False
    return True

def random_complete_board(board):
    for i in range(81):
        if board[i] == 0:
            nums = list(range(1, 10))
            random.shuffle(nums)
            
            for num in nums:
                if number_is_valid(board, i, num):
                    board[i] = num
                    if random_complete_board(board):
                        return True
                    board[i] = 0 
            return False
    return True

# --------
board = create_board()
random_complete_board(board)

# imprimir bonito 
def print_board(board):
    for i in range(0, 81, 9):
        print(board[i:i+9])

print_board(board)