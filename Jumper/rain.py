import pygame
from pygame.sprite import Group
import sys
from pygame.sprite import Sprite
from settings import Settings
from random import randint


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


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("rain")
    drops = Group()
    drop = Drop(ai_settings, screen)
    available_space = int(ai_settings.screen_width / drop.rect.width)
    for number in range(available_space):
        drop = Drop(ai_settings, screen)
        drop.rect.x = drop.rect.width * number
        drops.add(drop)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        screen.fill(ai_settings.bg_colour)
        drops.draw(screen)
        drops.update()
        for drop in drops.copy():
            if drop.rect.top >= 800:
                drop.y = 0




run_game()