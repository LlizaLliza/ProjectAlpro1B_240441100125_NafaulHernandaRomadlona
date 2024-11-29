import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird Clone")

# Warna dan Kecepatan
background_color = (135, 206, 235)  # Warna biru langit
clock = pygame.time.Clock()

# Variabel untuk Game
gravity = 0.7
velocity = 0
player_jump = -10
player_x, player_y = 100, 300
score = 0
best_score = 0
game_active = False
menu_active = True
background_scroll_speed = 5

# Load Asset
try:
    background = pygame.image.load("assets/background_day.png").convert()
    bird = pygame.image.load("assets/bird.png").convert_alpha()
    pipe_surface = pygame.image.load("assets/pipe.png").convert_alpha()
except FileNotFoundError:
    print("Pastikan gambar background, bird, dan pipe ada di folder assets!")
    sys.exit()

# Ubah Ukuran Burung dan Pipa
bird = pygame.transform.scale(bird, (50, 50))  # Ukuran burung menjadi 50x50
pipe_surface = pygame.transform.scale(pipe_surface, (80, 500))  # Ukuran pipa menjadi 80x500
background = pygame.transform.scale(background, (800, 600))

# Posisikan Pipes
pipe_list = []
pipe_height = [400, 500, 600]

# Font
font = pygame.font.Font(None, 40)
smallfont = pygame.font.SysFont('Corbel', 40)

# Fungsi Membuat Pipe
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(900, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(900, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Fungsi Menampilkan Skor
def display_score():
    score_surface = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def display_best_score():
    best_score_surface = font.render(f"Best Score: {int(best_score)}", True, (255, 255, 255))
    screen.blit(best_score_surface, (10, 50))

# Game Loop
running = True
background_x = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Key Input untuk Game
        if event.type == pygame.KEYDOWN:
            if menu_active:
                if event.key == pygame.K_RETURN:  # Mulai permainan
                    menu_active = False
                    game_active = True
                    pipe_list.clear()
                    player_y = 300
                    velocity = 0
                    score = 0
                if event.key == pygame.K_q:  # Keluar dari game
                    running = False
            elif game_active:
                if event.key == pygame.K_SPACE:
                    velocity = player_jump
            else:
                if event.key == pygame.K_r:  # Restart game
                    game_active = True
                    pipe_list.clear()
                    player_y = 300
                    velocity = 0
                    score = 0
                if event.key == pygame.K_q:  # Quit dari game over
                    running = False

    # Background Scrolling
    background_x -= background_scroll_speed
    if background_x <= -800:
        background_x = 0

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 800, 0))

    if menu_active:
        # title_surface = font.render("Flappy Bird Clone", True, (255, 255, 255))
        start_surface = font.render(" Start", True, (47, 79, 79))
        quit_surface = font.render("Quit", True, (47, 79, 79))
        # screen.blit(title_surface, (300, 200))
        screen.blit(start_surface, (357, 175))
        screen.blit(quit_surface, (365, 250))

    elif game_active:
        # Gerakan Player
        velocity += gravity
        player_y += velocity
        player_rect = bird.get_rect(center=(player_x, player_y))

        # Tampilkan Player
        screen.blit(bird, player_rect)

        # Pipes
        if len(pipe_list) == 0 or pipe_list[-1].centerx < 600:
            pipe_list.extend(create_pipe())
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Tambah Skor
        score += 0.01
        display_score()

        # Deteksi Tabrakan
        if player_rect.top <= -50 or player_rect.bottom >= 600:
            game_active = False
            if score > best_score:
                best_score = int(score)
        for pipe in pipe_list:
            if player_rect.colliderect(pipe):
                game_active = False
                if score > best_score:
                    best_score = int(score)
    else:  # Game over
        game_over_surface = font.render("Game Over!", True, (255, 255, 255))
        restart_surface = font.render("Press R to Restart", True, (255, 255, 255))
        quit_surface = font.render("Press Q to Quit", True, (255, 255, 255))
        best_score_surface = font.render(f"Best Score: {int(best_score)}", True, (255, 255, 255))
        final_score_surface = font.render(f"Score: {int(score)}", True, (255, 255, 255))

        screen.blit(game_over_surface, (300, 200))
        screen.blit(final_score_surface, (300, 250))
        screen.blit(best_score_surface, (300, 300))
        screen.blit(restart_surface, (270, 350))
        screen.blit(quit_surface, (290, 400))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
