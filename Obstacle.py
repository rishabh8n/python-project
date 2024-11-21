from config import *
from sprites import Sprite

class Obstacle:
    def __init__(self,pos,surf,groups,collision_sprites):
        self.sprite=Sprite(pos,surf,groups)
        self.rect=self.sprite.image.get_frect(topleft=pos)
        self.hitbox_rect=self.rect.inflate(-30,-10)

    def update(self,dt,player):
        pass
