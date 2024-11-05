from config import *
from support import *
from Level import Level
# from support import *
from pytmx.util_pygame import load_pygame
import os
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(NAME)
        self.screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock=pygame.time.Clock()
        self.dt=0
        self.isGameRunning=True
        self.import_assets()
        self.tmx_map=load_pygame(os.path.join(".","data","tmx","map1.tmx"))
        self.stage=Level(self.tmx_map,self.level_frames)
        self.font=pygame.font.SysFont("arial",40)
        self.ui=UI(self.font)

    def import_assets(self):
        self.level_frames={
            'player': {'idle':import_folder('.','graphics','2BlueWizardIdle'),
                       'jump':import_folder('.','graphics','2BlueWizardJump'),
                       'walk':import_folder('.','graphics','2BlueWizardWalk')}
                       
        }

    def run(self):
        while self.isGameRunning:
            self.dt=self.clock.tick(60)/1000
            self.processInput()
            self.update()
            self.render()

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isGameRunning=False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.stage.player.jump_count < 2:
                    self.stage.player.jump()


    def update(self):
        if(self.stage.player.health<=0):
            self.isGameRunning=False
        self.stage.update(self.dt)
        self.ui.update(self.dt,self.stage.score,self.stage.player.health)
        

    def render(self):
        self.screen.fill((255,255,255))
        self.stage.draw(self.screen)
        self.ui.display_text()
        pygame.display.flip()