#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer


win_widht = 700
win_heiht = 500
size = (700,500)
window = display.set_mode(size)
display.set_caption('Space')
clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font2 = font.SysFont("verdana", 32)

lost = 0
score = 0
goal = 10
max_lost = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        pressedKey = key.get_pressed()
        if pressedKey[K_RIGHT] and self.rect.x < win_widht - 100:
            self.rect.x += self.speed
        if pressedKey[K_LEFT] and self.rect.x > win_widht - 700:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heiht:
            self.rect.x = randint(80, win_widht - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#class Fail():
    #def __init__(self, x, y, widht, height, color):
        #self.rect = Rect(x, y, widht, height)
        #self.rect_fill = color
    #def set_text(self, text, r_size, r_color):
        #self.image = font.Font(None, r_size).render(text, True, r_color)
    #def draw(self):
        #draw.rect(window, self.rect_fill, self.rect)
        #window.blit(self.image, (self.rect.x, self.rect.y))

#rectange.collidepoint(x, y)

spaceship = Player('rocket.png', 300, 345, 10, 120, 150)

background = transform.scale(image.load('galaxy.jpg'), size)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, win_widht - 80), -80, randint(1, 5), 80, 40)
    monsters.add(ufo)

finish =  False

rel_time = False

num_fire = 0

run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    spaceship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
      
    if not finish == True:

        spaceship.update()
        monsters.update()
        bullets.update()
        window.blit(background,(0,0))

        spaceship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('wait...', 1, (255, 255, 255))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score = score + 1
            ufo = Enemy('ufo.png', randint(80, win_widht - 80), -80, randint(1, 5), 80, 40)
            monsters.add(ufo)
        if sprite.spritecollide (spaceship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lox, (200,200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

    text_lost = font2.render('Пропущено: ' + str(lost), 1, (255,255,255))
    text_score = font2.render('Счёт:' + str(score), 1, (255,255,255))
    lox = font2.render('ТЫ проиграл',1,(255,255,255))
    #button_lost = Fail(win_widht/2, win_heiht/2, 100, 100,(255,255,255))
    #button_lost.draw()
    win = font2.render('КРАСАВЧИК БОЖЕ', 1, (255,255,255))
    window.blit(text_lost,(10,50))
    window.blit(text_score,(10,20))

        
    display.update()
    clock.tick(60)

