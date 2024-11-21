from config import *
from pytmx.util_pygame import load_pygame
from os.path import join
from Level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt=0
        self.level=Level(load_pygame(join(".","tmx","map.tmx")))

    def run(self): 
        while self.running:
            self.processInput()
            self.update()
            self.draw()

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.level.player.jump_count < 1:   #to prevent double jump
                    self.level.player.jump()
    
    def update(self):
        self.dt = self.clock.tick(60) / 1000.0
        self.level.update(self.dt)
        if self.level.player.health<=0:
            self.running=False

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.level.draw()
        pygame.display.flip()
    
    def shutdown(self):
        pygame.quit()
        sys.exit()