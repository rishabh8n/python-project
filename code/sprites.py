from config import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,hitbox_offset=(0,0)):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(topleft=pos)
        # self.hitbox_rect=self.rect.inflate(hitbox_offset)
        self.old_rect=self.rect.copy()
    
    def update(self,dt):
        pass

class AnimatedSprite(Sprite):
    def __init__(self,pos,frames,groups,animation_speed=ANIMATION_SPEED):
        self.frames,self.frame_index=frames,0
        self.animation_speed=animation_speed
        super().__init__(pos,self.frames[self.frame_index],groups)
    
    def animate(self,dt):
        self.frame_index+=self.animation_speed*dt
        self.image=self.frames[int(self.frame_index)%len(self.frames)]

    def update(self, dt):
        self.animate(dt)