import pygame
import random
import button

from settings import *

pygame.init()

clock = pygame.time.Clock()

# window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('RPG do Demi')

# game variables
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False

# font and colors
fonte = pygame.font.Font("assets/RPGSystem.ttf", 26)
grey = (28, 28, 28)
white = (255, 255, 255)
black = (0, 0, 0)
red = (128, 0, 0)

# assets
# background
bg_img = pygame.image.load('assets/Background.png').convert_alpha()
# panel
panel_img = pygame.image.load('assets/panel.png').convert_alpha()
# sword
sword_img = pygame.image.load('assets/sword.png').convert_alpha()
# pots
potion_img = pygame.image.load('assets/potion.png').convert_alpha()


# draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.blit(bg_img, (0, 0))


def draw_panel():
    screen.blit(panel_img, (0, HEIGHT - BOTTOM_PANEL))
    # Knight Stats
    draw_text(f'{knight.name} HP: {knight.hp}', fonte, grey, 135, HEIGHT - BOTTOM_PANEL + 10)

    draw_text(f'{wizard.name} HP: {wizard.hp}', fonte, grey, 530, HEIGHT - BOTTOM_PANEL + 10)


class Fighter:
    def __init__(self, x, y, name, max_hp, strength, pots):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_pots = pots
        self.pots = pots
        self.alive = True
        self.animation_list = []
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:death
        # idle
        temp_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(10):
            img = pygame.image.load(f'assets/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2.6, img.get_height() * 2.6))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack
        temp_list = []
        self.update_time = pygame.time.get_ticks()
        for i in range(4):
            img = pygame.image.load(f'assets/{self.name}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2.6, img.get_height() * 2.6))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, alvo):
        # damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        alvo.hp -= damage
        if alvo.hp < 1:
            alvo.hp = 0
            alvo.alive = False
        # animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= (len(self.animation_list[self.action])):
            self.idle()

    def draw(self):
        screen.blit(self.image, self.rect)


class Wizard:
    def __init__(self, x, y, name, max_hp, strength, pots):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_pots = pots
        self.pots = pots
        self.alive = True
        self.animation_list = []
        self.action = 0  # 0:idle, 1:run, 2:hurt, 3:death
        # idle
        temp_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # attack
        temp_list = []
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # hurt
        temp_list = []
        self.update_time = pygame.time.get_ticks()
        for i in range(3):
            img = pygame.image.load(f'assets/{self.name}/hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, alvo):
        # damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        alvo.hp -= damage
        if alvo.hp < 1:
            alvo.hp = 0
            alvo.alive = False
        # animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= (len(self.animation_list[self.action])):
            self.idle()

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp

        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, white, (self.x + 1, self.y - 1, 150, 20))
        pygame.draw.rect(screen, white, (self.x - 1, self.y + 1, 150, 20))
        pygame.draw.rect(screen, grey, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, red, (self.x, self.y, 150 * ratio, 20))


knight = Fighter(200, 233, 'Knight', 35, 10, 3)
wizard = Wizard(700, 255, 'Wizard', 200, 12, 5)

knight_health_bar = HealthBar(120, HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
wizard_health_bar = HealthBar(520, HEIGHT - BOTTOM_PANEL + 40, wizard.hp, wizard.max_hp)

# buttons
pot_button = button.Button(screen, 100, HEIGHT - BOTTOM_PANEL + 70, potion_img, 64, 64)

loop = True
while loop:

    clock.tick(FPS)
    draw_bg()
    draw_panel()

    knight_health_bar.draw(knight.hp)
    wizard_health_bar.draw(wizard.hp)

    knight.update()
    knight.draw()

    wizard.update()
    wizard.draw()

    attack = False
    potion = False
    target = None
    pygame.mouse.set_visible(True)

    pos = pygame.mouse.get_pos()
    if wizard.rect.collidepoint(pos):
        pygame.mouse.set_visible(False)
        screen.blit(sword_img, pos)
        if clicked:
            attack = True
            target = wizard

    if pot_button.draw():
        potion = True

    # player action
    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # attack
                if attack and target is not None:
                    knight.attack(target)
                    current_fighter += 1
                    action_cooldown = 0

    # enemy action
    if current_fighter == 2:
        if wizard.alive:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # attack
                wizard.attack(knight)
                current_fighter += 1
                action_cooldown = 0

    if current_fighter > total_fighters:
        current_fighter = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
