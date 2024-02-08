import pygame
import random


def display_score():
    score_surf = game_font.render("pontszám: " + str(score), True, FONT_COLOR)
    score_rect = score_surf.get_rect(topleft=(10, 10))
    screen.blit(score_surf, score_rect)


def display_final_score():
    final_score_surf = game_font.render("PONTSZÁM: " + str(score), True, FONT_COLOR)
    final_score_rect = final_score_surf.get_rect(center=(WIDTH / 2, HEIGHT - 220))
    screen.blit(final_score_surf, final_score_rect)


def display_time_left():
    time_left_surf = game_font.render(
        "maradék idő: " + str(time_left), True, FONT_COLOR
    )
    time_left_rect = time_left_surf.get_rect(topleft=(10, 50))
    screen.blit(time_left_surf, time_left_rect)


WIDTH = 1280
HEIGHT = 620
STAR_SPEED = 4
FONT_COLOR = (255, 255, 255)
GAME_TIME = 10000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Csillagvadászat")
clock = pygame.time.Clock()

bg_surf = pygame.image.load("kepek/background.jpg").convert_alpha()
bg_surf = pygame.transform.rotozoom(bg_surf, 0, 0.5)
bg_rect = bg_surf.get_rect(bottomleft=(0, HEIGHT))

star_surf = pygame.image.load("kepek/star.png").convert_alpha()
star_surf = pygame.transform.rotozoom(star_surf, 0, 0.3)
stars_rect = []
stars_timer = pygame.USEREVENT + 1
pygame.time.set_timer(stars_timer, 800)

sack_surf = pygame.image.load("kepek/sack.png").convert_alpha()
sack_surf = pygame.transform.rotozoom(sack_surf, 0, 0.15)


game_font = pygame.font.SysFont("arial", 30, bold=True)
title_surf = game_font.render("CSILLAGVADÁSZAT", True, FONT_COLOR)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 200))
run_surf = game_font.render("Kezdéshez nyomd meg a szóközt!", True, FONT_COLOR)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT - 150))

start_time = pygame.time.get_ticks()
score = 0
game_active = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            sack_rect = sack_surf.get_rect(center=event.pos)
        if event.type == stars_timer:
            stars_rect.append(
                star_surf.get_rect(center=(random.randint(50, WIDTH - 50), HEIGHT - 60))
            )

    screen.blit(bg_surf, bg_rect)

    if game_active:
        for index, star_rect in enumerate(stars_rect):
            stars_rect[index].bottom -= STAR_SPEED
            mov_y = random.randint(0, 3)
            if mov_y == 0:
                stars_rect[index].left -= 2
            else:
                stars_rect[index].left += 2
            if stars_rect[index].top <= -10:
                del stars_rect[index]
            if (
                star_rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_pressed(num_buttons=3)[0]
            ):
                del stars_rect[index]
                score += 1

        screen.blit(star_surf, star_rect)
        screen.blit(sack_surf, sack_rect)

        display_score()

        time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
        if time_left < 1:
            game_active = False
        display_time_left()

    else:
        screen.blit(title_surf, title_rect)
        screen.blit(star_surf, star_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(sack_surf, sack_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(run_surf, run_rect)

        if score:
            display_final_score()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            stars_rect = []
            start_time = pygame.time.get_ticks()
            game_active = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
