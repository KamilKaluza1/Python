import pygame
import sys
from settings import Settings
from pygame.sprite import Sprite
from pygame.sprite import Group
from random import randint
from time import sleep


class Plate(Sprite):

    def __init__(self, ai_settings, screen, pitek):

        super(Plate, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, 209, 1)
        self.rect.centerx = pitek.rect.centerx
        self.rect.top = pitek.rect.top

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, pitek):

        self.rect.centerx = pitek.rect.centerx
        self.rect.top = pitek.rect.top

    def draw_plate(self):

        pygame.draw.rect(self.screen, self.color, self.rect)


class Drop(Sprite):
    def __init__(self, ai_settings, screen):
        super(Drop, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.image.load("../ALIEN_SS/images/poop.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        how_fast = randint(1, 10)
        self.y += (how_fast / 10)
        self.rect.y = self.y


class Pitek:
    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load("../ALIEN_SS/images/pitek.png")
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        self.jump_up = False
        self.gravitation = True

    def update(self):
        if self.moving_left:
            self.rect.centerx -= 1
        if self.moving_right:
            self.rect.centerx += 1

        if self.jump_up and self.rect.top >= 400  :
            self.rect.centery -= 2
        if self.gravitation and self.rect.bottom <= self.ai_settings.screen_height:
            self.rect.centery += 1



    def blitme(self):
        self.screen.blit(self.image, self.rect)


def get_available(ai_settings, screen):
    drop = Drop(ai_settings, screen)
    avaiable_space = int(ai_settings.screen_width / drop.rect.width) -1
    return avaiable_space


def creeate_rain(ai_settings, screen, drops):
    for number in range(1):
        drop = Drop(ai_settings, screen)
        drop.rect.x = drop.rect.width * randint(1, get_available(ai_settings, screen))
        drop.rect.y = randint(0, ai_settings.screen_width)
        drops.add(drop)


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pitek = Pitek(screen, ai_settings)
    available_drops = 3



    plates = Group()
    drops = Group()
    creeate_rain(ai_settings, screen, drops)
    for number in range(2):
        plate = Plate(ai_settings, screen, pitek)
        plates.add(plate)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pitek.moving_right = True
                elif event.key == pygame.K_LEFT:
                    pitek.moving_left = True
                elif event.key == pygame.K_UP:
                    pitek.jump_up = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pitek.moving_right = False
                elif event.key == pygame.K_LEFT:
                    pitek.moving_left = False
                elif event.key == pygame.K_UP:
                    pitek.jump_up = False

        if available_drops >= 1:
            pygame.display.flip()
            screen.fill(ai_settings.bg_colour)

            pitek.blitme()
            pitek.update()
            drops.draw(screen)
            drops.update()

            for plate in plates.sprites():
                plate.update(pitek)

            for drop in drops.copy():
                if drop.rect.bottom >= 800:
                    drop.y = 0
                    available_drops -= 1
                    sleep(0.5)
            if len(drops) == 0:
                creeate_rain(ai_settings, screen, drops)
            pygame.sprite.groupcollide(plates, drops, False, True)


run_game()
