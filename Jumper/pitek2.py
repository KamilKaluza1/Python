from rain import Drop
import pygame
from settings import Settings
from pygame.sprite import Group
from random import randint
import sys


class Mario():
    def __init__(self, ai_settings, screen):
        """Inicjalizacja statku kosmicznego i położenie jego..(początkowe)"""
        self.screen = screen
        self.ai_settings = ai_settings
        #Wczytanie obrazu statku kosmicznego i pobranie prostokonta jego.
        self.image = pygame.image.load('../ALIEN_SS/images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Każdy nowy statek kosmiczny pojawia się na dole ekranu
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Punkt środkowy statku jest przechowywany w postaci liczby zmiennoprzecinkowej
        self.center = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        #Opcje wskazujące na poruszanie się statku
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update(self):
        """Uaktualninie położenia statku na podstawie opcji wskaującej jego ruch"""
        #uaktualenienie wartości punktu środkowego statku a nie prostokonta
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += self.ai_settings.ship_speed_factor

        # Uaktualnienie obiektu rect na podstawie wartości self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Wyśwuetlenie statku kosmicznego w jego aktualnym położeniu"""
        self.screen.blit(self.image, self.rect)
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("pitek łappie")
    mario = Mario(ai_settings, screen)
    drops = Group()
    drop = Drop(ai_settings, screen)
    available_space = int(ai_settings.screen_width / drop.rect.width)
    for number in range(available_space):
        drop = Drop(ai_settings, screen)
        drop.rect.x = drop.rect.x * number
        drop.rect.y = randint(100, 400)
        drops.add(drops)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        mario.blitme()
        pygame.display.flip()
        screen.fill(ai_settings.bg_colour)
        drops.draw(screen)
        drops.update()
        for drop in drops.copy():
            if drop.rect.top >= ai_settings.screen_height:
                drop.rect.y = 0
