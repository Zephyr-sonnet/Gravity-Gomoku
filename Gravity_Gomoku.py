import pygame

# ===================== Global Config =====================
pygame.init()
COL = 11
ROW = 11
CELL_SIZE = 60
GAP = 1
WIDTH = COL * CELL_SIZE
TOP_MARGIN = 60
HEIGHT = ROW * CELL_SIZE + TOP_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Gomoku")

# Color define
BG_COLOR = (30, 30, 120)
WOOD_NORMAL = (160, 112, 68)
P1_COLOR = (0, 0, 0)
P2_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
BTN_COLOR = (60, 120, 220)
BTN_HOVER = (90, 160, 255)
ANN_COLOR = (50, 150, 250)

# Directions for win check
DIRS = [(-1, 0), (0, 1), (-1, 1), (-1, -1)]

# Game state enum
STATE_HOME = 0
STATE_GAME = 1
STATE_HELP = 2
STATE_AI = 3
STATE_AI_SELECT = 4
AI_DIFFICULTY = 4
DIFFICULTY_DEPTH = {'EASY': 4, 'MEDIUM': 5, 'HARD': 6}
game_state = STATE_HOME
AI_PLAYER = 2

# Board & game data
board = [[0 for _ in range(COL)] for _ in range(ROW)]
current_player = 1
game_over = False
step_stack = []  # Stack for undo move (LIFO)

# Font
font_large = pygame.font.SysFont(None, 70)
font_mid = pygame.font.SysFont(None, 45)
font_small = pygame.font.SysFont(None, 32)

clock = pygame.time.Clock()

# ===================== Draw Start Home Page =====================
def draw_home():
    SCREEN.fill(BG_COLOR)
    # Title
    title = font_large.render("Gravity Gomoku", True, TEXT_COLOR)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//6))

    # Two Players Button
    btn_w, btn_h = 220, 70
    btn_x_start = WIDTH//2 - btn_w//2
    btn_y_start = HEIGHT//2 - 90
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Start button
    if btn_x_start <= mouse_x <= btn_x_start+btn_w and btn_y_start <= mouse_y <= btn_y_start+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x_start, btn_y_start, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x_start, btn_y_start, btn_w, btn_h), border_radius=12)
    btn_text_start = font_mid.render("TWO PLAYERS", True, TEXT_COLOR)
    SCREEN.blit(btn_text_start, (WIDTH//2 - btn_text_start.get_width()//2, btn_y_start + 12))

    # VS AI Button
    btn_x_help = WIDTH//2 - btn_w//2
    btn_y_help = HEIGHT//2 + 20
    if btn_x_help <= mouse_x <= btn_x_help+btn_w and btn_y_help <= mouse_y <= btn_y_help+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x_help, btn_y_help, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x_help, btn_y_help, btn_w, btn_h), border_radius=12)
    btn_text_help = font_mid.render("VS AI PLAYER", True, TEXT_COLOR)
    SCREEN.blit(btn_text_help, (WIDTH//2 - btn_text_help.get_width()//2, btn_y_help + 12))

    # How To Play Button
    btn_y_ai = HEIGHT//2 + 130
    if btn_x_help <= mouse_x <= btn_x_help+btn_w and btn_y_ai <= mouse_y <= btn_y_ai+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x_help, btn_y_ai, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x_help, btn_y_ai, btn_w, btn_h), border_radius=12)
    btn_text_ai = font_mid.render("HOW TO PLAY", True, TEXT_COLOR)
    SCREEN.blit(btn_text_ai, (WIDTH//2 - btn_text_ai.get_width()//2, btn_y_ai + 12))

    pygame.display.update()
    return btn_x_start, btn_y_start, btn_w, btn_h, btn_x_help, btn_y_help, btn_y_ai

# ===================== Draw Help Rule Page =====================
def draw_help():
    SCREEN.fill(BG_COLOR)
    title = font_large.render("Game Rules", True, TEXT_COLOR)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    rules = [
        "1. Two players take turns to drop pieces.",
        "2. Click any column, piece falls to the bottom.",
        "3. Player 1: BLACK, Player 2: WHITE.",
        "4. First to connect 5 pieces in a line wins.",
        "5. Lines can be horizontal, vertical or diagonal.",
        "6. Press U to undo your last move.",
        "7. Press R to restart a new game.",
        "8. If the board is full with no winner, it's a draw.",
        "9. You always go first when you play with AI."
    ]
    y_offset = 130
    for line in rules:
        text = font_small.render(line, True, TEXT_COLOR)
        SCREEN.blit(text, (40, y_offset))
        y_offset += 42

    # Back button top-right
    btn_w, btn_h = 160, 60
    btn_x = WIDTH - btn_w - 20
    btn_y = 30
    mx, my = pygame.mouse.get_pos()
    if btn_x <= mx <= btn_x+btn_w and btn_y <= my <= btn_y+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x, btn_y, btn_w, btn_h), border_radius=10)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x, btn_y, btn_w, btn_h), border_radius=10)
    back_text = font_mid.render("BACK", True, TEXT_COLOR)
    SCREEN.blit(back_text, (btn_x + (btn_w - back_text.get_width())//2, btn_y + 8))

    pygame.display.update()
    return btn_x, btn_y, btn_w, btn_h

# ===================== Draw AI_SELECT Page =====================
def draw_ai_select():
    SCREEN.fill(BG_COLOR)
    title = font_large.render("Select Difficulty", True, TEXT_COLOR)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//6))

    btn_w, btn_h = 220, 70
    btn_x = WIDTH//2 - btn_w//2
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Easy
    btn_y_easy = HEIGHT//2 - 100
    if btn_x <= mouse_x <= btn_x+btn_w and btn_y_easy <= mouse_y <= btn_y_easy+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x, btn_y_easy, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x, btn_y_easy, btn_w, btn_h), border_radius=12)
    txt_easy = font_mid.render("EASY", True, TEXT_COLOR)
    SCREEN.blit(txt_easy, (WIDTH//2 - txt_easy.get_width()//2, btn_y_easy + 12))

    # Medium
    btn_y_mid = HEIGHT//2
    if btn_x <= mouse_x <= btn_x+btn_w and btn_y_mid <= mouse_y <= btn_y_mid+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x, btn_y_mid, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x, btn_y_mid, btn_w, btn_h), border_radius=12)
    txt_mid = font_mid.render("MEDIUM", True, TEXT_COLOR)
    SCREEN.blit(txt_mid, (WIDTH//2 - txt_mid.get_width()//2, btn_y_mid + 12))

    # Hard
    btn_y_hard = HEIGHT//2 + 100
    if btn_x <= mouse_x <= btn_x+btn_w and btn_y_hard <= mouse_y <= btn_y_hard+btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (btn_x, btn_y_hard, btn_w, btn_h), border_radius=12)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (btn_x, btn_y_hard, btn_w, btn_h), border_radius=12)
    txt_hard = font_mid.render("HARD", True, TEXT_COLOR)
    SCREEN.blit(txt_hard, (WIDTH//2 - txt_hard.get_width()//2, btn_y_hard + 12))

    # Top right back button
    back_w, back_h = 130, 50
    back_x = WIDTH - back_w - 10
    back_y = 10
    if back_x <= mouse_x <= back_x+back_w and back_y <= mouse_y <= back_y+back_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (back_x, back_y, back_w, back_h), border_radius=8)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (back_x, back_y, back_w, back_h), border_radius=8)
    back_txt = font_small.render("BACK", True, TEXT_COLOR)
    SCREEN.blit(back_txt, (back_x + (back_w - back_txt.get_width())//2, back_y + 10))

    pygame.display.update()
    return btn_x, btn_y_easy, btn_y_mid, btn_y_hard, back_x, back_y, back_w, back_h


# ===================== Draw Game Board =====================
def draw_board():
    SCREEN.fill(BG_COLOR)

    # Top right BACK button
    btn_w, btn_h = 130, 50
    back_btn_x = WIDTH - btn_w - 10
    back_btn_y = 5
    mx, my = pygame.mouse.get_pos()
    if back_btn_x <= mx <= back_btn_x + btn_w and back_btn_y <= my <= back_btn_y + btn_h:
        pygame.draw.rect(SCREEN, BTN_HOVER, (back_btn_x, back_btn_y, btn_w, btn_h), border_radius=8)
    else:
        pygame.draw.rect(SCREEN, BTN_COLOR, (back_btn_x, back_btn_y, btn_w, btn_h), border_radius=8)
    back_text = font_small.render("BACK", True, TEXT_COLOR)
    SCREEN.blit(back_text, (back_btn_x + (btn_w - back_text.get_width())//2, back_btn_y + 10))

    # Top left tip text
    if not game_over:
        tip = font_small.render(f"Current Player: {current_player}", True, TEXT_COLOR)
    else:
        tip = font_small.render("Game Over! Press R to restart", True, TEXT_COLOR)
    SCREEN.blit(tip, (10, 15))

    # Draw board with top margin offset
    for y in range(ROW):
        for x in range(COL):
            rect = pygame.Rect(
                x * CELL_SIZE + GAP,
                y * CELL_SIZE + GAP + TOP_MARGIN,
                CELL_SIZE - 2 * GAP,
                CELL_SIZE - 2 * GAP
            )
            pygame.draw.rect(SCREEN, WOOD_NORMAL, rect, border_radius=8)
            # Draw pieces
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = y * CELL_SIZE + CELL_SIZE // 2 + TOP_MARGIN
            r = (CELL_SIZE - 10) // 2
            if board[y][x] == 1:
                pygame.draw.circle(SCREEN, P1_COLOR, (cx, cy), r)
            elif board[y][x] == 2:
                pygame.draw.circle(SCREEN, P2_COLOR, (cx, cy), r)

    pygame.display.update()
    return back_btn_x, back_btn_y, btn_w, btn_h

# ===================== Core Function =====================
def get_drop_row(col):
    """Return lowest empty row in target column, -1 if full"""
    for y in range(ROW-1, -1, -1):
        if board[y][col] == 0:
            return y
    return -1

def check_win(x, y, player):
    """Check if current piece forms 5 in a line"""
    for dy, dx in DIRS:
        count = 1
        # Forward
        ny, nx = y + dy, x + dx
        while 0 <= ny < ROW and 0 <= nx < COL and board[ny][nx] == player:
            count += 1
            ny += dy
            nx += dx
        # Backward
        ny, nx = y - dy, x - dx
        while 0 <= ny < ROW and 0 <= nx < COL and board[ny][nx] == player:
            count += 1
            ny -= dy
            nx -= dx
        if count >= 5:
            return True
    return False

def reset_game():
    """Reset all game status to initial"""
    global board, current_player, game_over, step_stack
    board = [[0]*COL for _ in range(ROW)]
    current_player = 1
    game_over = False
    step_stack.clear()
    draw_board()

def undo_step():
    """人机对战时，一次性撤回人类+AI两步；双人只撤一步"""
    global current_player, game_state
    if len(step_stack) == 0 or game_over:
        return
    # 双人模式：只撤销1步
    if game_state == STATE_GAME:
        y, x, old_player = step_stack.pop()
        board[y][x] = 0
        current_player = old_player
    # AI模式：连续弹出两步（玩家一步 + AI一步）
    elif game_state == STATE_AI:
        # 先弹AI
        y1, x1, _ = step_stack.pop()
        board[y1][x1] = 0
        # 再弹玩家
        y2, x2, old_p = step_stack.pop()
        board[y2][x2] = 0
        current_player = 1
    draw_board()

# ===================== AI Logic =====================
def count_consecutive(x, y, dx, dy, target_p):
    cnt = 0
    cx, cy = x + dx, y + dy
    while 0 <= cx < COL and 0 <= cy < ROW and board[cy][cx] == target_p:
        cnt += 1
        cx += dx
        cy += dy
    return cnt

def is_open(x, y, dx, dy):
    cx, cy = x + dx, y + dy
    if 0 <= cx < COL and 0 <= cy < ROW and board[cy][cx] == 0:
        return True
    return False

def evaluate_board(player):
    score = 0
    center = COL // 2
    human = 1
    ai = player

    # 子函数：打分，防守威胁权重 > 自身普通进攻
    def get_val(is_ai, total, open_both):
        if is_ai:
            # AI自己的棋（进攻分）
            if total >= 5:
                return 100000
            elif total == 4 and open_both:
                return 8000
            elif total == 4:
                return 5000
            elif total == 3 and open_both:
                return 3000
            elif total == 3:
                return 1000
            elif total == 2 and open_both:
                return 300
            elif total == 2:
                return 100
            else:
                return 20
        else:
            # 人类棋子（防守扣分，权重更高）
            if total >= 5:
                return -100000
            elif total == 4 and open_both:
                return -9000   # 对手活四，优先级最高
            elif total == 4:
                return -6000
            elif total == 3 and open_both:
                return -3500   # 对手活三 > AI普通三
            elif total == 3:
                return -1500
            elif total == 2 and open_both:
                return -350
            elif total == 2:
                return -120
            else:
                return -20

    for y in range(ROW):
        for x in range(COL):
            piece = board[y][x]
            if piece == 0:
                continue
            current_is_ai = (piece == ai)

            for dy, dx in DIRS:
                forward = count_consecutive(x, y, dx, dy, piece)
                backward = count_consecutive(x, y, -dx, -dy, piece)
                total = forward + backward + 1
                open_f = is_open(x, y, dx, dy)
                open_b = is_open(x, y, -dx, -dy)
                val = get_val(current_is_ai, total, open_f and open_b)
                score += val

            # 中心位置加分，鼓励AI占中间
            dist = abs(x - center) + abs(y - center)
            if current_is_ai:
                score += max(0, 30 - dist * 4)
    return score

# Minimax Alpha-Beta递归推演
def minimax(depth, alpha, beta, is_max, ai_p, human_p):
    full = True
    for c in range(COL):
        if get_drop_row(c) != -1:
            full = False
            break
    if full or depth == 0:
        return evaluate_board(ai_p)
    if is_max:
        max_val = -float('inf')
        for c in range(COL):
            r = get_drop_row(c)
            if r == -1:
                continue
            board[r][c] = ai_p
            cur = minimax(depth - 1, alpha, beta, False, ai_p, human_p)
            board[r][c] = 0
            max_val = max(max_val, cur)
            alpha = max(alpha, cur)
            if alpha >= beta:
                break
        return max_val
    else:
        min_val = float('inf')
        for c in range(COL):
            r = get_drop_row(c)
            if r == -1:
                continue
            board[r][c] = human_p
            cur = minimax(depth - 1, alpha, beta, True, ai_p, human_p)
            board[r][c] = 0
            min_val = min(min_val, cur)
            beta = min(beta, cur)
            if alpha >= beta:
                break
        return min_val

def ai_get_best_col():
    ai_p = AI_PLAYER
    human_p = 1
    best_col = COL // 2
    best_score = -float('inf')
    search_depth = AI_DIFFICULTY  # 读取选择的难度深度

    for c in range(COL):
        r = get_drop_row(c)
        if r == -1:
            continue
        board[r][c] = ai_p
        val = minimax(search_depth - 1, -float('inf'), float('inf'), False, ai_p, human_p)
        board[r][c] = 0
        if val > best_score:
            best_score = val
            best_col = c
    return best_col

# ===================== Main Game Loop =====================
def main():
    global game_state, current_player, game_over
    while True:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # ========== Home Page Logic ==========
            if game_state == STATE_HOME:
                bx1, by1, bw, bh, bx2, by2, by_ai = draw_home()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Click Two Players
                    if bx1 <= mx <= bx1+bw and by1 <= my <= by1+bh:
                        game_state = STATE_GAME
                        reset_game()
                    # Click VS AI PLAYER
                    if bx2 <= mx <= bx2+bw and by2 <= my <= by2+bh:
                        game_state = STATE_AI_SELECT
                    # Click how to play
                    if bx2 <= mx <= bx2+bw and by_ai <= my <= by_ai+bh:
                        game_state = STATE_HELP

            # ========== Help Rule Page Logic ==========
            elif game_state == STATE_HELP:
                btx, bty, btw, bth = draw_help()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if btx <= mx <= btx+btw and bty <= my <= bty+bth:
                        game_state = STATE_HOME

            # ========== AI Difficulty Select Page ==========
            elif game_state == STATE_AI_SELECT:
                bx, by_e, by_m, by_h, bk_x, bk_y, bk_w, bk_h = draw_ai_select()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Back to home
                    if bk_x <= mx <= bk_x + bk_w and bk_y <= my <= bk_y + bk_h:
                        game_state = STATE_HOME
                        continue
                    # Easy
                    if bx <= mx <= bx+220 and by_e <= my <= by_e+70:
                        global AI_DIFFICULTY
                        AI_DIFFICULTY = DIFFICULTY_DEPTH["EASY"]
                        game_state = STATE_AI
                        reset_game()
                    # Medium
                    if bx <= mx <= bx+220 and by_m <= my <= by_m+70:
                        AI_DIFFICULTY = DIFFICULTY_DEPTH["MEDIUM"]
                        game_state = STATE_AI
                        reset_game()
                    # Hard
                    if bx <= mx <= bx+220 and by_h <= my <= by_h+70:
                        AI_DIFFICULTY = DIFFICULTY_DEPTH["HARD"]
                        game_state = STATE_AI
                        reset_game()

            # ========== Two Player Game Logic ==========
            elif game_state == STATE_GAME:
                if not game_over:
                    back_x, back_y, back_w, back_h = draw_board()
                else:
                    btn_w, btn_h = 130, 50
                    back_x = WIDTH - btn_w - 10
                    back_y = 5
                    back_w = btn_w
                    back_h = btn_h

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Back home button
                    if back_x <= mx <= back_x + back_w and back_y <= my <= back_y + back_h:
                        game_state = STATE_HOME
                        continue
                    # Drop piece
                    if not game_over:
                        click_col = mx // CELL_SIZE
                        if 0 <= click_col < COL:
                            drop_y = get_drop_row(click_col)
                            if drop_y != -1:
                                board[drop_y][click_col] = current_player
                                step_stack.append((drop_y, click_col, current_player))
                                draw_board()
                                if check_win(click_col, drop_y, current_player):
                                    game_over = True
                                    win_text = font_large.render(f"Player {current_player} Win!", True, ANN_COLOR)
                                    SCREEN.blit(win_text, (WIDTH//2-win_text.get_width()//2, HEIGHT//2-40))
                                    pygame.display.update()
                                elif all(board[0][c] != 0 for c in range(COL)):
                                    game_over = True
                                    draw_text = font_large.render("Draw! Board Full", True, ANN_COLOR)
                                    SCREEN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2, HEIGHT//2-40))
                                    pygame.display.update()
                                else:
                                    current_player = 2 if current_player == 1 else 1
                # Hotkey
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                    if event.key == pygame.K_u and not game_over:
                        undo_step()

            # ========== VS AI Game Logic ==========
            elif game_state == STATE_AI:
                if not game_over:
                    back_x, back_y, back_w, back_h = draw_board()
                else:
                    btn_w, btn_h = 130, 50
                    back_x = WIDTH - btn_w - 10
                    back_y = 5
                    back_w = btn_w
                    back_h = btn_h

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if back_x <= mx <= back_x + back_w and back_y <= my <= back_y + back_h:
                        game_state = STATE_HOME
                        continue
                    # Only human can drop when it's his turn
                    if not game_over and current_player == 1:
                        click_col = mx // CELL_SIZE
                        if 0 <= click_col < COL:
                            drop_y = get_drop_row(click_col)
                            if drop_y != -1:
                                board[drop_y][click_col] = 1
                                step_stack.append((drop_y, click_col, 1))
                                draw_board()
                                if check_win(click_col, drop_y, 1):
                                    game_over = True
                                    win_text = font_large.render("You Win!", True, ANN_COLOR)
                                    SCREEN.blit(win_text, (WIDTH//2-win_text.get_width()//2, HEIGHT//2-40))
                                    pygame.display.update()
                                elif all(board[0][c] != 0 for c in range(COL)):
                                    game_over = True
                                    draw_text = font_large.render("Draw! Board Full", True, ANN_COLOR)
                                    SCREEN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2, HEIGHT//2-40))
                                    pygame.display.update()
                                else:
                                    current_player = AI_PLAYER
                                    # AI move
                                    ai_col = ai_get_best_col()
                                    ai_y = get_drop_row(ai_col)
                                    board[ai_y][ai_col] = AI_PLAYER
                                    step_stack.append((ai_y, ai_col, AI_PLAYER))
                                    draw_board()
                                    if check_win(ai_col, ai_y, AI_PLAYER):
                                        game_over = True
                                        win_text = font_large.render("AI Win!", True, ANN_COLOR)
                                        SCREEN.blit(win_text, (WIDTH//2-win_text.get_width()//2, HEIGHT//2-40))
                                        pygame.display.update()
                                    elif all(board[0][c] != 0 for c in range(COL)):
                                        game_over = True
                                        draw_text = font_large.render("Draw! Board Full", True, ANN_COLOR)
                                        SCREEN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2, HEIGHT//2-40))
                                        pygame.display.update()
                                    current_player = 1
                # Hotkey
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                    if event.key == pygame.K_u and not game_over:
                        undo_step()

if __name__ == "__main__":
    main()
