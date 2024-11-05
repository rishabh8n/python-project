from config import *

class UI:
    def __init__(self,font):
        self.display_surface = pygame.display.get_surface()
        self.sprites=pygame.sprite.Group()
        self.font=font
        self.score=100

    def update(self,dt,score,health):
        self.score=score
        self.health=health

    def display_text(self):
        text_surf=self.font.render("Score: "+str(self.score),False,'black')
        text_surf_h=self.font.render("Health: "+str(self.health),False,'black')
        text_rect=text_surf.get_frect(topleft=(16,32))
        text_rect_h=text_surf.get_frect(topleft=(16,92))
        self.display_surface.blit(text_surf,text_rect)
        self.display_surface.blit(text_surf_h,text_rect_h)

        
        