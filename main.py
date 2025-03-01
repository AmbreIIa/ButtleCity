import pygame
from random import randint, choice

pygame.init()

WIDTH, HEIGHT = 900, 800
FPS = 60
TILE = 50

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]




class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5
        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.keyLEFT, self.keyRIGHT, self.keyUP, self.keyDOWN, self.keySHOT = keyList

    def update(self):
        oldX, oldY = self.rect.topleft

        if keys[self.keyLEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.moveSpeed
                self.direct = 3
        elif keys[self.keyRIGHT]:
            if self.rect.right < WIDTH:
                self.rect.x += self.moveSpeed
                self.direct = 1
        elif keys[self.keyUP]:
            if self.rect.top > 0:
                self.rect.y -= self.moveSpeed
                self.direct = 0
        elif keys[self.keyDOWN]:
            if self.rect.bottom < HEIGHT:
                self.rect.y += self.moveSpeed
                self.direct = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            self.shoot()

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def shoot(self):
        dx, dy = DIRECTS[self.direct]
        Bullet(self, self.rect.centerx, self.rect.centery, dx * self.bulletSpeed, dy * self.bulletSpeed,
               self.bulletDamage)
        self.shotTimer = self.shotDelay

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
        x, y = self.rect.centerx + DIRECTS[self.direct][0] * 40, self.rect.centery + DIRECTS[self.direct][1] * 40
        pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class AITank(Tank):
    def __init__(self, color, px, py):
        super().__init__(color, px, py, 0, (None, None, None, None, None))
        self.moveTimer = 0

    def update(self):
        if self.moveTimer <= 0:
            self.direct = choice(range(4))
            self.moveTimer = randint(30, 60)

        new_x = self.rect.x + DIRECTS[self.direct][0] * self.moveSpeed
        new_y = self.rect.y + DIRECTS[self.direct][1] * self.moveSpeed

        if 0 <= new_x <= WIDTH - TILE and 0 <= new_y <= HEIGHT - TILE:
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            self.direct = choice(range(4))

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.direct = choice(range(4))

        self.moveTimer -= 1

        if randint(0, 100) < 3:
            self.shoot()


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

    def draw(self):
        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'gray20', self.rect, 2)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
AITank('red', 650, 275)


LEVEL_MAP = [
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
]

MAP_TILE_SIZE = min(WIDTH // len(LEVEL_MAP[0]), HEIGHT // len(LEVEL_MAP))

for row_idx, row in enumerate(LEVEL_MAP):
    for col_idx, cell in enumerate(row):
        if cell == 1:
            Block(col_idx * MAP_TILE_SIZE, row_idx * MAP_TILE_SIZE, MAP_TILE_SIZE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()
    for bullet in bullets: bullet.update()
    for obj in objects:
        if hasattr(obj, 'update'):
            obj.update()
    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
