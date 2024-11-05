from config import *
from sprites import Sprite
import os

class Obstacle:
    def __init__(self,pos,surf,groups,collision_sprites):
        self.sprite=Sprite(pos,surf,groups)
        self.rect=self.sprite.image.get_frect(topleft=pos)
        self.hitbox_rect=self.rect.inflate(-100,-80)
        self.old_rect=self.hitbox_rect.copy()
        self.collision_rects=[sprite.rect for sprite in collision_sprites]

    def checkCollision(self,player):
        if self.hitbox_rect.colliderect(player.hitbox_rect):
                # if axis == "horizontal":
                    if player.hitbox_rect.left<=self.hitbox_rect.right and player.old_rect.left>=self.old_rect.right:
                        player.hitbox_rect.left=self.hitbox_rect.right+30
                        player.damage()
                    if player.hitbox_rect.right>=self.hitbox_rect.left and player.old_rect.right<=self.old_rect.left:
                        player.hitbox_rect.right=self.hitbox_rect.left-30
                        player.damage()

                # if axis == "vertical":
                    if player.hitbox_rect.bottom>=self.hitbox_rect.top and player.old_rect.bottom<=self.old_rect.top:
                        if(player.hitbox_rect.center[0]-self.hitbox_rect.center[0]<0):
                            player.hitbox_rect.right=self.hitbox_rect.left-30
                        else:
                            player.hitbox_rect.left=self.hitbox_rect.right+30
                        player.damage()
                    if player.hitbox_rect.top<=self.hitbox_rect.bottom and player.old_rect.top>=self.old_rect.bottom:
                        if(player.hitbox_rect.center[0]-self.hitbox_rect.center[0]>0):
                            player.hitbox_rect.right=self.hitbox_rect.left-10
                        else:
                            player.hitbox_rect.left=self.hitbox_rect.right+10
                        player.damage()

    def update(self,dt,player):
        self.old_rect=self.hitbox_rect.copy()
        self.checkCollision(player)
