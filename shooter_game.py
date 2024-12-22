from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):

    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Космический шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
score = 0
lost = 0
max_lost = 3
goal = 30
life = 3

win = font1.render('!!ПОБЕДА!!', True, 'chartreuse3')
lose = font1.render('ПОРАЖЕНИЕ', True, 'crimson')
restart = font1.render('ПЕРЕЗАПУСК ИГРЫ', True, 'cadetblue3')

ship = Player('rocket.png', 5, win_height-80, 80, 100, 10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_height - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(30, win_height - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

finish = False
game = True
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                rel_text = font2.render('Подождите, перезарядка...', 1, 'palevioletred1')
                window.blit(rel_text, (200,430))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render(f'Счёт: {str(score)}', 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render(f'Пропущено: {str(lost)}', 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if life == 3:
            life_color = 'green1'
        if life == 2:
            life_color = 'yellow'
        if life == 1:
            life_color = 'red'
        if life == 0:
            life_color = 'brown4'
        asteroids.update()
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (600, 20))
        display.update()

    else:
        time.delay(3000)
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()

        for i in range(5):
            monster = Enemy('ufo.png', randint(80, win_height - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    time.delay(50)