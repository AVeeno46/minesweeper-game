import pygame
import sys
import random
import time

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("지뢰찾기")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 게임 설정
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
NUM_MINES = 15

# 게임 변수 초기화
def reset_game():
    global grid, revealed, mines, flagged, game_over, game_won, start_time, elapsed_time
    
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    game_over = False
    game_won = False
    start_time = time.time()
    elapsed_time = 0
    
    # 지뢰 배치
    while len(mines) < NUM_MINES:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1
    
    # 주변 지뢰 개수 계산
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == -1:
                continue
            count = sum((nx, ny) in mines for dx in [-1, 0, 1] for dy in [-1, 0, 1] 
                        if 0 <= (nx := x + dx) < GRID_SIZE and 0 <= (ny := y + dy) < GRID_SIZE)
            grid[y][x] = count

# 빈 칸 자동 오픈
def flood_fill(x, y):
    if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or revealed[y][x] or flagged[y][x]:
        return
    revealed[y][x] = True
    if grid[y][x] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                flood_fill(x + dx, y + dy)

# 승리 조건 체크
def check_win():
    global game_won, elapsed_time
    if all(revealed[y][x] or (x, y) in mines for y in range(GRID_SIZE) for x in range(GRID_SIZE)):
        game_won = True
        elapsed_time = time.time() - start_time

# 버튼 생성 함수
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# 게임 초기화
reset_game()
clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            
            if game_over or game_won:
                if 100 <= x <= 300 and 200 <= y <= 250:
                    reset_game()
                elif 100 <= x <= 300 and 270 <= y <= 320:
                    running = False
            else:
                if event.button == 1:  # 좌클릭
                    if (grid_x, grid_y) in mines:
                        game_over = True
                    else:
                        flood_fill(grid_x, grid_y)
                        check_win()
                elif event.button == 3:  # 우클릭 (깃발 기능)
                    flagged[grid_y][grid_x] = not flagged[grid_y][grid_x]

    # 화면 그리기
    screen.fill(GRAY)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
            if revealed[y][x]:
                pygame.draw.rect(screen, WHITE, rect)
                if grid[y][x] > 0:
                    text = pygame.font.Font(None, 36).render(str(grid[y][x]), True, BLUE)
                    screen.blit(text, (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4))
            elif flagged[y][x]:
                pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE // 4)
            elif game_over and (x, y) in mines:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)

    # 타이머 표시 (오른쪽 상단으로 이동)
    if not game_over and not game_won:
        elapsed_time = time.time() - start_time
    timer_text = pygame.font.Font(None, 36).render(f"Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

    if game_over:
        font = pygame.font.Font(None, 72)
        text_surface = font.render("Game Over", True, RED)
        screen.blit(text_surface, (100, 100))
        draw_button("AGAIN", 100, 200, 200, 50, WHITE, BLACK)
        draw_button("OUT", 100, 270, 200, 50, WHITE, BLACK)
    elif game_won:
        font = pygame.font.Font(None, 72)
        text_surface = font.render("You Win!", True, BLUE)
        screen.blit(text_surface, (120, 100))
        draw_button("AGAIN", 100, 200, 200, 50, WHITE, BLACK)
        draw_button("OUT", 100, 270, 200, 50, WHITE, BLACK)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
