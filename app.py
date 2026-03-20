import random

quadrantes_conquistados = [0] * 9  
ultimo_quadrante_jogado = -1      
jogador_atual = 1

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


def check_subgrid(board, index):
    quad_id = (index // 27) * 3 + ((index % 9) // 3)
    indices = []
    r_start, c_start = (quad_id // 3) * 3, (quad_id % 3) * 3
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            indices.append(r * 9 + c)
    
    if all(board[i] != 0 for i in indices):
        quadrantes_conquistados[quad_id] = jogador_atual
        print(f"Quadrante {quad_id} conquistado pelo Jogador {jogador_atual}!")
    return

def play_is_valid(board, index, num):
    if index == -1: return True # Sinal para sair
    if not (0 <= index <= 80): return False
    if board[index] != 0: return False
    
    quad_atual = (index // 27) * 3 + ((index % 9) // 3)
    if quad_atual == ultimo_quadrante_jogado:
        print("Aviso: Quadrante bloqueado! Jogue em outro.")
        return False
    
    return number_is_valid(board, index, num)

def play_auto(board):
    for i in range(81):
        for n in range(1, 10):
            if play_is_valid(board, i, n):
                return i, n
    return None, None

def win():
    v = quadrantes_conquistados
    vitorias = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in vitorias:
        if v[a] == v[b] == v[c] != 0:
            return v[a]
    return 0

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
    print(f"Status dos Quadrantes: {quadrantes_conquistados}")
    if ultimo_quadrante_jogado != -1:
        print(f"Quadrante Bloqueado: {ultimo_quadrante_jogado}")

# --------
board = create_board()

while True:
    print_board(board)
    print(f"\nVez do Jogador {jogador_atual}")
    
    if jogador_atual == 1:
        entrada = input("Índice (0-80) e Número (Ex: 10 5) ou '-1' para sair: ")
        if entrada == "-1": break
        try:
            idx, num = map(int, entrada.split())
        except: continue
    else:
        idx, num = play_auto(board)
        print(f"Algoritmo jogou no índice {idx} o número {num}")

    if play_is_valid(board, idx, num):
        board[idx] = num
        check_subgrid(board, idx)
        ultimo_quadrante_jogado = (idx // 27) * 3 + ((idx % 9) // 3)
        
        vencedor = win()
        if vencedor:
            print_board(board)
            print(f"FIM DE JOGO! Jogador {vencedor} venceu a linha de quadrantes!")
            break
            
        jogador_atual = 2 if jogador_atual == 1 else 1
    else:
        print("Jogada inválida!")

print("Execução encerrada.")