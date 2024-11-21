from config import *
from sprites import PlayerSprite, Sprite
import os

class Enemy:
    def __init__(self,pos,groups,collision_sprites,damage_sprites,image,player):
        #sprite
        self.state='idle'
        self.face="right"
        self.sprite=PlayerSprite(pos,image,groups,self.state,self.face,(20,70),(30,30),(30,30))
        # self.sprite2=RotatingSprite(pos,image,groups)
        # self.frames=frames
        # self.image=pygame.image.load('./graphics/2BlueWizardIdle/0.png')
        self.rect=self.sprite.image.get_frect(topleft=pos)
        self.hitbox_rect=self.rect
        self.old_rect=self.hitbox_rect.copy()
        self.dir=pygame.Vector2()
        self.dir.x=1
        self.speed=100
        self.gravity=0
        # self.jump=12000
        self.isJumping=False
        self.jump_count = 0
        self.speedY=1100
        self.all_sprites=groups
        self.collision_sprites=collision_sprites
        self.damage_sprites=damage_sprites
        self.boundary=[pos[0]-100,pos[0]+300]
        self.player=player
        self.isBullet=False


    def processInput(self):
        move=pygame.Vector2()

        keys=pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     self.isJumping=True
        if keys[pygame.K_LEFT]:
            move.x-=1
            self.face="left"
        if keys[pygame.K_RIGHT]:
            move.x+=1
            self.face="right"
        self.dir.x=move.x

        
    def jump(self):
        self.isJumping=True
    
    def move(self,dt):
        self.hitbox_rect.x+=self.dir.x*self.speed*dt
        # self.collision("horizontal")
        
        # dy=self.gravity
        # self.dir.y+=self.gravity
        # # self.dir.y+=dy/2*dt
        # if(self.isJumping):
        #     self.dir.y=-self.speedY
        #     self.isJumping=False
        #     self.jump_count+=1
        # self.hitbox_rect.y+=self.dir.y*dt
        # self.collision("vertical")
        # self.check_onsurface()

    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == "horizontal":
                    if self.hitbox_rect.left<=sprite.rect.right and self.old_rect.left>=sprite.old_rect.right:
                        self.hitbox_rect.left=sprite.rect.right
                    if self.hitbox_rect.right>=sprite.rect.left and self.old_rect.right<=sprite.old_rect.left:
                        self.hitbox_rect.right=sprite.rect.left
                if axis == "vertical":
                    if self.hitbox_rect.bottom>=sprite.rect.top and self.old_rect.bottom<=sprite.old_rect.top:
                        self.hitbox_rect.bottom=sprite.rect.top
                    if self.hitbox_rect.top<=sprite.rect.bottom and self.old_rect.top>=sprite.old_rect.bottom:
                        self.hitbox_rect.top=sprite.rect.bottom
                    self.dir.y=0

    def check_onsurface(self):
        floor_rect=pygame.Rect(self.hitbox_rect.bottomleft,(self.hitbox_rect.width,1))
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(floor_rect):
                self.onsurface=True
                self.jump_count=0
                break
            else:
                self.onsurface=False

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
        print("Health:",self.health)

    def draw(self):
        # self.sprite.draw_particles()
        pass
    
    def shoot(self, player):
        if abs(self.rect.centerx - player.rect.centerx) < 300 and not self.isBullet:  # Check if player is within range
            bullet = Bullet(self.rect.center,self.player.hitbox_rect.center, self.face,self.all_sprites,self)
            self.damage_sprites.add(bullet)
            self.isBullet=True

class Bullet(Sprite):
    def __init__(self, pos,playerpos, direction,groups,enemy):
        super().__init__(pos, pygame.Surface((10, 5)),groups)
        # self.image = pygame.Surface((10, 5))
        self.image.fill((250, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 300
        self.direction = pygame.Vector2(playerpos)-pygame.Vector2(pos)
        self.direction=self.direction.normalize() if self.direction.length() != 0 else pygame.Vector2(1,0)
        self.enemy=enemy

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
            self.enemy.isBullet=False
        # if self.rect.top < 0 or self.rect.bottom > pygame.display.get_surface().get_height():
        #     self.kill()
        #     self.enemy.isBullet=False
        # if not pygame.display.get_surface().get_rect().contains(self.rect):
        #     self.kill()
        #     self.enemy.isBullet = False