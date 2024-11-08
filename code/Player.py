from config import *
from sprites import AnimatedSprite
import os

class Player:
    def __init__(self,pos,groups,collision_sprites,damage_sprites,frames):
        #sprite
        self.state='idle'
        self.face="right"
        self.sprite=AnimatedSprite(pos,frames[self.state],groups)
        self.frames=frames
        # self.image=pygame.image.load('./graphics/2BlueWizardIdle/0.png')
        self.rect=self.sprite.image.get_frect(topleft=pos)
        self.hitbox_rect=self.rect.inflate(-200,-120)
        self.old_rect=self.hitbox_rect.copy()
        self.dir=vector()
        self.speed=400
        self.gravity=50
        # self.jump=12000
        self.isJumping=False
        self.jump_count = 0
        self.speedY=1000
        self.collision_sprites=collision_sprites
        self.damage_sprites=damage_sprites
        self.onsurface=False

        self.health=10

    def processInput(self):
        move=vector()

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
        self.collision("horizontal")
        
        # dy=self.gravity
        self.dir.y+=self.gravity
        # self.dir.y+=dy/2*dt
        if(self.isJumping):
            self.dir.y=-self.speedY
            self.isJumping=False
            self.jump_count+=1
        self.hitbox_rect.y+=self.dir.y*dt
        self.collision("vertical")
        self.check_onsurface()

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

        # for sprite in self.damage_sprites:
        #     if sprite.rect.colliderect(self.hitbox_rect):
        #         if axis == "horizontal":
        #             if self.hitbox_rect.left<=sprite.rect.right and self.old_rect.left>=sprite.old_rect.right:
        #                 self.hitbox_rect.left=sprite.rect.right+30
        #                 print("Damage")
        #             if self.hitbox_rect.right>=sprite.rect.left and self.old_rect.right<=sprite.old_rect.left:
        #                 self.hitbox_rect.right=sprite.rect.left-30
        #                 print("Damage")

        #         if axis == "vertical":
        #             if self.hitbox_rect.bottom>=sprite.rect.top and self.old_rect.bottom<=sprite.old_rect.top:
        #                 if(self.hitbox_rect.center[0]-sprite.rect.center[0]<0):
        #                     self.hitbox_rect.right=sprite.rect.left-30
        #                 else:
        #                     self.hitbox_rect.left=sprite.rect.right+30
        #                 print("Damage")
        #             if self.hitbox_rect.top<=sprite.rect.bottom and self.old_rect.top>=sprite.old_rect.bottom:
        #                 if(self.hitbox_rect.center[0]-sprite.rect.center[0]>0):
        #                     self.hitbox_rect.right=sprite.rect.left-10
        #                 else:
        #                     self.hitbox_rect.left=sprite.rect.right+10
        #                 print("Damage")
                    # self.dir.y=0

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
        self.processInput()
        self.move(dt)
        self.rect.center=self.hitbox_rect.center
        self.sprite.rect.center=self.hitbox_rect.center
        if self.face=="right":
            self.sprite.image=self.sprite.image
        else:
            self.sprite.image=pygame.transform.flip(self.sprite.image,True,False)
        if not self.onsurface:
            self.state="jump"
        else:
            self.state="idle" if self.dir.x==0 else "walk"
        self.sprite.frames=self.frames[self.state]

    def damage(self):
        self.health-=1
        print("Health:",self.health)
    