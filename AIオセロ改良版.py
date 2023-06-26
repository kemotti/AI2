import random

# ゲームボードの初期化
board = [[' ' for _ in range(8)] for _ in range(8)]
board[3][3] = '◯'
board[3][4] = '●'
board[4][3] = '●'
board[4][4] = '◯'

# 盤面の表示
def print_board(board):
    print('  1 2 3 4 5 6 7 8')
    for i in range(8):
        print(str(i+1) + ' ', end='')
        for j in range(8):
            print(board[i][j] + ' ', end='')
        print()

# 手の入力
def get_move():
    while True:
        move = input('次の手を入力してください（例: 3,4）: ')
        try:
            row, col = move.split(',')
            row = int(row.strip()) - 1
            col = int(col.strip()) - 1
            if row in range(8) and col in range(8):
                return row, col
            else:
                print('無効な手です。もう一度入力してください。')
        except ValueError:
            print('入力が無効です。もう一度入力してください。')

# 石の配置
def place_piece(board, row, col, piece):
    board[row][col] = piece

# 盤面の更新
def update_board(board, row, col, piece):
    # 各方向への変位
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # 裏返せる石を保持するリスト
    flip_list = []
    
    # 各方向に対して裏返せる石を探索
    for direction in directions:
        dx, dy = direction
        temp_list = []
        x, y = row, col
        x += dx
        y += dy
        
        # 隣接する石が敵の石の場合、探索を続ける
        while x in range(8) and y in range(8) and board[x][y] != ' ' and board[x][y] != piece:
            temp_list.append((x, y))
            x += dx
            y += dy
        
        # 探索した結果、裏返せる石が存在する場合、flip_listに追加
        if x in range(8) and y in range(8) and board[x][y] == piece:
            flip_list.extend(temp_list)
    
    # 裏返せる石を裏返す
    for flip in flip_list:
        fx, fy = flip
        board[fx][fy] = piece

# 有効な手の取得
def get_valid_moves(board, piece):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, piece):
                valid_moves.append((row, col))
    return valid_moves

# 有効な手の判定
def is_valid_move(board, row, col, piece):
    if board[row][col] != ' ':
        return False
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for direction in directions:
        dx, dy = direction
        x, y = row + dx, col + dy
        
        if x in range(8) and y in range(8) and board[x][y] != ' ' and board[x][y] != piece:
            x += dx
            y += dy
            while x in range(8) and y in range(8) and board[x][y] != ' ':
                if board[x][y] == piece:
                    return True
                x += dx
                y += dy
    
    return False

# AIの手の選択（ミニマックス法 + α-β枝刈り法）
def ai_move(board, piece):
    valid_moves = get_valid_moves(board, piece)
    best_move = None
    best_score = float('-inf')
    for move in valid_moves:
        new_board = [row[:] for row in board]
        row, col = move
        place_piece(new_board, row, col, piece)
        update_board(new_board, row, col, piece)
        score = minmax(new_board, piece, 3, False, float('-inf'), float('inf'))
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# ミニマックス法
def minmax(board, piece, depth, maximizing_player, alpha, beta):
    if depth == 0 or not get_valid_moves(board, piece):
        return evaluate(board, piece)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_valid_moves(board, piece):
            new_board = [row[:] for row in board]
            row, col = move
            place_piece(new_board, row, col, piece)
            update_board(new_board, row, col, piece)
            eval = minmax(new_board, piece, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent_piece = '◯' if piece == '●' else '●'
        for move in get_valid_moves(board, opponent_piece):
            new_board = [row[:] for row in board]
            row, col = move
            place_piece(new_board, row, col, opponent_piece)
            update_board(new_board, row, col, opponent_piece)
            eval = minmax(new_board, piece, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# 盤面の評価
def evaluate(board, piece):
    score = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                score += 1
    return score

# ゲームのメインループ
def play_game():
    print('=== オセロゲーム ===')
    print_board(board)
    
    while True:
        print('黒の手番です。')
        row, col = get_move()
        place_piece(board, row, col, '●')
        update_board(board, row, col, '●')
        print_board(board)
        
        if not get_valid_moves(board, '◯'):
            break
        
        print('白の手番です。')
        row, col = ai_move(board, '◯')
        place_piece(board, row, col, '◯')
        update_board(board, row, col, '◯')
        print_board(board)
        
        if not get_valid_moves(board, '●'):
            break

# ゲームの実行
play_game()