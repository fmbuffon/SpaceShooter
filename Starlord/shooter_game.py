from pygame import *
from random import *
from time import time as timer


run = True
FPS = 60
lost = 0
score = 0
finish = False
w = 700
h = 500
lives = 3
yellow = (255,255,0)
green = (0, 255, 0)
red = (255, 0, 0)
shots = 0
reload_time = False


class GameSprite(sprite.Sprite):
    def __init__(self, pimage, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(pimage), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def Fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.y = 0
            self.rect.x = randint(0, w - 80)
            lost += 1
        

class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.y = 0
            self.rect.x = randint(0, w - 80)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player('rocket.png', 350, 400, 65, 100, 7)
enemies = sprite.Group()
for i in range (5):
    enemy = Enemy('ufo.png', randint(0, w - 80), - 50, 80, 50, randint(1, 3))
    enemies.add(enemy)
asteroids = sprite.Group()
for i in range (1):
    asteroid = Asteroid('asteroid.png', randint(0, w - 80), - 50, 80, 50, randint(2, 5))
    asteroids.add(asteroid)

mw = display.set_mode((w, h))
display.set_caption('SpaceFighter')
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
font.init()
font1 = font.SysFont('Arial', 36)
firee = mixer.Sound('fire.ogg')
firee.set_volume(0.2)
font2 = font.SysFont('Arial', 50)
lose = font2.render('YOU LOSE!', True, (255, 0, 0))
font3 = font.SysFont('Arial', 50)
Win = font3.render('YOU WIN!', True, (0, 255, 0))


bullets = sprite.Group()


while run:
    for i in event.get():
        if i.type == QUIT:
            run = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if shots < 5 and reload_time == False:
                    ship.Fire()
                    firee.play()
                    shots += 1
                if shots >= 5 and reload_time == False:
                    reload_time = True
                    time1 = timer()
    if not finish:
        mw.blit(bg, (0, 0))
        ship.reset()
        ship.update()
        enemies.draw(mw)
        enemies.update()
        text1 = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        mw.blit(text1, (10, 10))
        text2 = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        mw.blit(text2, (10, 40))
        bullets.draw(mw)
        bullets.update()
        collides = sprite.groupcollide(enemies, bullets, True, True)
        asteroids.draw(mw)
        asteroids.update()
        if reload_time == True:
            time2 = timer()
            if (time2 - time1) < 3:
                reload = font1.render('Waiting for reload', 1, red)
                mw.blit(reload, (250, 450))
            else:
                shots = 0
                reload_time = False
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(0, w - 80), - 50, 80, 50, randint(1, 3))
            enemies.add(enemy)
        if sprite.spritecollide(ship, enemies, True):
            lives -= 1
        if score == 10:
            finish = True
            mw.blit(Win, (260, 240))
        if lost == 3 or lives == 0:
            finish = True
            mw.blit(lose, (260, 245))
        if sprite.spritecollide(ship, asteroids, True):
            lives -= 1
        if lives == 3:
            text3 = font1.render('Жизни: ' + str(lives), 1, green)
        elif lives == 2:
            text3 = font1.render('Жизни: ' + str(lives), 1, yellow)
        elif lives == 1:
            text3 = font1.render('Жизни: ' + str(lives), 1, red)
        mw.blit(text3, (10, 70))
    else:
        finish = False
        lost = 0
        score = 0
        lives = 3
        shots = 0
        reload_time = False  
        for e in enemies:
            e.kill()
        for a in asteroids:
            a.kill()
        for b in bullets:
            b.kill()
        time.delay(3000) 
        for i in range (5):
            enemy = Enemy('ufo.png', randint(0, w - 80), - 50, 80, 50, randint(1, 3))
            enemies.add(enemy)
        for i in range (1):
            asteroid = Asteroid('asteroid.png', randint(0, w - 80), - 50, 80, 50, randint(2, 5))
            asteroids.add(asteroid) 


    display.update()
    time.delay(20)
