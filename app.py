from flask import Flask, render_template, request, jsonify
import logic

app = Flask(__name__)

board = logic.create_board()
logic.generate_random_numbers(board)
last_played_subgrid = -1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({
        "board": board,
        "last_played": last_played_subgrid,
        "subgrids_conquered": logic.subgrids_conquered
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    global last_played_subgrid
    data = request.json
    idx, num = int(data['index']), int(data['num'])
    
    valid, reason = logic.play_is_valid_detailed(board, idx, num, last_played_subgrid)
    if not valid:
        return jsonify({"status": "error", "message": reason})

    board[idx] = num
    logic.check_subgrid_conquest(board, idx, 1)
    last_played_subgrid = (idx // 27) * 3 + ((idx % 9) // 3)

    alg_idx, alg_num = logic.play_auto(board, last_played_subgrid)
    if alg_idx is not None:
        board[alg_idx] = alg_num
        logic.check_subgrid_conquest(board, alg_idx, 2)
        last_played_subgrid = (alg_idx // 27) * 3 + ((alg_idx % 9) // 3)


    reset = False
    for q in range(9):
        if logic.subgrids_conquered[q] == 0 and not logic.has_valid_move_in_subgrid(board, q):
            logic.clean_subgrid(board, q)
            last_played_subgrid = -1 
            reset = True

    return jsonify({
        "status": "success",
        "board": board,
        "player_idx": idx,
        "alg_idx": alg_idx,
        "subgrids_conquered": logic.subgrids_conquered,
        "last_played": last_played_subgrid,
        "reset": reset,
        "winner": logic.check_win()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)