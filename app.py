import random

subgrids_conquered = [0] * 9  
last_played_subgrid = -1      
current_player = 1

def create_board():
    return [0] * 81

def number_is_valid(board, index, num):
    row = index // 9
    col = index % 9

    # Checa Linha
    for i in range(9):
        pos = row * 9 + i
        if pos != index and board[pos] == num:
            return False
            
    # Checa Coluna
    for i in range(9):
        pos = i * 9 + col
        if pos != index and board[pos] == num:
            return False
            
    # Checa Quadrante 3x3
    r_start, c_start = 3 * (row // 3), 3 * (col // 3)
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            pos = r * 9 + c
            if pos != index and board[pos] == num:
                return False            
    return True

def has_valid_move_in_subgrid(board, subgrid_id):
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    indices = []
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            indices.append(r * 9 + c)
    
    empty_cells = [i for i in indices if board[i] == 0]
    
    if not empty_cells: return True 

    for idx in empty_cells:
        for n in range(1, 10):
            if number_is_valid(board, idx, n):
                return True 
    return False

def clean_subgrid(board, subgrid_id):
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    for r in range(r_start, r_start + 3):
        for c in range(c_start, c_start + 3):
            board[r * 9 + c] = 0 
    print(f"\n--- O Quadrante {subgrid_id} estava travado e foi resetado! ---")

def check_subgrid_conquest(board, index):
    subgrid_id = (index // 27) * 3 + ((index % 9) // 3)
    r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
    indices = [r * 9 + c for r in range(r_start, r_start + 3) for c in range(c_start, c_start + 3)]
    
    if all(board[i] != 0 for i in indices):
        subgrids_conquered[subgrid_id] = current_player
        print(f"Quadrante {subgrid_id} conquistado pelo Jogador {current_player}!")

def play_is_valid_detailed(board, index, num):
    if not (0 <= index <= 80): 
        return False, "Índice fora do tabuleiro (0-80)."
    if board[index] != 0: 
        return False, "Esta posição já está ocupada."

    current_subgrid = (index // 27) * 3 + ((index % 9) // 3)
    if last_played_subgrid != -1 and current_subgrid == last_played_subgrid:
        return False, f"O Quadrante {current_subgrid} está bloqueado nesta rodada!"

    if not number_is_valid(board, index, num):
        return False, "Violação de Sudoku (Número repetido na linha, coluna ou bloco)."
        
    return True, "Sucesso"

def play_auto(board):
    for i in range(81):
        for n in range(1, 10):
            if play_is_valid_detailed(board, i, n)[0]:
                return i, n
    return None, None

def check_win():
    v = subgrids_conquered
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_conditions:
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
    print(f"Status dos Quadrantes: {subgrids_conquered}")
    if last_played_subgrid != -1:
        print(f"Quadrante Bloqueado: {last_played_subgrid}")
    else:
        print("Bloqueio: NENHUM (Passe Livre Ativo)")

def generate_random_numbers(board):
    for subgrid_id in range(9):
        r_start, c_start = (subgrid_id // 3) * 3, (subgrid_id % 3) * 3
        indices = [r * 9 + c for r in range(r_start, r_start + 3) for c in range(c_start, c_start + 3)]
        
        amount = random.randint(2, 5)
        chosen_pos = random.sample(indices, amount)

        for idx in chosen_pos:
            nums = list(range(1, 10))
            random.shuffle(nums)
            for n in nums:
                if number_is_valid(board, idx, n):
                    board[idx] = n
                    break

# --------
board = create_board()
generate_random_numbers(board)

while True:
    print_board(board)
    print(f"\nVez do Jogador {current_player}")
    
    if current_player == 1:
        entry = input("Índice (0-80) e Número (Ex: 10 5) ou '-1' para sair: ")
        if entry == "-1": break
        try:
            parts = entry.split()
            idx, num = int(parts[0]), int(parts[1])
        except:
            print("[ERRO] Formato inválido! Digite dois números.")
            continue
    else:
        idx, num = play_auto(board)
        if idx is None:
            print("Algoritmo não encontrou jogadas. Pulando turno...")
            current_player = 2 if current_player == 1 else 1
            continue
        print(f"Algoritmo jogou no índice {idx} o número {num}")

    is_valid, reason = play_is_valid_detailed(board, idx, num)
    
    if is_valid:
        board[idx] = num
        check_subgrid_conquest(board, idx) 

        next_destination = (idx // 27) * 3 + ((idx % 9) // 3) 
        
        if not has_valid_move_in_subgrid(board, next_destination):
            clean_subgrid(board, next_destination)
            last_played_subgrid = -1 
            print(f"[SISTEMA] PASSE LIVRE ATIVADO: Próximo joga onde quiser.")
        else:
            last_played_subgrid = next_destination

        winner = check_win()
        if winner:
            print_board(board)
            print(f"\n***** FIM DE JOGO! JOGADOR {winner} VENCEU! *****")
            break
            
        current_player = 2 if current_player == 1 else 1
    else:
        print(f"[JOGADA INVÁLIDA] {reason}")

print("Programa finalizado.")