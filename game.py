import pygame
import random


def display_score():
    score_surf = game_font.render("pontszám: " + str(score), True, BLUE)
    score_rect = score_surf.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_surf, score_rect)


def display_final_score():
    final_score_surf = game_font.render("PONTSZÁM: " + str(score), True, BLUE)
    final_score_rect = final_score_surf.get_rect(center=(WIDTH / 2, HEIGHT - 220))
    screen.blit(final_score_surf, final_score_rect)


def display_time_left():
    time_left_surf = game_font.render(
        "maradék idő: " + str(time_left), True, BLUE
    )
    time_left_rect = time_left_surf.get_rect(topright=(WIDTH - 10, 50))
    screen.blit(time_left_surf, time_left_rect)

def display_lives_left():
    lives_left_surf = game_font.render(
        "Életek: " + str(lives), True, BLUE
    )
    lives_left_rect = lives_left_surf.get_rect(topleft=(10, 10))
    screen.blit(lives_left_surf, lives_left_rect)


def BG_Generation():
    bg_surf = pygame.image.load("kepek/background.jpg").convert_alpha()
    bg_surf = pygame.transform.rotozoom(bg_surf, 0, 0.5)
    bg_rect = bg_surf.get_rect(bottomleft=(0, HEIGHT))
    return bg_surf, bg_rect


def STAR_Setup():
    star_surf = pygame.image.load("kepek/star.png").convert_alpha()
    star_surf = pygame.transform.rotozoom(star_surf, 0, 0.3)
    stars_rect = [star_surf.get_rect(center=(random.randint(50, WIDTH - 50), HEIGHT - 60))]
    return star_surf, stars_rect


def SACK_Setup():
    sack_surf = pygame.image.load("kepek/sack.png").convert_alpha()
    sack_surf = pygame.transform.rotozoom(sack_surf, 0, 0.10)
    return sack_surf


WIDTH = 1280
HEIGHT = 620
star_speed = 4
BLUE = (100, 100, 255)
GAME_TIME = 30000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Csillagvadászat")
clock = pygame.time.Clock()

bg_surf, bg_rect = BG_Generation()

star_surf, stars_rect = STAR_Setup()

speedup_timer = pygame.USEREVENT + 2
pygame.time.set_timer(speedup_timer, 5000)

start_spawnrate = 800
new_spawnrate = 800
stars_timer = pygame.USEREVENT + 1
pygame.time.set_timer(stars_timer, start_spawnrate)

sack_surf = SACK_Setup()

game_font = pygame.font.SysFont("arial", 30, bold=True)
title_surf = game_font.render("CSILLAGVADÁSZAT", True, BLUE)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 200))
run_surf = game_font.render("Kezdéshez nyomd meg a szóközt!", True, BLUE)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT - 150))

start_time = pygame.time.get_ticks()
score = 0
lives = 5
game_active = False
running = True
while running:
    #Csillagok megjelenésének gyorsítása
    if start_spawnrate != new_spawnrate:
        start_spawnrate = new_spawnrate
        pygame.time.set_timer(stars_timer, start_spawnrate)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Curor lekövetése
        if event.type == pygame.MOUSEMOTION:
            sack_rect = sack_surf.get_rect(center=event.pos)
        #Csillagok listhoz csillag hozzáadás
        if event.type == stars_timer:
            stars_rect.append(
                star_surf.get_rect(center=(random.randint(50, WIDTH - 50), -80))
            )
        #Csillagok sebességének növelése
        if event.type == speedup_timer:
            star_speed += 2
            new_spawnrate -= 50

    screen.blit(bg_surf, bg_rect)

    if game_active:
        #Életek számlálása
        if lives <= 0:
            game_active = False
        #Csillagok kezelése
        for index, star_rect in enumerate(stars_rect):
            stars_rect[index].top += star_speed
            mov_y = random.randint(0, 3)
            if mov_y == 0:
                stars_rect[index].left -= 2
            else:
                stars_rect[index].left += 2
            if stars_rect[index].bottom >= HEIGHT + 10:
                lives -= 1
                del stars_rect[index]
            #Csillagra kattintás checkolása
            if (
                star_rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_pressed(num_buttons=3)[0]
            ):
                del stars_rect[index]
                score += 1

            screen.blit(star_surf, star_rect)
        screen.blit(sack_surf, sack_rect)        

        display_score()
        #idő lejárásának chekkolása
        time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
        if time_left < 1:
            game_active = False
        display_time_left()

        display_lives_left()

    else:
        screen.blit(title_surf, title_rect)
        screen.blit(star_surf, star_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(run_surf, run_rect)

        if score:
            display_final_score()
        #Space lenyomására minden játékadat resetelése
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            lives = 5
            star_speed = 4
            score = 0
            stars_rect = []
            start_time = pygame.time.get_ticks()
            game_active = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
