from config import *
from os.path import join
from sprites import Sprite,PlatformSprite
from Player import Player
from Obstacle import Obstacle
from AllSprites import AllSprites
from Enemy import Enemy

class Level:
    def __init__(self, tmx_data):
        self.tmx_data = tmx_data
        self.level_width=self.tmx_data.width*TILE_SIZE
        self.level_height=self.tmx_data.height*TILE_SIZE
        self.screen = pygame.display.get_surface()
        self.obstacles=[]
        self.all_sprites=AllSprites(self.level_width,self.level_height)
        self.damage_sprites=pygame.sprite.Group()
        self.collision_sprites=pygame.sprite.Group()
        self.enemies=[]
        self.setup()

    def setup(self):
        for obstacle in self.tmx_data.get_layer_by_name("obstacles"):
            self.obstacles.append(Obstacle((obstacle.x,obstacle.y),obstacle.image,(self.all_sprites,self.damage_sprites),self.collision_sprites))
        
        for player in self.tmx_data.get_layer_by_name("player"):
            # frames=level_frames['player']
            self.player=Player((player.x,player.y),self.all_sprites,self.collision_sprites,self.damage_sprites,player.image,self.obstacles)
        
        for player in self.tmx_data.get_layer_by_name("enemies"):
            # frames=level_frames['player']
            self.enemies.append(Enemy((player.x,550),self.all_sprites,self.collision_sprites,self.damage_sprites,player.image,self.player))

        for x,y,surf in self.tmx_data.get_layer_by_name("Tile Layer 1").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))

        for platform in self.tmx_data.get_layer_by_name("platforms"):
            # print(surf)
            PlatformSprite((platform.x,platform.y),200,0,platform.image,(self.all_sprites,self.collision_sprites),self.collision_sprites,self.player)

    def update(self,dt):
        self.all_sprites.update(dt)
        # self.checkDamage()
        for obstacle in self.obstacles:
            obstacle.update(dt,self.player)
        # self.item_collision()
        self.check_constraint()
        self.player.update(dt)
        for enemy in self.enemies:
            enemy.update(dt)

    def check_constraint(self):
        if self.player.hitbox_rect.left<=0:
            self.player.hitbox_rect.left=0
        if self.player.hitbox_rect.right>=self.level_width:
            self.player.hitbox_rect.right=self.level_width

        if self.player.hitbox_rect.bottom>=self.level_height:
            self.player.health=0

    def draw(self):
        self.screen.fill((255,255,255))
        self.all_sprites.draw(self.player.hitbox_rect.center)