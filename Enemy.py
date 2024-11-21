from config import *
from sprites import PlayerSprite, Sprite
import os

class Enemy:
    def __init__(self,pos,groups,collision_sprites,damage_sprites,image,player):
        #sprite
        self.state='idle'
        self.face="right"
        self.sprite=PlayerSprite(pos,image,groups,self.state,self.face,(20,70),(30,30),(30,30))
        self.rect=self.sprite.image.get_frect(topleft=pos)
        self.hitbox_rect=self.rect
        self.old_rect=self.hitbox_rect.copy()
        self.dir=pygame.Vector2()
        self.dir.x=1
        self.speed=100
        self.all_sprites=groups
        self.collision_sprites=collision_sprites
        self.damage_sprites=damage_sprites
        self.boundary=[pos[0]-100,pos[0]+300]
        self.player=player
        self.isBullet=False


    def processInput(self):
        move=pygame.Vector2()

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move.x-=1
            self.face="left"
        if keys[pygame.K_RIGHT]:
            move.x+=1
            self.face="right"
        self.dir.x=move.x

    def move(self,dt):
        self.hitbox_rect.x+=self.dir.x*self.speed*dt

    def update(self,dt):
        self.old_rect=self.hitbox_rect.copy()
        # self.processInput()
        self.move(dt)
        if(self.rect.left<self.boundary[0] or self.rect.right>self.boundary[1]):
            self.dir.x *=-1
        self.rect.center=self.hitbox_rect.center
        self.sprite.rect.center=self.hitbox_rect.center
        if self.face=="right":
            self.sprite.image=self.sprite.image
        else:
            self.sprite.image=pygame.transform.flip(self.sprite.image,True,False)
        # self.sprite.frames=self.frames[self.state]
        self.sprite.face=self.face
        # self.sprite.walking=True if self.dir.x!=0 else False
        self.shoot(self.player)
        self.sprite.update(dt)
        # self.sprite2.update(dt)

    def damage(self):
        self.health-=1

    def draw(self):
        # self.sprite.draw_particles()
        pass
    
    def shoot(self, player):
        if abs(self.rect.centerx - player.rect.centerx) < 300 and not self.isBullet and self.player.state!='hide':  # Check if player is within range
            bullet = Bullet(self.rect.center,self.player.hitbox_rect.center, self.face,self.all_sprites,self)
            self.damage_sprites.add(bullet)
            self.isBullet=True

class Bullet(Sprite):
    def __init__(self, pos,playerpos, direction,groups,enemy):
        super().__init__(pos, pygame.Surface((20, 20)),groups)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 750
        self.direction = pygame.Vector2(playerpos)-pygame.Vector2(pos)
        self.direction=self.direction.normalize() if self.direction.length() != 0 else pygame.Vector2(1,0)
        self.enemy=enemy
        self.image.set_colorkey((255,255,255))


    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
            self.enemy.isBullet=False
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.bottom < 0 or self.rect.top > 1100:
            self.kill()
            self.enemy.isBullet=False