import pygame
#import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from inits import *
from levels import *
from classes import *


# Show game titles
def showText(message):
    font = pygame.font.Font('freesansbold.ttf', 48) 
    text = font.render(message, True, color_text)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    SCREEN.blit(text, textRect)
    pygame.display.flip()

def showScore(number):
    font = pygame.font.Font('freesansbold.ttf', 32) 
    text = font.render(number, True, color_text)
    textRect = text.get_rect()
    textRect.center = (width - 64, height - 64)
    SCREEN.blit(text, textRect)
    pygame.display.flip()

def showHearts(amount):
    image = GR_UI_HEART_DEFAULT
    Rect = image[0].get_rect()
    Rect.y = height - Rect.height
    Rect.x = 0
    i = 0
    while i < amount:
        SCREEN.blit(image[0], Rect)
        Rect.x += Rect.width
        i += 1

# Main program
#-------------
# Pygame initials

# Title
pygame.display.set_caption("Luolalentely")
icon = GR_PLAYER_BODY_DEFAULT
pygame.display.set_icon(icon[0])

# Create player
player = PlayerShip(player_start_x, player_start_y)

# Main loop
while True: 
    # Play the level
    clock = pygame.time.Clock()
    scroll_speed = basic_scroll_speed   
    offset = 0
    
    end_counter = 0
    stars = StarField(250)
    this_level = levels[current_level]
    pygame.mixer.music.play(-1)
    
    while clock.tick(framerate):
        # Keyevents listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()
        player.setSpeedX(pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT])
        player.setSpeedY(pressed[pygame.K_DOWN]-pressed[pygame.K_UP])
        player.shoot(pressed[pygame.K_SPACE])
        player.changeWeapon(pressed)
         
       # Is player alive?
        if player.alive == False:
            player.speedx = 0.0
            player.speedy = 0.0
            if end_counter > framerate:
                break
            end_counter += 1

        # Is player reached the end of level?
        if offset >= -this_level.start_point:
            scroll_speed = 0  
            # Check if boss is dead         
            if checkBosses() == False:
                if end_counter > framerate * 2:
                    break
                end_counter += 1

        # Objects update
        player_group.update(this_level, offset)
        enemy_group.update(this_level, offset, player)
        player_ammo_group.update(this_level, offset)
        enemy_ammo_group.update(this_level, offset)
        effects_group.update(this_level, offset)

        # Objects movement
        for i in player_group.sprites():
            i.move(scroll_speed)

        for i in enemy_group.sprites():
            i.move(scroll_speed)

        for i in player_ammo_group.sprites():
            i.move(scroll_speed)

        for i in enemy_ammo_group.sprites():
            i.move(scroll_speed)

        for i in effects_group.sprites():
            i.move(scroll_speed)

        # Clean destroyed enemies
        for i in enemy_group:
            if i.killed == True:
                score += i.score
                i.kill()

        # Create new enemies
        enemy_positions_list = this_level.getEnemies(offset)
        if enemy_positions_list:
            for i in enemy_positions_list:
                enemy = selectEnemy(i[0], i[1], i[2])

        # Background update
        SCREEN.fill(color_bg_default)
        stars.draw(SCREEN, 2)
        this_level.draw(offset, SCREEN)        

        # Draw all the objects
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_ammo_group.draw(SCREEN)
        enemy_ammo_group.draw(SCREEN)
        effects_group.draw(SCREEN)
        # Rectange for collision debugging
        #pygame.draw.rect(SCREEN, RED, player.hitbox, 1)

        # Show hearts of hitpoints
        showHearts(player.hitpoints)

        # Show score
        showScore(str(score))

        # Update screen
        pygame.display.flip()
        
        # Move the whole screen up one step
        offset += scroll_speed

    # Show level ending text
    if player.alive == False:
        showText("Kuolit!")
        # Reset player
        player = PlayerShip(player_start_x, player_start_y)
        
    elif current_level == (len(levels)-1):
        showText("HIENOA, PELI LÄPÄISTY!")
        player.setStartPosition()
        current_level = 0
    else:
        showText("Kenttä läpäisty!")
        player.setStartPosition()
        current_level += 1

    enemy_group.empty()
    player_ammo_group.empty()
    enemy_ammo_group.empty()
    effects_group.empty()      

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




