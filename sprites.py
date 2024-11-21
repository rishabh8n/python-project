from config import *
import random

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(topleft=pos)
        # self.hitbox_rect=self.rect.inflate(hitbox_offset)
        self.old_rect=self.rect.copy()
    
    def update(self,dt):
        pass

# class AnimatedSprite(Sprite):
#     def __init__(self,pos,frames,groups,animation_speed=ANIMATION_SPEED):
#         self.frames,self.frame_index=frames,0
#         self.animation_speed=animation_speed
#         super().__init__(pos,self.frames[self.frame_index],groups)
    
#     def animate(self,dt):
#         self.frame_index+=self.animation_speed*dt
#         self.image=self.frames[int(self.frame_index)%len(self.frames)]

#     def update(self, dt):
#         self.animate(dt)

class PlayerSprite(Sprite):
    def __init__(self, pos, surf, groups, state,face,particleSizeRange=(0,40),particleXOffeset=(5,5),particleYOffset=(5,15), rotation_speed=150):
        super().__init__(pos, surf, groups)
        self.original_image = surf
        self.state=state
        self.angle = 0
        self.rotation_speed = rotation_speed
        self.original_image.set_colorkey((255,255,255))
        self.walking=False
        self.face=face
        self.particles = []
        self.particles_size=particleSizeRange
        self.particleXOffset=particleXOffeset
        self.particleYOffset=particleYOffset
        self.screen = pygame.display.get_surface()

    def update(self, dt):
        if self.state == 'jump' and self.walking:
            self.angle += self.rotation_speed*dt
            self.angle = self.angle % 360  # Keep the angle within 0-359 degrees
            self.image = pygame.transform.rotate(self.original_image, -self.angle if self.face=="right" else self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.state != 'jump':
            self.angle = 0
            self.image = self.original_image
            self.rect = self.image.get_rect(center=self.rect.center)
        
        self.create_particle()
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.lifetime <= 0:
                particle.kill()
                self.particles.remove(particle)
        
    def create_particle(self):
        pos = self.rect.center
        size = random.randint(self.particles_size[0],self.particles_size[1])
        color = (0, 0, 0)
        scaleVelocity = random.uniform(0.005,0.01)
        lifetime = random.uniform(0.5, 0.8)
        self.particles.append(ParticleSprite((random.uniform(pos[0]-self.particleXOffset[0],pos[0]+self.particleXOffset[1]),random.uniform(pos[1]-self.particleYOffset[0],pos[1]+self.particleYOffset[1])), size, color, scaleVelocity, lifetime, self.groups()))

class ParticleSprite(Sprite):
    def __init__(self, pos, size, color, scaleVelocity, lifetime, groups):
        super().__init__(pos, pygame.Surface((size, size)), groups)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        # self.velocity = pygame.Vector2(velocity)
        # self.image.set_colorkey((255,255,255))
        self.lifetime = lifetime
        self.scale=1
        self.angle = random.uniform(-180, 180)
        self.scaleVelocity= scaleVelocity
        self.image.set_colorkey((255,255,255))

    def update(self, dt):
        self.lifetime -= dt
        self.scale-=self.scaleVelocity*dt
        self.image = pygame.transform.rotozoom(self.image,0, self.scale)
        self.rect = self.image.get_rect(center=self.rect.center)


class PlatformSprite(Sprite):
    def __init__(self, pos, move_x, move_y, surf,groups,collision_sprites,player):
        self.image = surf
        super().__init__(pos,surf,groups)
        print("Self rect",surf)
        self.rect=self.image.get_frect(topleft=pos)

        self.move_direction = 1
        self.move_counter = random.randint(0, 40)
        self.move_x = move_x # flag to move in x direction
        self.move_y = move_y # flag to move in y direction
        self.collision_sprites=collision_sprites
        self.player=player

    # handle platform movement
    def update(self,dt):
        self.rect.x += self.move_direction * self.move_x*dt
        self.rect.y += self.move_direction * self.move_y*dt
        self.move_counter += 1
        if self.player.hitbox_rect.right > self.rect.left and self.player.hitbox_rect.left<self.rect.right and self.player.dir.y==0:
            self.player.hitbox_rect.x+=self.move_direction * self.move_x*dt
        self.check_collision()

    def check_collision(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.rect.left<=sprite.rect.right and self.old_rect.left>=sprite.old_rect.right:
                    self.rect.left=sprite.rect.right
                    self.move_direction *= -1
                if self.rect.right>=sprite.rect.left and self.old_rect.right<=sprite.old_rect.left:
                    self.rect.right=sprite.rect.left
                    self.move_direction *= -1
