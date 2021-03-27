import math
import random
from inits import *
from classes import *
from weapons import *

# Player class
class PlayerShip(pygame.sprite.Sprite, Base):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, GR_PLAYER_BODY_DEFAULT, player_group)
        self.hostile_group = enemy_ammo_group
        self.hor_margin = -15
        self.ver_margin = -30
        self.orientation = (-0.0, -1.0)
        self.imageset_hilight = GR_PLAYER_BODY_BLINK
        self.imageset_up = GR_PLAYER_BODY_UP 
        self.start_x = x
        self.start_y = y
        self.alive = True
        self.invincible = 0
        self.hitpoints = 10
        self.hitpoints_max = 10
        self.max_speedx = 4.0
        self.max_speedy = 3.0
        self.frictionX = 0.2 
        self.frictionY = 0.2
        self.setStartPosition()
        self.getWeapon(1)
        self.tryout = 0
        
    
    # Set player to starting position on screen and initialize hitbox
    def setStartPosition(self):
        self.rect.x = 0
        self.rect.y = 0
        self.rect = self.rect.move(self.start_x, self.start_y)
        self.alignHitBox(self.rect)
        
    # Passive movement & collision detection
    def update(self, level, offset):
        sx, sy = self.speed
        # Check if dead        
        if self.alive == True:
            if self.destroyed() == True:
                self.alive = False
                self.explode(GR_EFFECT_EXPLOSION_BIG, snd_player_death)
                player_group.remove(self)
                

            # Dies if collided to level walls but destroys them when invincible
            hitted_block = level.checkCollision(self.hitbox, offset)
            if hitted_block:
                if self.invincible > 0:
                    level.removeBlock(hitted_block[0], hitted_block[1])
                    snd_wall_destroy.play()
                else:
                    self.hitpoints -= 1
                    self.setAnimation(self.imageset_hilight, 12)
                    snd_wall_hit.play()
    

            if self.invincible <= 0:
                # Check collision to ammo
                damage = self.getCollisionDamage(self.hostile_group)
                if damage:
                    self.hitpoints -= damage
                    self.setAnimation(self.imageset_hilight, 12)
                    

                # Check collision to enemy
                if pygame.sprite.spritecollideany(self, enemy_group, self.collided):
                    self.hitpoints = 0

            # Update shooting delay
            self.weapon.shoot_timer += 1

            # Check special weapon ammo left and go back to default weapon
            if self.weapon.magazine == 0:
                self.getWeapon(1)

            # Set thruster animation if moved
            if self.speed[1] < -1.0:
                self.setAnimation(self.imageset_up, 4)

            # bounces from top and bottom of the area
            if self.rect.top < 0:
                self.rect.top = 0
                sy = -sy
            if self.rect.bottom > level.height:
                self.rect.bottom = level.height
                sy = -sy
            self.speed = (sx, sy)

            # Bounces from sides of level
            self.bounceFromSides(level, offset)

            # Bounces form walls
            self.bounceFromRect(level.locateCollision(self.hitbox, offset))

            # Apply Friction
            self.applyFriction(self.frictionX, self.frictionY)

            # Change animation frame
            self.changeFrame()

            # Counts invincibility
            if self.invincible > 0:
                self.invincible -= 1

            # Ensures that hitbox is following
            self.alignHitBox(self.rect)

            # Give coordinates for shadow casting
            #level.background.getPlayerPosition(self.rect)


    def move(self, scroll_speed): 
        # Move the player
        self.rect = self.rect.move(self.speed)
        self.alignHitBox(self.rect)

    def setSpeed(self, acc_x, acc_y):
        sx, sy = self.speed
        sx += acc_x
        sy += acc_y
        if sx > self.max_speedx :
            sx = self.max_speedx
        if sx < -self.max_speedx :
            sx = -self.max_speedx
        if sy > self.max_speedy :
            sy = self.max_speedy
        if sy < -self.max_speedy :
            sy = -self.max_speedy
        self.speed = (sx, sy)

    # Change a weapon
    def changeWeapon(self, key):
        if key[pygame.K_1] == True:
            self.weapon = WeaponSingle(feat_player_beam_default, self.orientation)
            self.weapon.magazine = -1
        if key[pygame.K_2] == True:
            self.weapon = WeaponDouble(feat_player_beam_default, self.orientation)
            self.weapon.magazine = -1
        if key[pygame.K_3] == True:
            self.weapon = WeaponMinigun(feat_player_beam_minigun, self.orientation)
            self.weapon.magazine = -1
        if key[pygame.K_4] == True:
            self.weapon = WeaponLauncher(feat_player_rocket, self.orientation)
            self.weapon.magazine = -1
        if key[pygame.K_5] == True:
            self.weapon = WeaponThrower(feat_player_flame, self.orientation)
            self.weapon.magazine = -1

    # Change a weapon
    def getWeapon(self, key):
        if key == 1:
            self.weapon = WeaponSingle(feat_player_beam_default, self.orientation)
            self.weapon.magazine = -1
        if key == 2:
            self.weapon = WeaponDouble(feat_player_beam_default, self.orientation)
            self.weapon.magazine = 15
        if key == 3:
            self.weapon = WeaponMinigun(feat_player_beam_default, self.orientation)
            self.weapon.magazine = 30
        if key == 4:
            self.weapon = WeaponLauncher(feat_player_rocket, self.orientation)
            self.weapon.magazine = 15
        if key == 5:
            self.weapon = WeaponThrower(feat_player_flame, self.orientation)
            self.weapon.magazine = 60

    def getHealth(self):
        if self.hitpoints < self.hitpoints_max:
            self.hitpoints += 1
            self.setAnimation(self.imageset_hilight, 12)

    def getShield(self):
        PlayerEffect(self, GR_PLAYER_SHIELD, 1000)
        self.invincible = 1000

    # Shooting
    def shoot(self, key):
        if self.alive == True and key == True:
            self.weapon.launch(self.rect.centerx, self.rect.y)



class PlayerEffect(pygame.sprite.Sprite, Base):
    def __init__(self, player, imageset, duration):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, player.rect.centerx, player.rect.centery, imageset, effects_group)
        self.rect = self.rect.move(round(-self.rect.w / 2), round(-self.rect.h / 2))
        self.host = player
        self.lifetime = duration
        self.lifetime_counter = 0
        self.animation_duration = 0
        self.transparent = GR_PLAYER_SHIELD_BLINK
        self.disable_warning_time = 64

    
    def update(self, level, offset):
        # Erase if lifetime spent
        if self.lifetime_counter >= self.lifetime or self.host.alive == False:
            self.kill()

        # Blink if lifetime about to end
        if self.lifetime - self.lifetime_counter < self.disable_warning_time:
            self.setAnimation(self.transparent, 0)

        self.lifetime_counter += 1
        # Update animation
        self.changeFrame()
        
    def move(self, scroll_speed):
        self.rect.centerx = self.host.rect.centerx
        self.rect.centery = self.host.rect.centery
        self.alignHitBox(self.rect)