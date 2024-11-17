import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran Window
WIDTH, HEIGHT = 400, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sliding Puzzle by Jasen')

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Ukuran grid puzzle
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE

# Menyusun tiles
tiles = [i for i in range(1, GRID_SIZE * GRID_SIZE)] + [None]

# Frame rate
clock = pygame.time.Clock()
FPS = 30

# Fungsi untuk menggambar grid puzzle
def draw_grid():
    window.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile = tiles[i * GRID_SIZE + j]
            if tile is not None:
                pygame.draw.rect(window, BLACK, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 60)
                text = font.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                window.blit(text, text_rect)
            else:
                pygame.draw.rect(window, GRAY, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Fungsi untuk menangani pergerakan tile
def move_tile(pos):
    x, y = pos
    idx = y * GRID_SIZE + x
    empty_idx = tiles.index(None)
    empty_x, empty_y = empty_idx % GRID_SIZE, empty_idx // GRID_SIZE

    # Pindahkan tile jika bersebelahan dengan tile kosong
    if(abs(empty_x - x) == 1 and empty_y == y) or (abs(empty_y - y) == 1 and empty_x == x):
        tiles[empty_idx], tiles[idx] = tiles[idx], tiles[empty_idx]

def shuffle_tiles():
    random.shuffle(tiles)
    while not is_solvable(tiles) or check_win():
        random.shuffle(tiles)

def is_solvable(tiles):
    inversions = 0
    tile_list = [tile for tile in tiles if tile is not None]
    for i in range(len(tile_list)):
        for j in range(i + 1, len(tile_list)):
            if tile_list[i] > tile_list[j]:
                inversions += 1
    return inversions % 2 == 0

def check_win():
    return tiles == [i for i in range(1, GRID_SIZE * GRID_SIZE)] + [None]

# Memanggil shuffle pada saat permainan dimulai
shuffle_tiles()

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= TILE_SIZE
            y //= TILE_SIZE
            move_tile((x, y))
    draw_grid()
    pygame.display.flip()
    clock.tick(FPS)

    # Cek apakah pemain menang
    if check_win():
        print("You Win!")
        running = False


pygame.quit()