from config import *
from sprites import Sprite
from Player import Player
from AllSprites import AllSprites
from Obstacle import Obstacle


class Level:
    def __init__(self,tmx_map,level_frames):
        self.level_width=tmx_map.width*TILE_SIZE
        self.level_height=tmx_map.height*TILE_SIZE
        self.screen = pygame.display.get_surface()
        self.all_sprites=AllSprites(self.level_width,self.level_height)
        self.collision_sprites=pygame.sprite.Group()
        self.damage_sprites=pygame.sprite.Group()
        self.item_sprites=pygame.sprite.Group()
        self.obstacles=[]
        self.score=0
        self.setup(tmx_map,level_frames)
        
    
    def setup(self,tmx_map,level_frames):
        for obstacle in tmx_map.get_layer_by_name("obstacles"):
            self.obstacles.append(Obstacle((obstacle.x,obstacle.y),obstacle.image,(self.all_sprites,self.damage_sprites),self.collision_sprites))

        for x,y,surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))
        
        for player in tmx_map.get_layer_by_name("Player"):
            frames=level_frames['player']
            self.player=Player((player.x,player.y),self.all_sprites,self.collision_sprites,self.damage_sprites,frames)

        for x,y,surf in tmx_map.get_layer_by_name("grassb").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites)

        for x,y,surf in tmx_map.get_layer_by_name("grassf").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites)

        for item in tmx_map.get_layer_by_name("Items"):
            Sprite((item.x,item.y),item.image,(self.all_sprites,self.item_sprites))

        # for x,y,surf in tmx_map.get_layer_by_name("Grass").tiles():
        #    Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites)

    # def checkDamage(self):
    #     for sprite in self.damage_sprites:
    #         if sprite.rect.colliderect(self.player.hitbox_rect):
    #             if self.player.hitbox_rect.left<=sprite.hitbox_rect.right and self.player.old_rect.left>=sprite.old_rect.right:
    #                 print("Damage")
    #                 self.player.hitbox_rect.left=sprite.rect.right+10
    #             if self.player.hitbox_rect.right>=sprite.hitbox_rect.left and self.player.old_rect.right<=sprite.old_rect.left:
    #                 print("Damage")
    #                 self.player.hitbox_rect.right=sprite.rect.left-10
    #             if self.player.hitbox_rect.bottom>=sprite.hitbox_rect.top and self.player.old_rect.bottom<=sprite.old_rect.top:
    #                 print("Damage")
    #                 self.player.hitbox_rect.right=sprite.rect.left-10
    #             if self.player.hitbox_rect.top<=sprite.hitbox_rect.bottom and self.player.old_rect.top>=sprite.old_rect.bottom:
    #                 print("Damage")
    #                 self.player.hitbox_rect.right=sprite.rect.left-10


    def update(self,dt):
        self.all_sprites.update(dt)
        # self.checkDamage()
        for obstacle in self.obstacles:
            obstacle.update(dt,self.player)
        self.item_collision()
        self.check_constraint()
        self.player.update(dt)

    def item_collision(self):
        # if self.item_sprites:
        #     item_sprites = pygame.sprite.spritecollide(self.player.sprite,self.item_sprites,True)
        #     if item_sprites:
        #         print("item collision")
        for item in self.item_sprites:
            if item.rect.colliderect(self.player.hitbox_rect):
                print("item collision")
                self.score+=1
                print("self score:",self.score)
                item.kill()
                # self.item_sprites.remove(item)
                # self.all_sprites.remove(item)

    def check_constraint(self):
        if self.player.hitbox_rect.left<=0:
            self.player.hitbox_rect.left=0
        if self.player.hitbox_rect.right>=self.level_width:
            self.player.hitbox_rect.right=self.level_width

        if self.player.hitbox_rect.bottom>=self.level_height:
            self.player.health=0

    def draw(self,screen):
        screen.fill("white")
        self.all_sprites.draw(self.player.hitbox_rect.center)