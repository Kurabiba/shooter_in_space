from pygame import *
from random import *
import time as py_time



class GameSprate(sprite.Sprite):
    def __init__(self, image_l, speed, x_p, y_p, x_ast, y_ast):
        super().__init__()
        self.image  = transform.scale(image.load(image_l), (x_ast, y_ast))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x_p
        self.rect.y = y_p   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprate):
    def __init__(self, image_l, speed, x_p, y_p, x_ast, y_ast):
        super().__init__(image_l, speed, x_p, y_p, x_ast, y_ast)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 620 :
            self.rect.x += self.speed
    def fire(self):
        bull = Bullet("bullet.png", 10, rocket.rect.centerx-13, rocket.rect.top-20, 30, 40)
        bullets.add(bull)

class Enemy(GameSprate):
    def update(self):
        if self.rect.y > 500:
            self.rect.y = 0
            self.speed = randint(1, 5)
            self.rect.x = randint(20, 650)
            global lost
            lost += 1
        self.rect.y += self.speed

class Asteroid(GameSprate):
    def update(self):
        if self.rect.y > 500:
            self.rect.y = 0
            self.speed = randint(1, 5)
            self.rect.x = randint(20, 650)
        self.rect.y += self.speed

class Bullet(GameSprate):

    def update(self):   
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

        
setWinn = [700, 500]
window = display.set_mode(setWinn)
display.set_caption("Что-то про космос")
background = transform.scale(image.load("galaxy.jpg"), (setWinn))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
s = mixer.Sound("fire.ogg")

rocket = Player("rocket.png", 10, 300, 400, 65, 65)
bullets = sprite.Group()
monsters = sprite.Group()
ast = sprite.Group()

for i in  range(5):
    ufo = Enemy("ufo.png", randint(1, 3), randint(20, 650), randint(-60, -20), 65, 65)
    monsters.add(ufo)

for e in range(3):
    asts = Asteroid("asteroid.png", randint(1, 3), randint(20, 650), randint(-60, -20), 65, 65)
    ast.add(asts)

clock = time.Clock()
FPS = 60
lost = 0
kill = 0
font.init()
fon = font.SysFont("Arial", 30)
end = False
game = True
amount = 5
redbull = False
timeocl = 0
rel = ""
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if amount !=0:
                    rocket.fire()
                    s.play()
                    amount -= 1

    if end != True:
        monsters.update()
        ast.update()
        rocket.update()
        bullets.update()
        window.blit(background, (0, 0))
        rocket.reset()
        monsters.draw(window)
        ast.draw(window)
        bullets.draw(window) 


        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        sprite_ast = sprite.groupcollide(bullets, ast, True, False)

        for i in sprite_list:
            kill += 1
            asteroid = Enemy("ufo.png", randint(1, 3), randint(20, 650), randint(-60, -20), 65, 65)
            monsters.add(asteroid)

        if kill >= 10:
            win = fon.render(("WIN"), True, [255, 255, 255])
            window.blit(win, (300, 230))
            end = True

        if lost >= 5:
            wast = fon.render(("LOSE"), True, [255, 255, 255])
            window.blit(wast, (300, 230))
            end = True

        if amount == 0:
            redbull = True
            rel = "Перезарядка"
        if redbull:
            if timeocl == 0:
                timeocl = py_time.time()

            if py_time.time() - timeocl >=3:
                amount = 5
                redbull = False
                timeocl = 0
                rel = ""
    

        losts = fon.render("Пропущено: " + str(lost), True, [255, 255, 255])
        kills = fon.render("Убито: " + str(kill), True, [255, 255, 255])
        biilis = fon.render("Пули: " + str(amount), True, [255, 255, 255])
        amm = fon.render(rel,  True, [255, 255, 255])
        window.blit(losts, (10, 10)) 
        window.blit(kills, (10, 40))
        window.blit(biilis, (600, 10))
        window.blit(amm, (255, 400)) 
    display.update()
    clock.tick(FPS)