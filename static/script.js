let currentIdx = -1;
const boardElement = document.getElementById('sudoku-board');
const sidePanel = document.querySelector('.side-panel');

// 1. Criar o Mini-Mapa acima do teclado
const miniBoard = document.createElement('div');
miniBoard.className = 'mini-board';
for (let i = 0; i < 9; i++) {
    const miniCell = document.createElement('div');
    miniCell.className = 'mini-cell';
    miniCell.id = `mini-${i}`;
    miniBoard.appendChild(miniCell);
}
sidePanel.prepend(miniBoard); // Adiciona no topo do painel lateral

// Inicialização do tabuleiro principal
if (boardElement) {
    for (let i = 0; i < 81; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.id = `cell-${i}`;
        cell.onclick = () => focusCell(i);
        boardElement.appendChild(cell);
    }
}

function focusCell(i) {
    currentIdx = i;
    document.querySelectorAll('.cell').forEach(c => c.classList.remove('focused'));
    document.getElementById(`cell-${i}`)?.classList.add('focused');
}

document.addEventListener('keydown', e => {
    if (currentIdx !== -1 && e.key >= '1' && e.key <= '9') enviarJogada(currentIdx, parseInt(e.key));
});

const selectBtn = n => currentIdx !== -1 ? enviarJogada(currentIdx, n) : showToast("Selecione uma casa");

async function enviarJogada(idx, num) {
    const res = await fetch('/make_move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({index: idx, num: num})
    });
    const data = await res.json();
    data.status === "success" ? atualizar(data) : showToast(data.message);
}

function atualizar(data) {
    const { board, subgrids_conquered, player_idx, ai_idx, winner, reset, last_played } = data;

    // Atualiza Tabuleiro Principal
    board.forEach((val, i) => {
        const cell = document.getElementById(`cell-${i}`);
        const subId = Math.floor(i / 27) * 3 + Math.floor((i % 9) / 3);
        
        cell.className = 'cell'; 
        cell.innerText = val !== 0 ? val : "";

        if (last_played !== -1 && subId === last_played) cell.classList.add('blocked-subgrid');
        
        // Aplica apenas uma borda de destaque se o quadrante foi conquistado
        if (subgrids_conquered[subId] === 1) cell.classList.add('conquered-player');
        if (subgrids_conquered[subId] === 2) cell.classList.add('conquered-ai');
    });

    // Atualiza o Mini-Mapa (Tic-Tac-Toe)
    subgrids_conquered.forEach((owner, i) => {
        const miniCell = document.getElementById(`mini-${i}`);
        miniCell.className = 'mini-cell';
        if (owner === 1) { miniCell.innerText = "X"; miniCell.classList.add('x-conquered'); }
        else if (owner === 2) { miniCell.innerText = "O"; miniCell.classList.add('o-conquered'); }
        else { miniCell.innerText = ""; }
    });

    if (player_idx !== undefined) document.getElementById(`cell-${player_idx}`)?.classList.add('last-player-move');
    if (ai_idx !== null) document.getElementById(`cell-${ai_idx}`)?.classList.add('last-ai-move');

    if (reset) showToast("Quadrante limpo!");
    if (winner) { 
        alert(`Fim de jogo! Vencedor: ${winner === 1 ? 'Você' : 'Algoritmo'}`); 
        location.reload(); 
    }
}

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.querySelector('p').innerText = msg;
    t.classList.remove('hidden');
    if (window.toastTimer) clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => t.classList.add('hidden'), 5000);
}

window.onload = async () => {
    const res = await fetch('/get_board');
    const data = await res.json();
    atualizar(data);
};