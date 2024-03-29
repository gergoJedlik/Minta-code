import pygame
import random
import sqlite3
    

#kiírja a pontszámot jaték közben
def display_score():
    score_surf = game_font.render("pontszám: " + str(score), True, BLUE)
    score_rect = score_surf.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_surf, score_rect)

#kiírja a pontszámot és időt jaték után
def display_final_score():
    final_score_surf = game_font.render("PONTSZÁM: " + str(score), True, BLUE)
    final_score_rect = final_score_surf.get_rect(center=(WIDTH / 2, HEIGHT - 220))
    screen.blit(final_score_surf, final_score_rect)

#kiírja a időt jaték közben
def display_time_left():
    time_left_surf = game_font.render(
        "maradék idő: " + str(time_left), True, BLUE
    )
    time_left_rect = time_left_surf.get_rect(topright=(WIDTH - 10, 50))
    screen.blit(time_left_surf, time_left_rect)

#kiírja a életek számát játék közben
def display_lives_left():
    lives_left_surf = game_font.render(
        "Életek: " + str(lives), True, BLUE
    )
    lives_left_rect = lives_left_surf.get_rect(topleft=(10, 10))
    screen.blit(lives_left_surf, lives_left_rect)

def update_leader():
    if len(UserName) > 2:
        cur.execute(SQL_INSERT, (UserName, score))
        con.commit()

def get_leader_info() -> list[tuple[str, int]]:
    cur.execute(SQL_SELECT)
    return cur.fetchall()

def display_leaderboard(leader_db: list[tuple[str, int]]):
    printed_names: list[str] = []
    leader_surf = game_font.render(
        "Ranglista: ", True, BLUE
    )
    leader_rect = leader_surf.get_rect(topright = (WIDTH-10, 10))
    screen.blit(leader_surf, leader_rect)
    i = 1
    for item in leader_db:
        if item[0] not in printed_names and i <= 10:
            leader_surf = game_font.render(
                str(i) + ".   " + str(item[0]) + "    " + str(item[1]), True, BLUE
            )

            leader_rect = leader_surf.get_rect(topright = (WIDTH-10, 50*i))

            screen.blit(leader_surf, leader_rect)
            printed_names.append(item[0])
            i+=1



        


#legenerálja a hátteret
def BG_Generation():
    bg_surf = pygame.image.load("kepek/background.jpg").convert_alpha()
    bg_surf = pygame.transform.rotozoom(bg_surf, 0, 0.5)
    bg_rect = bg_surf.get_rect(bottomleft=(0, HEIGHT))
    return bg_surf, bg_rect

#Előkészíti a csillagokat a .blit()-elésre
def STAR_Setup():
    star_surf = pygame.image.load("kepek/star.png").convert_alpha()
    star_surf = pygame.transform.rotozoom(star_surf, 0, 0.3)
    stars_rect = [star_surf.get_rect(center=(random.randint(50, WIDTH - 50), HEIGHT - 60))]
    return star_surf, stars_rect

#Előkészíti a zsákot a .blit()-elésre
def SACK_Setup():
    sack_surf = pygame.image.load("kepek/sack.png").convert_alpha()
    sack_surf = pygame.transform.rotozoom(sack_surf, 0, 0.10)
    sack_rect = sack_surf.get_rect()
    return sack_surf, sack_rect


WIDTH = 1280
HEIGHT = 620
star_speed = 4
BLUE = (100, 100, 255)
game_time = 30000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Csillagvadászat")
clock = pygame.time.Clock()

bg_surf, bg_rect = BG_Generation()

star_surf, stars_rect = STAR_Setup()

#A sebességnövelés EVENT-jének létrehozása és ütemezése
speedup_timer = pygame.USEREVENT + 2
pygame.time.set_timer(speedup_timer, 5000)

#A csillagok megjelenítés EVENT-jének létrehozása és ütemezése
start_spawnrate = 800
new_spawnrate = 800
stars_timer = pygame.USEREVENT + 1
pygame.time.set_timer(stars_timer, start_spawnrate)

sack_surf, sack_rect = SACK_Setup()

#Kezdőképernyő előkészítése .blit()-elésre
game_font = pygame.font.SysFont("arial", 30, bold=True)
title_surf = game_font.render("CSILLAGVADÁSZAT", True, BLUE)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 200))
run_surf = game_font.render("Kezdéshez nyomd meg a szóközt!", True, BLUE)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT - 150))

con = sqlite3.connect("Leaderboard.db")
cur = con.cursor()
SQL_INSERT = "INSERT INTO leaderboard (name, score) VALUES (?, ?)"
SQL_CREATE = "CREATE TABLE leaderboard(name, score)"
SQL_SELECT = "SELECT name, score FROM leaderboard ORDER BY score DESC"

try:
    cur.execute(SQL_CREATE)
    print("--DATABASE CREATED--")
except:
    print("--DATABASE FOUND--")

user_text = '' 
input_rect = pygame.Rect(WIDTH//2 - 45, HEIGHT-90, 400, 50)  
color_active = pygame.Color('lightskyblue3') 
color_passive = BLUE 
color = color_passive
input_active = False

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
        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else: 
                    input_active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                update_leader()
                leaderboard_list = get_leader_info()
                game_active = False
            if not game_active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else: 
                    user_text += event.unicode
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
            star_speed += 1
            new_spawnrate -= 20

    screen.blit(bg_surf, bg_rect)


    if game_active:
        #Életek számlálása
        if lives <= 0:
            update_leader()
            leaderboard_list = get_leader_info()
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
                game_time += start_spawnrate-100


            screen.blit(star_surf, star_rect)
        screen.blit(sack_surf, sack_rect)        

        display_score()

        #idő lejárásának chekkolása
        time_left = int((start_time + game_time - pygame.time.get_ticks()) / 1000)
        if time_left < 1:
            update_leader()
            leaderboard_list = get_leader_info()
            game_active = False
        display_time_left()

        display_lives_left()

    else:
        #A kezdőképernyő .blit()-elése
        leaderboard_list = get_leader_info()
        display_leaderboard(leaderboard_list)

        screen.blit(title_surf, title_rect)
        screen.blit(star_surf, star_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(run_surf, run_rect)
        
        if score:
            display_final_score()

        #Input rect és színe
        if input_active:
            input_color = color_active
        else:
            input_color = color_passive
        pygame.draw.rect(screen, input_color, input_rect)
        text_surface = game_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
        input_rect.w = max(100, text_surface.get_width()+10) 
        pygame.display.flip()


        #Space lenyomására minden játékadat resetelése
        keys = pygame.key.get_pressed()
        if not input_active:
            if keys[pygame.K_SPACE]:
                game_time = 30000
                UserName = user_text.replace(" ", "")
                new_spawnrate = 800
                lives = 5
                star_speed = 4
                score = 0
                stars_rect = []
                start_time = pygame.time.get_ticks()
                game_active = True

    #játékablak frissítése
    pygame.display.update()
    clock.tick(60)

con.close()
pygame.quit()
quit()
