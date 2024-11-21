from config import *

class AllSprites(pygame.sprite.Group):
    def __init__(self,width,height):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=pygame.Vector2(0,0)
        self.width=width
        self.height=height
    
    def camera_constraint(self):
        self.offset.x = max(0, min(self.offset.x, self.width - SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.height - SCREEN_HEIGHT))

    def draw(self,target_pos):
        self.offset.x=target_pos[0]-SCREEN_WIDTH/2
        self.offset.y=target_pos[1]-SCREEN_HEIGHT/2
        # print(self.height,self.offset.y)
        self.camera_constraint()
        for sprite in self:
            offset_pos=sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            # rect=sprite.hitbox_rect
            # rect.topleft=offset_pos
            # pygame.draw.rect(self.display_surface,"blue",rect)
            