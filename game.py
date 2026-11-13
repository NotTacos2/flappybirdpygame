import pygame
import os
import sys
import json
import random

pygame.init()
clock = pygame.time.Clock()

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists("flappybirdsavefile.json"):
    with open("flappybirdsavefile.json", "r") as file:
        data = json.load(file)
        highscore = data["highscore"]
        totalscore = data["totalscore"]
        selected = data["selected"]
        deaths = data["deaths"]
        clicks = data["clicks"]
        achievementoneunlocked = data["achievementoneunlocked"]
        achievementtwounlocked = data["achievementtwounlocked"]
else:
    highscore = 0 
    totalscore = 0
    selected = 0
    deaths = 0
    clicks = 0
    achievementoneunlocked = False
    achievementtwounlocked = False

score = 0

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Flappy Bird")

exitbutton = pygame.surface.Surface((200, 50))
exitbutton.fill((0, 0, 0))

playbutton = pygame.surface.Surface((200, 50))
playbutton.fill((0, 0, 0))

settingsbutton = pygame.surface.Surface((200, 50))
settingsbutton.fill((0, 0, 0))

backbutton = pygame.surface.Surface((200, 50))
backbutton.fill((0, 0, 0))

statsbutton = pygame.surface.Surface((200, 50))
statsbutton.fill((0, 0, 0))

resetbutton = pygame.surface.Surface((200, 50))
resetbutton.fill((0, 0, 0))

skinbutton = pygame.surface.Surface((200, 50))
skinbutton.fill((0, 0, 0))

achievementbutton = pygame.surface.Surface((250, 50))
achievementbutton.fill((0, 0, 0))

font = pygame.font.SysFont(None, 48)
smallfont = pygame.font.SysFont(None, 34)
titlefont = font.render("Flappy Bird", True, (0, 0, 0))
exitfont = font.render("Exit Game", True, (255, 255, 255))
settingsfont = font.render("Settings", True, (255, 255, 255))
playfont = font.render("Play Game", True, (255, 255, 255))
backfont = font.render("Go Back", True, (255, 255, 255))
scorefont = font.render("Score: " + str(score), True, (0, 0, 0))
highscorefont = font.render("You got a new highscore of " + str(highscore), True, (0, 0, 0))
gameoverfont = font.render("Game over!", True, (0, 0, 0))
tryagainfont = font.render("Try again? (Press R)", True, (0, 0, 0))
trytoquitfont = font.render("Or quit (press esc)", True, (0, 0, 0))
statsfont = font.render("Stats", True, (255, 255, 255))
resetfont = font.render("Reset save", True, (255, 255, 255))
skinfont = font.render("Skins", True, (255, 255, 255))
totalclickedfont = font.render("You have clicked " + str(clicks) + " times", True, (0, 0, 0))
highscorestatfont = font.render("Your high score is " + str(highscore), True, (0, 0, 0))
deathsfont = font.render("You have died " + str(deaths) + " times", True, (0, 0, 0))
totalscorefont = font.render("Your total score gained is " + str(totalscore), True, (0, 0, 0))
statsstatfont = font.render("Stats", True, (0, 0, 0))
achievementsfont = font.render("Achievements", True, (255, 255, 255))
achievementstextfont = font.render("Achievements", True, (0, 0, 0))
achievementsonetitlefont = font.render("???", True, (0, 0, 0))
achievementsonedescfont = smallfont.render("Reach a specific amount of highscore to get this", True, (0, 0, 0))
achievementstwotitlefont = font.render("???", True, (0, 0, 0))
achievementstwodescfont = smallfont.render("Reach a specific amount of clicks to get this", True, (0, 0, 0))
skinstextfont = font.render("Skins", True, (0, 0, 0))
currentlyselectedfont = font.render("Current selected: Default Yellow Bird", True, (0, 0, 0))

exitbutton_x = 300
exitbutton_y = 350
exit_interact = exitbutton.get_rect(topleft=(exitbutton_x, exitbutton_y))

settingsbutton_x = 300
settingsbutton_y = 290
settings_interact = settingsbutton.get_rect(topleft=(settingsbutton_x, settingsbutton_y))

backbutton_x = 0
backbutton_y = 0
back_interact = backbutton.get_rect(topleft=(backbutton_x, backbutton_y))

playbutton_x = 300
playbutton_y = 230
play_interact = playbutton.get_rect(topleft=(playbutton_x, playbutton_y))

statsbutton_x = 600
statsbutton_y = 0
stats_interact = statsbutton.get_rect(topleft=(statsbutton_x, statsbutton_y))

achievementbutton_x = 550
achievementbutton_y = 100
achievement_interact = achievementbutton.get_rect(topleft=(achievementbutton_x, achievementbutton_y))

resetbutton_x = 300
resetbutton_y = 250
reset_interact = resetbutton.get_rect(topleft=(resetbutton_x, resetbutton_y))

skinbutton_x = 50
skinbutton_y = 50
skin_interact = skinbutton.get_rect(topleft=(skinbutton_x, skinbutton_y))

bird_x = 100
bird_y = 300
pipe_x = 800
pipe_top = 0
pipe_bottom = 0
didwepasspipe = False
bird_velocity = 0
gravity = 0.5
flap_force = -8
gameover = False

game_state = 1

bird = pygame.surface.Surface((50, 50))
bird.fill((255, 255, 255))
bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "defaultbird.png")).convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))
if selected == 1:
    currentlyselectedfont = font.render("Current selected: Blue Bird", True, (0, 0, 0))
    bird = pygame.surface.Surface((50, 50))
    bird.fill((255, 255, 255))
    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "bluebird.png")).convert_alpha()
    bird = pygame.transform.scale(bird, (50, 50))
if selected == 2:
    currentlyselectedfont = font.render("Current selected: Cyan Bird", True, (0, 0, 0))
    bird = pygame.surface.Surface((50, 50))
    bird.fill((255, 255, 255))
    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "cyanbird.png")).convert_alpha()
    bird = pygame.transform.scale(bird, (50, 50))
if selected == 3:
    currentlyselectedfont = font.render("Current selected: Green Bird", True, (0, 0, 0))
    bird = pygame.surface.Surface((50, 50))
    bird.fill((255, 255, 255))
    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "greenbird.png")).convert_alpha()
    bird = pygame.transform.scale(bird, (50, 50))
if selected == 4:
    currentlyselectedfont = font.render("Current selected: Pink Bird", True, (0, 0, 0))
    bird = pygame.surface.Surface((50, 50))
    bird.fill((255, 255, 255))
    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "pinkbird.png")).convert_alpha()
    bird = pygame.transform.scale(bird, (50, 50))
if selected == 5:
    currentlyselectedfont = font.render("Current selected: Red Bird", True, (0, 0, 0))
    bird = pygame.surface.Surface((50, 50))
    bird.fill((255, 255, 255))
    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "redbird.png")).convert_alpha()
    bird = pygame.transform.scale(bird, (50, 50))

lockedachievement = pygame.surface.Surface((75, 75))
lockedachievement.fill((255, 255, 255))
lockedachievement = pygame.image.load(os.path.join(BASE_DIR, "imgs", "locked.png")).convert_alpha()
lockedachievement = pygame.transform.scale(lockedachievement, (75, 75))

achievementone = pygame.surface.Surface((75, 75))
achievementone.fill((255, 255, 255))
achievementone = pygame.image.load(os.path.join(BASE_DIR, "imgs", "achievement1.png")).convert_alpha()
achievementone = pygame.transform.scale(achievementone, (75, 75))

achievementtwo = pygame.surface.Surface((75, 75))
achievementtwo.fill((255, 255, 255))
achievementtwo = pygame.image.load(os.path.join(BASE_DIR, "imgs", "achievement2.png")).convert_alpha()
achievementtwo = pygame.transform.scale(achievementtwo, (75, 75))

defaultbird = pygame.surface.Surface((60, 60))
defaultbird.fill((255, 255, 255))
defaultbird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "defaultbird.png")).convert_alpha()
defaultbird = pygame.transform.scale(defaultbird, (60, 60))

bluebird = pygame.surface.Surface((60, 60))
bluebird.fill((255, 255, 255))
bluebird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "bluebird.png")).convert_alpha()
bluebird = pygame.transform.scale(bluebird, (60, 60))

cyanbird = pygame.surface.Surface((60, 60))
cyanbird.fill((255, 255, 255))
cyanbird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "cyanbird.png")).convert_alpha()
cyanbird = pygame.transform.scale(cyanbird, (60, 60))

greenbird = pygame.surface.Surface((60, 60))
greenbird.fill((255, 255, 255))
greenbird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "greenbird.png")).convert_alpha()
greenbird = pygame.transform.scale(greenbird, (60, 60))

pinkbird = pygame.surface.Surface((60, 60))
pinkbird.fill((255, 255, 255))
pinkbird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "pinkbird.png")).convert_alpha()
pinkbird = pygame.transform.scale(pinkbird, (60, 60))

redbird = pygame.surface.Surface((60, 60))
redbird.fill((255, 255, 255))
redbird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "redbird.png")).convert_alpha()
redbird = pygame.transform.scale(redbird, (60, 60))

defaultbird_x = 100
defaultbird_y = 150
defaultbird_interact = defaultbird.get_rect(topleft=(defaultbird_x, defaultbird_y))

bluebird_x = 300
bluebird_y = 150
bluebird_interact = bluebird.get_rect(topleft=(bluebird_x, bluebird_y))

cyanbird_x = 500
cyanbird_y = 150
cyanbird_interact = cyanbird.get_rect(topleft=(cyanbird_x, cyanbird_y))

greenbird_x = 100
greenbird_y = 300
greenbird_interact = greenbird.get_rect(topleft=(greenbird_x, greenbird_y))

pinkbird_x = 300
pinkbird_y = 300
pinkbird_interact = pinkbird.get_rect(topleft=(pinkbird_x, pinkbird_y))

redbird_x = 500
redbird_y = 300
redbird_interact = redbird.get_rect(topleft=(redbird_x, redbird_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_interact.collidepoint(event.pos):
                    sys.exit()
                elif play_interact.collidepoint(event.pos):
                    game_state = 2
                    bird_y = 300
                    bird_velocity = 0
                    score = 0
                    pipe_x = 800
                    pipe_top = random.randint(50, 400)
                    pipe_bottom = pipe_top + 200
                    gametimer = 0
                    scorefont = font.render("Score: " + str(score), True, (0, 0, 0))
                elif settings_interact.collidepoint(event.pos):
                    game_state = 3
                elif stats_interact.collidepoint(event.pos):
                    game_state = 4
                elif skin_interact.collidepoint(event.pos):
                    game_state = 5
                elif achievement_interact.collidepoint(event.pos):
                    game_state = 6

        if game_state == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_velocity += flap_force
                clicks += 1
                if clicks >= 1000 and achievementtwounlocked == False:
                    achievementtwounlocked = True
                with open("flappybirdsavefile.json", "w") as file:
                    json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                totalclickedfont = font.render("You have clicked " + str(clicks) + " times", True, (0, 0, 0))

        if game_state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1
                if reset_interact.collidepoint(event.pos):
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": 0, "totalscore": 0, "selected": 0, "deaths": 0, "clicks": 0, "achievementoneunlocked": False, "achievementtwounlocked": False}, file)
                    highscore = 0
                    totalscore = 0
                    selected = 0
                    deaths = 0
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "defaultbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    totalclickedfont = font.render("You have clicked " + str(clicks) + " times", True, (0, 0, 0))
                    highscorestatfont = font.render("Your high score is " + str(highscore), True, (0, 0, 0))
                    deathsfont = font.render("You have died " + str(deaths) + " times", True, (0, 0, 0))
                    totalscorefont = font.render("Your total score gained is " + str(totalscore), True, (0, 0, 0))

        if game_state == 4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1

        if game_state == 5:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1
                elif defaultbird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Default Yellow Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "defaultbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 0
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                elif bluebird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Blue Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "bluebird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 1
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                elif cyanbird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Cyan Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "cyanbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 2
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                elif greenbird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Green Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "greenbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 3
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                elif pinkbird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Pink Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "pinkbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 4
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                elif redbird_interact.collidepoint(event.pos):
                    currentlyselectedfont = font.render("Current selected: Red Bird", True, (0, 0, 0))
                    bird = pygame.surface.Surface((50, 50))
                    bird.fill((255, 255, 255))
                    bird = pygame.image.load(os.path.join(BASE_DIR, "imgs", "redbird.png")).convert_alpha()
                    bird = pygame.transform.scale(bird, (50, 50))
                    selected = 5
                    with open("flappybirdsavefile.json", "w") as file:
                        json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)

        if game_state == 6:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1

        if gameover == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameover = False
                    game_state = 2
                    bird_y = 300
                    bird_velocity = 0
                    score = 0
                    pipe_x = 800
                    pipe_top = random.randint(50, 400)
                    pipe_bottom = pipe_top + 200
                    gametimer = 0
                    scorefont = font.render("Score: " + str(score), True, (0, 0, 0))
                if event.key == pygame.K_ESCAPE:
                    gameover = False
                    game_state = 1



    window.fill((135, 206, 235))

    if game_state == 1:
        window.blit(titlefont, (300, 150))
        exitbutton.blit(exitfont, exitfont.get_rect(center=exitbutton.get_rect().center))
        window.blit(exitbutton, exit_interact)
        playbutton.blit(playfont, playfont.get_rect(center=playbutton.get_rect().center))
        window.blit(playbutton, play_interact)
        settingsbutton.blit(settingsfont, settingsfont.get_rect(center=settingsbutton.get_rect().center))
        window.blit(settingsbutton, settings_interact)
        statsbutton.blit(statsfont, statsfont.get_rect(center=statsbutton.get_rect().center))
        window.blit(statsbutton, stats_interact)
        skinbutton.blit(skinfont, skinfont.get_rect(center=skinbutton.get_rect().center))
        window.blit(skinbutton, skin_interact)
        achievementbutton.blit(achievementsfont, achievementsfont.get_rect(center=achievementbutton.get_rect().center))
        window.blit(achievementbutton, achievement_interact)

    if game_state == 3:
        backbutton.blit(backfont, backfont.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)
        resetbutton.blit(resetfont, resetfont.get_rect(center=resetbutton.get_rect().center))
        window.blit(resetbutton, reset_interact)

    if game_state == 4:
        backbutton.blit(backfont, backfont.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)
        window.blit(statsstatfont, (300, 50))
        window.blit(highscorestatfont, (290, 120))
        window.blit(totalclickedfont, (290, 180))
        window.blit(deathsfont, (290, 230))
        window.blit(totalscorefont, (290, 280))

    if game_state == 5:
        window.blit(skinstextfont, (300, 50))
        window.blit(defaultbird, defaultbird_interact)
        window.blit(bluebird, bluebird_interact)
        window.blit(cyanbird, cyanbird_interact)
        window.blit(greenbird, greenbird_interact)
        window.blit(pinkbird, pinkbird_interact)
        window.blit(redbird, redbird_interact)
        window.blit(currentlyselectedfont, (100, 450))
        backbutton.blit(backfont, backfont.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)

    if game_state == 6:
        backbutton.blit(backfont, backfont.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)
        window.blit(achievementstextfont, (300, 50))
        window.blit(lockedachievement, (150, 150))
        window.blit(lockedachievement, (150, 350))
        window.blit(achievementsonetitlefont, (250, 150))
        window.blit(achievementsonedescfont, (240, 200))
        window.blit(achievementstwotitlefont, (250, 350))
        window.blit(achievementstwodescfont, (240, 400))
        if achievementoneunlocked == True:
            achievementsonetitlefont = font.render("Highscore of 100+!", True, (0, 0, 0))
            achievementsonedescfont = smallfont.render("Reached a highscore of 100+!", True, (0, 0, 0))
            window.blit(achievementsonetitlefont, (250, 150))
            window.blit(achievementsonedescfont, (240, 200))
            window.blit(achievementone, (150, 150))
        if achievementtwounlocked == True:
            achievementstwotitlefont = font.render("1000+ Clicks!", True, (0, 0, 0))
            achievementstwodescfont = smallfont.render("Clicked 1000+ times in game!", True, (0, 0, 0))
            window.blit(achievementstwotitlefont, (250, 350))
            window.blit(achievementstwodescfont, (240, 400))
            window.blit(achievementtwo, (150, 350))

    if game_state == 2:
        if gameover == False:
            bird_velocity += gravity
            bird_y += bird_velocity
            bird_velocity *= 0.95

            if bird_y > 600:
                bird_y = 600
                bird_velocity = 0
                deaths += 1
                with open("flappybirdsavefile.json", "w") as file:
                    json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                deathsfont = font.render("You have died " + str(deaths) + " times", True, (0, 0, 0))
                gameover = True

            pipe_x -= 4

            bird_rect = pygame.Rect(bird_x, bird_y, 50, 50)
            top_piperect = pygame.Rect(pipe_x, 0, 50, pipe_top)
            bottom_piperect = pygame.Rect(pipe_x, pipe_bottom, 50, 600 - pipe_bottom)

            if bird_rect.colliderect(top_piperect) or bird_rect.colliderect(bottom_piperect):
                deaths += 1
                with open("flappybirdsavefile.json", "w") as file:
                    json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                deathsfont = font.render("You have died " + str(deaths) + " times", True, (0, 0, 0))
                gameover = True
  
        if not didwepasspipe and pipe_x < bird_x:
            didwepasspipe = True
            score += 1
            totalscore += 1
            with open("flappybirdsavefile.json", "w") as file:
                json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
            totalscorefont = font.render("Your total score gained is " + str(totalscore), True, (0, 0, 0))
            scorefont = font.render("Score: " + str(score), True, (0, 0, 0))

        if gameover == True:
            if score > highscore:
                highscore = score
                window.blit(highscorefont, (10, 50))
                if highscore >= 100 and achievementoneunlocked == False:
                    achievementoneunlocked = True
                with open("flappybirdsavefile.json", "w") as file:
                    json.dump({"highscore": highscore, "totalscore": totalscore, "selected": selected, "deaths": deaths, "clicks": clicks, "achievementoneunlocked": achievementoneunlocked, "achievementtwounlocked": achievementtwounlocked}, file)
                highscorestatfont = font.render("Your high score is " + str(highscore), True, (0, 0, 0))
            window.blit(gameoverfont, (300, 230))
            window.blit(tryagainfont, (300, 280))
            window.blit(trytoquitfont, (300, 330))

        pygame.draw.rect(window, (0, 255, 0), (pipe_x, 0, 50, pipe_top))
        pygame.draw.rect(window, (0, 255, 0), (pipe_x, pipe_bottom, 50, 600 - pipe_bottom))

        if pipe_x < -60:
            pipe_x = 790
            randomnum = random.randint(50, 400)
            pipe_top = randomnum
            pipe_bottom = randomnum + 200
            didwepasspipe = False

        window.blit(bird, (bird_x, bird_y))
        window.blit(scorefont, (10, 10))
    


    clock.tick(60)
    pygame.display.flip()