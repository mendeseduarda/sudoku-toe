import random

subgrids_conquered = [0] * 9  
last_played_subgrid = -1      
current_player = 1

def create_board():
    return [0] * 81

def number_is_valid(board, index, num):
    row, col = index // 9, index % 9
    
    for i in range(9):
        if (board[row * 9 + i] == num and (row * 9 + i) != index) or \
           (board[i * 9 + col] == num and (i * 9 + col) != index):
            return False
        
    r_start, c_start = 3 * (row // 3), 3 * (col // 3)
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            pos = r * 9 + c
            if pos != index and board[pos] == num:
                return False            
    return True

def has_valid_move_in_subgrid(board, subgrid_id):
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            idx = r * 9 + c
            if board[idx] == 0:
                for n in range(1, 10):
                    if number_is_valid(board, idx, n):
                        return True 
    return False

def clean_subgrid(board, subgrid_id):
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            board[r * 9 + c] = 0 
    print(f"--- Quadrante {subgrid_id} resetado! ---")

def check_subgrid_conquest(board, index, player):
    global subgrids_conquered
    subgrid_id = (index // 27) * 3 + ((index % 9) // 3)
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    indices = [r * 9 + c for r in range(r_start, r_start + 3) for c in range(c_start, c_start + 3)]
    
    if all(board[i] != 0 for i in indices):
        subgrids_conquered[subgrid_id] = player
        return True
    return False

def play_is_valid_detailed(board, index, num, blocked_subgrid):
    if not (0 <= index <= 80): return False, "Índice inválido."
    if board[index] != 0: return False, "Posição ocupada."
    
    current_q = (index // 27) * 3 + ((index % 9) // 3)
    if blocked_subgrid != -1 and current_q == blocked_subgrid:
        return False, f"Quadrante {current_q} bloqueado!"

    if not number_is_valid(board, index, num):
        return False, "Regra do Sudoku violada."
    return True, "Sucesso"

def play_auto(board, blocked_subgrid):
    for i in range(81):
        q = (i // 27) * 3 + ((i % 9) // 3)
        if q != blocked_subgrid and board[i] == 0:
            for n in range(1, 10):
                if number_is_valid(board, i, n):
                    return i, n
    return None, None

def check_win():
    v = subgrids_conquered
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if v[a] == v[b] == v[c] != 0: return v[a]
    return 0

def generate_random_numbers(board):
    for q in range(9):
        r_s, c_s = (q // 3) * 3, (q % 3) * 3
        indices = [r * 9 + c for r in range(r_s, r_s + 3) for c in range(c_s, c_s + 3)]
        for idx in random.sample(indices, random.randint(1, 2)):
            for n in random.sample(range(1, 10), 9):
                if number_is_valid(board, idx, n):
                    board[idx] = n
                    break

def print_board(board):
    print("\n    0 1 2   3 4 5   6 7 8")
    print("  +-------+-------+-------+")
    for i in range(9):
        row_data = board[i*9 : (i+1)*9]
        row_str = ""
        for j, val in enumerate(row_data):
            if j % 3 == 0: row_str += "| "
            row_str += (str(val) if val != 0 else ".") + " "
        print(f"{i} {row_str}|")
        if (i + 1) % 3 == 0:
            print("  +-------+-------+-------+")
    print(f"Status dos Quadrantes: {subgrids_conquered}")
    if last_played_subgrid != -1:
        print(f"Quadrante Bloqueado: {last_played_subgrid}")
    else:
        print("Bloqueio: NENHUM (Passe Livre Ativo)")