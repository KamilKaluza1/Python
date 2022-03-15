import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Inicjalizacja statku kosmicznego i położenie jego..(początkowe)"""
        super(Ship, self).__init__()
        #inicjalizujemy obiekty ustawien i ekranu
        self.screen = screen
        self.ai_settings = ai_settings
        #Wczytanie obrazu statku kosmicznego i pobranie prostokonta jego.
        self.image = pygame.image.load('images/ship.png')
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

    def center_ship(self):
        """ Umieszczenie statku w pozycji początkowej"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

