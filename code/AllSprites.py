from config import *

class AllSprites(pygame.sprite.Group):
    def __init__(self,width,height):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=vector(0,0)
        self.width=width
        self.height=height
    
    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x > 0 else 0
        # self.offset.x = self.offset.x if self.offset.x < -self.width+WINDOW_WIDTH else -self.width+WINDOW_WIDTH

        # self.offset.y = self.offset.y if self.offset.y < 0 else 0
        # self.offset.y = self.offset.y if self.offset.y > self.height-WINDOW_HEIGHT else self.height-WINDOW_HEIGHT

        # self.offset.y = self.offset.y if self.offset.y > 0 else 0
        # self.offset.y = self.offset.y if

    def draw(self,target_pos):
        self.offset.x=target_pos[0]-WINDOW_WIDTH/2
        self.offset.y=target_pos[1]-WINDOW_HEIGHT/2
        # print(self.height,self.offset.y)
        self.camera_constraint()
        for sprite in self:
            offset_pos=sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            # rect=sprite.hitbox_rect
            # rect.topleft=offset_pos
            # pygame.draw.rect(self.display_surface,"blue",rect)