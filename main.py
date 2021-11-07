import pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from inits import *
from assets import *
from text import *
from interface import *
from levels import *
from classes import *
from enemy import *
from player import *

# Main program
#-------------
# Title
pygame.display.set_caption("Luolalentely")
pygame.display.set_icon(GR_PLAYER_BODY_DEFAULT[0])

offset = 0
current_level = 0 
score = 0
money = 0

# Create player
player = PlayerShip(player_start_x, player_start_y)

# Main loop
while True: 
    # Play the level
    clock = pygame.time.Clock()
    scroll_speed = basic_scroll_speed   
    offset = 0
    counter_backwards = 0
    end_counter = 0
    boss_music = False
    this_level = Walls(levels[current_level])
    loadMusic(this_level.music[0])
    pygame.mixer.music.play(-1)
     
    while clock.tick(framerate):
        # Keyevents listener
        pressed = pygame.key.get_pressed()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT  or pressed[pygame.K_ESCAPE]:  
                pygame.quit()
                sys.exit()
  
        # Debug keys
        nextlevel = pressed[pygame.K_l]
        if nextlevel == True:
            break

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
            # Toggles boss music
            if boss_music == False:
                loadMusic(this_level.music[1])
                pygame.mixer.music.play(-1)
                boss_music = True
            # Check if boss is dead         
            if checkBosses() == False:
                if end_counter > framerate * 4:
                    break
                end_counter += 1

        # Is player pressing down at the bottom of level
        
        elif player.rect.bottom >= this_level.height and pressed[pygame.K_DOWN]:
            if counter_backwards > 0: 
                scroll_speed = round(basic_scroll_speed / 2)
            if counter_backwards > 16:
                scroll_speed = 0
            if counter_backwards > 32:
                scroll_speed = -round(basic_scroll_speed / 2)
            counter_backwards += 1
        else:
            scroll_speed = basic_scroll_speed
            counter_backwards = 0

        # Objects update
        player_group.update(this_level, offset)
        enemy_group.update(this_level, offset, player, scroll_speed)
        player_ammo_group.update(this_level, offset, player)
        enemy_ammo_group.update(this_level, offset, player)
        effects_group.update(this_level, offset)

        # Key Controls
        acc_x = pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT]
        acc_y = pressed[pygame.K_DOWN]-pressed[pygame.K_UP]
        player.setSpeed(acc_x, acc_y)
        player.shoot(pressed[pygame.K_LCTRL] + pressed[pygame.K_SPACE], this_level)
        player.changeWeapon(pressed)

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

        # Process collectables
        for i in effects_group:
            if i.killed == True:
                if i.type == "coin":
                    money += i.score
                elif i.type == "weapon":
                    player.getWeapon(i.boost)
                elif i.type == "powerup":
                    player.getHealth()
                elif i.type == "shield":
                    player.getShield()
                i.kill()

        # Create new enemies
        enemy_positions_list = this_level.getEnemies(offset)
        if enemy_positions_list:
            for i in enemy_positions_list:
                enemy = selectEnemy(i[0], i[1], i[2])

        # Background update
        this_level.draw(offset, SCREEN, scroll_speed)        

        # Draw all the objects
        player_ammo_group.draw(SCREEN)
        enemy_ammo_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_group.draw(SCREEN)
        effects_group.draw(SCREEN)
        # Rectange for collision debugging
        #pygame.draw.rect(SCREEN, RED, player.hitbox, 1)

        # Show hearts of hitpoints
        showHearts(player.hitpoints)

        # Show score and money
        text.showValue(str(money), textplace_rightdown_second, font_medium)
        text.showValue(str(score), textplace_rightdown_first, font_medium)
        
        # Update screen
        pygame.display.flip()
        
        # Move the whole screen up one step
        offset += scroll_speed

    # Show level ending text
    if player.alive == False:
        text.showTitle("t_player_dead", textplace_center, font_large)
        # Reset player
        player = PlayerShip(player_start_x, player_start_y)
        this_level.reset(levels[current_level])

    elif current_level == (len(levels)-1):
        text.showTitle("t_game_finished", textplace_center, font_large)
        player.setStartPosition()
        current_level = 0
    
    else:
        text.showTitle("t_level_finished", textplace_center, font_large)
        player.setStartPosition()
        current_level += 1
    
    # Update screen
    pygame.display.flip()
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




