#Muhammad Zeeshan
#261940660
#COMP 111A

import pygame
import time
import random

pygame.init()

width,height=750,500
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Game")
#Loading images
enemyship=pygame.transform.scale(pygame.image.load("enemyshipb.png"), (150,150))

whiteast=pygame.transform.scale(pygame.image.load("whiteast.png"),(150,150))

coin=pygame.transform.scale(pygame.image.load("coinb.png"), (75,75))

asteroid=pygame.transform.scale(pygame.image.load("asteroidb.png"),(100,100))

bg=pygame.transform.scale(pygame.image.load("pinkspacegame.jpg"), (width,height))

ship=pygame.transform.scale(pygame.image.load("spaceshipb.png"), (150,150))

laser=pygame.transform.scale(pygame.image.load("laserb.png"),(150,150))
weapon=pygame.transform.scale(pygame.image.load("weaponb.png"), (75,75))

shield=pygame.transform.scale(pygame.image.load("shieldb.png"), (75,75))

#Collision function
#Calculates offset of x and y separately and uses overlap to detect pixel perfect collision
def collide(fobj,sobj):
    offx=sobj.x-fobj.x
    offy=sobj.y-fobj.y
    return fobj.hitbox.overlap(sobj.hitbox, (offx,offy))

#Powerup class
class Powerup:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def grav(self,speed):
        self.y+=speed

#Derived classes of powerup that each give different advantages to the player
class Coin(Powerup):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img=coin
        self.hitbox=pygame.mask.from_surface(self.img)
        self.scoregive=25

    def form(self,gamewin):
        gamewin.blit(self.img,(self.x,self.y))

    def givebuff(self,playerobj):
        playerobj.score.increase(self.scoregive)
            
        
class Weapon(Powerup):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img=weapon
        self.hitbox=pygame.mask.from_surface(self.img)
        self.ammogive=10

    def form(self,gamewin):
        gamewin.blit(self.img,(self.x,self.y))

    def givebuff(self,playerobj):
        playerobj.ammo.increase(self.ammogive)

class Shield(Powerup):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img=shield
        self.hitbox=pygame.mask.from_surface(self.img)
        self.shgive=5

    def form(self,gamewin):
        gamewin.blit(self.img,(self.x,self.y))

    def givebuff(self,playerobj):
        playerobj.shield.increase(self.shgive)

#Players way of destroying enemies        
class Magic:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img=laser
        self.hitbox=pygame.mask.from_surface(self.img)

    def formmag(self, gamewin):
        gamewin.blit(self.img, (self.x,self.y))
        

    def move(self,speed):
        self.y-= speed

    def collast(self,obj):
        return collide(self,obj)

    #returns whether laser collides with enemy

#Spaceships necessary requirements score and health
class Score:
    def __init__(self,start):
        self.scoreval=start

    def increase(self,ivalue):
        self.scoreval+=ivalue


class Health:
    def __init__(self,tothealth):
        self.healthvalue=tothealth

    def decrease(self,gvalue):
        self.healthvalue-=gvalue

    def increase(self,ivalue):
        self.healthvalue+=ivalue

#Ships attack and protection abilities
class ShipAbilities:
    def __init__(self,svalue):
        self.value=svalue

    def increase(self,given):
        self.value+=given

    def decrease(self,given):
        self.value-=given

class Ammo(ShipAbilities):
    pass

class ShieldSt(ShipAbilities):
    pass
        
#Player class requires a totsl health value a starting score value and one ammo object and shield object to
#determine its abilities
class Player:
    def __init__(self,x,y,hval,sval,ammobj,shobj):
        self.x=x
        self.y=y
        self.health=Health(hval)
        self.shipimg= None
        self.score=Score(sval)
        self.magic=[]
        self.shield=shobj
        self.ammo=ammobj

    #drawing ships image
    def form(self,gamewin):
        gamewin.blit(self.shipimg,(self.x,self.y))
        for i in self.magic:
            i.formmag(screen)

    #ship/player movement

    def moveleft(self):
        self.x-=3

    def moveright(self):
        self.x+=3

    def moveup(self):
        self.y-=3

    def movedown(self):
        self.y+=3

    def shoot(self):
        if self.ammo.value>0:
            magic1=Magic(self.x,self.y)
            self.magic.append(magic1)
            self.ammo.decrease(1)

class Spaceship(Player):
    def __init__(self,x,y,hval,sval,ammobj,shobj):
        super().__init__(x,y,hval,sval,ammobj,shobj)
        self.shipimg=ship
        self.hitbox=pygame.mask.from_surface(self.shipimg)
        #ships mask that is used to detect overlapping and cause collision

#Enemy can destroy a player object shield (if any) or their health if there is no shield after collision detected
#by collide(fobj,sobj)
class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.astimg= None
        self.health=Health(1)

    def form(self,gamewin):
        gamewin.blit(self.astimg,(self.x,self.y))

    def fall(self, speed):
        self.y+=speed

    def destroyhealth(self,playerobj):
        playerobj.health.decrease(1)

    def destroyshield(self,playerobj):
        playerobj.shield.decrease(1)


#Deriving enemy ship and asteroid from Enemy and creating theirmasks
class Asteroid(Enemy):
    def __init__(self,x,y,img):
        super().__init__(x,y)
        self.astimg=img
        self.hitbox=pygame.mask.from_surface(self.astimg)
        self.vspeed1=random.randint(3,7)
        self.vspeed2=random.randint(-5,5)
        
    #at the time of creation every asteroid obj will have a different speed value
    #and depending on which part of the screen the come from that random speed is incremented
    #disperse() for asteroid coming up from the screen
    #clashright() for asteroids going from left to right
    #clashleft() for asteroids going from right to left
        
    def disperse(self):
        self.y+=self.vspeed1
        self.x+=self.vspeed2

    #overriding fall function to allow every asteroid obj to move at
        #random speed at runtime
       
class EnemyShip(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.astimg=enemyship
        self.hitbox=pygame.mask.from_surface(self.astimg)
        self.health=Health(5)
                                             
def main():
    run= True
    fps=60
    ammo1=Ammo(25)
    shield1=ShieldSt(0)
    player=Spaceship(150,350,50,0,ammo1,shield1)
    #player obj of spaceship type created with ammo and shield objects
    fontgame=pygame.font.SysFont("timesnewroman",30)
    clock= pygame.time.Clock()
    #list to store asteroids enemys and buffs
    oppasteroids=[]
    eships=[]
    buffs=[]
    bufflow=1
    spawnrate=0
    failed=False

    def drawscreen():
        screen.blit(bg,(0,0))
        #displaying ships information
        healthstring= fontgame.render(f"Remaining Power:{player.health.healthvalue}",1,(255,255,255))
        scorestring= fontgame.render(f"Score:{player.score.scoreval}",1,(255,255,255))
        maxscore= fontgame.render(f"Highest Score: {h}",1,(255,255,255))
        ammostring= fontgame.render(f"Ammo: {player.ammo.value}",1,(255,255,255))
        shstring= fontgame.render(f"Shield Strength: {player.shield.value}",1,(255,255,255))
        screen.blit(healthstring,(20,20))
        screen.blit(ammostring, (20,45))
        screen.blit(scorestring, (width-150,20))
        screen.blit(maxscore,(width-250,45))
        screen.blit(shstring, (20,450))
        player.form(screen)
        #forming asteroids enemyships and buffs on screen based on their position (x,y) in the list
        for i in oppasteroids:
            i.form(screen)
        for i in eships:
            i.form(screen)
        for i in buffs:
            i.form(screen)
        pygame.display.update()
        

    while run==True:
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            pygame.quit()  
            run=False

        #when power is 0 end game and write the highscore no matter if its beaten or not as
        #that is determined by a statement at the end of this code
        if player.health.healthvalue==0:
            p=open("score.txt","w")
            p.write(str(h))
            failed=True
            break
            
        #when the lists run out of objects (length is zero) add more objects to list
        #and make random position for them to fall above the screens height
        #buffs contains different kinds of powerups
        if len(oppasteroids)==0:
            spawnrate+=3
            for i in range(spawnrate):
                asteroid1=Asteroid(random.randint(50, width-100),random.randint(-800,-100),asteroid)
                oppasteroids.append(asteroid1)

        if len(eships)==0:
           for i in range(bufflow):
               enemy1=EnemyShip(random.randint(50, width-100),random.randint(-800,-100))
               eships.append(enemy1)
                
        if len(buffs)==0:
            for i in range(bufflow):
                weapon1=Weapon(random.randint(50, width-100),random.randint(-800,-100))
                shield1=Shield(random.randint(50,width-100),random.randint(-800,-100))
                coin1=Coin(random.randint(50,width-100),random.randint(-800,-100))
                buffs.append(weapon1)
                buffs.append(shield1)
                buffs.append(coin1)
                
        #Iterating through the list and increasing y values based on some speed
        #checking for collisions using collide and setting the
        #difference each objects makes to the player ship when it
        #collides with the playership
                
        for i in oppasteroids:
            i.disperse()
            if collide(i,player):
                if player.shield.value>0:
                    i.destroyshield(player)
                    #this loop is applied anywhere an obj is supposed to disappear
                    #itcheck if the obj was removed due to some other event and is not in list
                    # but if it wasnt removed and is still in list then remove it
                    if i in oppasteroids:
                        oppasteroids.remove(i)
                else:
                    i.destroyhealth(player)
                    if i in oppasteroids:
                        oppasteroids.remove(i)
            if i.y>height or i.x>width or i.x<0:
                                    player.score.increase(1)
                                    if i in oppasteroids:
                                        oppasteroids.remove(i)                            
                

        #loop for ships to fall downwards/towards players
        for i in eships:
            i.fall(3)
            if collide(i,player):
                if player.shield.value>0:
                    i.destroyshield(player)
                    if i in eships:
                        eships.remove(i)
                else:
                    i.destroyhealth(player)
                    if i in eships:
                        eships.remove(i)
            if i.y>height:
                if i in eships:
                        eships.remove(i)

            
        for i in buffs:
            i.grav(2)
            if collide(i,player):
                i.givebuff(player)
                #only when power is less than 50 increase spaceships power by 5 after receiving any
                #powerup
                if player.health.healthvalue<50:
                    player.health.increase(5)
                if i in buffs:
                    buffs.remove(i)
            if i.y>height:
                if i in buffs:
                    buffs.remove(i)


        #checking players actions using keys dictionary to control the ships movements
        #and checking if left mouse button is click to shoot
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.moveleft()
        if keys[pygame.K_RIGHT]:
            player.moveright()
        if keys[pygame.K_UP]:
            player.moveup()
        if keys[pygame.K_DOWN]:
            player.movedown()
        if keys[pygame.K_SPACE]:
            player.shoot()
        

        #shoot() checks ammo if greater than 0 then appends an object of Magic class
        #that is set in the current position of player and it
        #is shot out of the player by the move function in
        #the for loop below and checks collisions to decrease enemy health and remove
        #enemy obj from their corresponding lists

        for i in player.magic:
              i.move(3)
              if i.y<0:
                  player.magic.remove(i)
              for j in oppasteroids:
                  if i.collast(j):
                     player.score.increase(1) 
                     j.health.decrease(1)
                     if j.health.healthvalue==0:
                         if j in oppasteroids:
                            oppasteroids.remove(j)
                                       
                         
        for i in player.magic:
              i.move(3)
              if i.y<0:
                  player.magic.remove(i)
              for j in eships:
                  if i.collast(j):
                     player.score.increase(5) 
                     j.health.decrease(1)
                     if j.health.healthvalue==0:
                         if j in eships:
                            eships.remove(j)
                            
        #reading highscore from a textfile
        #comparing it to players current score
        #seeing if its greater then writing new value of highscore which is players score
        f=open("score.txt","r")
        highscore=f.read()
        h=int(highscore)
        if player.score.scoreval>h:
            h=player.score.scoreval
            f=open("score.txt","w")
            f.write(str(h))
                     
        
        drawscreen()
        clock.tick(fps)
##    pygame.quit()
        
main()

        
