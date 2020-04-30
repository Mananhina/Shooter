from pygame import sprite, transform, image, key, display, time, event, font
from pygame import K_LEFT, K_RIGHT, K_SPACE, KEYDOWN, QUIT
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 90:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('./images/bullet.png', self.rect.x + 45, self.rect.y, 30, 70, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        if self.rect.y <= 660:
            self.rect.y += self.speed
        else:
            self.rect.y = randint(-40, 0)
            self.rect.x = randint(0, 650)


class Bullet(GameSprite):
    def update(self):
        if self.rect.y >= 0:
            self.rect.y -= self.speed
        else:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = image.load("./images/grass.png")
background = transform.scale(background, (700, 150))
window.blit(background, (0, 390))

background_l = transform.scale(image.load("./images/fail.jpg"), (700, 500))

background_w = transform.scale(image.load("./images/trophy.png"), (394, 500))

hero = Player("./images/hedgehog.png", 20, 430, 90, 60, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('./images/apple.png', randint(0, 620), randint(-100, 0), 60, 60, randint(3, 7))
    monsters.add(monster)

main_en = Enemy('./images/evil_apple.png', randint(0, 560), randint(-50, 0), 150, 150, 4)

floor = GameSprite('./images/grass.png', 0, 500, 700, 15, 0)

bullets = sprite.Group()

miss = 0
max_miss = 3
score = 0
score_ap_en = 10
score_en = 0
score_en_w = 10

font.init()
local_font = font.Font(None, 36)

run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            hero.fire()

    if not finish:
        window.fill((95, 173, 245))
        window.blit(background, (0, 390))
        floor.reset()
        hero.update()
        hero.reset()
        monsters.update()

        for i in monsters:
            i.reset()
        bullets.update()
        for i in bullets:
            i.reset()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('./images/apple.png', randint(0, 620), randint(-100, 0), 60, 60, randint(3, 7))
            monsters.add(monster)
            score += 1

        fs = sprite.spritecollide(floor, monsters, True)
        for f in fs:
            monster = Enemy('./images/apple.png', randint(0, 620), randint(-100, 0), 60, 60, randint(3, 7))
            monsters.add(monster)
            miss += 1

        collide_lose = sprite.spritecollide(hero, monsters, True)
        for _ in collide_lose:
            finish = True
            window.blit(background_l, (0, 0))

        if miss > max_miss:
            finish = True
            window.blit(background_l, (0, 0))

        if score > score_ap_en:
            main_en.update()
            main_en.reset()

            if sprite.collide_rect(hero, main_en):
                finish = True
                window.blit(background_l, (0, 0))

            collide_main = sprite.spritecollide(main_en, bullets, True)
            for m in collide_main:
                score_en += 1
            if score_en > score_en_w:
                finish = True
                window.fill((0, 0, 0))
                window.blit(background_w, (170, 0))
                text_w = local_font.render("Wow! ", 1, (240, 207, 46))
                text_w2 = local_font.render("Good job! ", 1, (240, 207, 46))
                text_w3 = local_font.render("Win! ", 1, (240, 207, 46))
                window.blit(text_w, (10, 100))
                window.blit(text_w2, (10, 160))
                window.blit(text_w3, (10, 220))

        text = local_font.render("Score: " + str(score), 1, (0, 0, 0))
        window.blit(text, (10, 20))
        text1 = local_font.render("Missed: " + str(miss), 1, (0, 0, 0))
        window.blit(text1, (10, 45))
        display.update()
