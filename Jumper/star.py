import pygame
from settings import Settings
from pygame.sprite import Sprite
import sys
from pygame.sprite import Group
from random import randint



class Star(Sprite):

    def __init__(self, ai_settings, screen):
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load("../ALIEN_SS/images/star.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def blitme(self):
        self.screen.blit(self.image, self.rect)


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('stars')
    stars = Group()
    star = Star(ai_settings, screen)
    avaiable_space = int(ai_settings.screen_width / star.rect.width)
    number_rows = int(ai_settings.screen_height / star.rect.height)
    for number in range(0, number_rows):
        for number_star in range(0, avaiable_space):
            star = Star(ai_settings, screen)
            random_number = randint(-10, 15)
            star.rect.x = (star.rect.width * number_star) + random_number
            star.rect.y = (star.rect.height * number) - random_number
            stars.add(star)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        stars.draw(screen)

run_game()