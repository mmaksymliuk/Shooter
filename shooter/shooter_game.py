from pygame import *
from random import randint   #підключення модулів

class GameSprite(sprite.Sprite):    #основний клас
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

img_bullet = "bullet.png"

class Player(GameSprite):    #дочірній клас (гравець)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
win = 0
lost = 0
score = 0
max_lost = 10
goal = 10

class Enemy(GameSprite):  #дочірній клас (ворог)
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):    #дочірній клас (куля)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height)) #параметри вікна та його створення

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

victory = font2.render("YOU WIN!", True, (255, 255, 255))
lose = font2.render("YOU LOSE!", True, (180, 0, 0)) #створення надписів про перемогу та програш


img_hero = "raketa.png" #додавання гравця
player = Player(img_hero, 5, win_height - 100, 80, 100, 10)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()  #додавання музики

fire_sound = mixer.Sound("fire.ogg")

img_enemy = "nlo.png"   #додавання ворогів
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


bullets = sprite.Group()

run = True
FPS = 60
clock = time.Clock()
finish = False  #задання частоти кадрів та основних параметрів

while run:  #ігровий цикл
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        
        window.blit(background, (0, 0))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_goal = font2.render("Збито: " + str(score), 1, (255, 255, 255))
        window.blit(text_goal, (10, 20))

        player.reset()  
        player.update()        

        monsters.update()
        monsters.draw(window)
        
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (270, 220))
        if score >= goal:
            finish = True
            window.blit(victory, (270, 220))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            
    time.delay(50)



