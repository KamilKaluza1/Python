import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Inicjalizacja gry i utworzenie obiektu ekranu
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Inwazja obcych")
    # Utworzenie egzemplarza przeznaczonego do przechowywania danych statystycznych
    stats = GameStats(ai_settings)
    # Utworzenie egzemplarza klasy Scoreboard
    sb = Scoreboard(ai_settings, screen, stats)
    # Utworzenie przycisku gra
    play_button = Button(ai_settings, screen, "Gra")

    # Utworzenie Obcego
    aliens = Group()
    # Utworzenie statku kosmicznego
    ship = Ship(ai_settings, screen)
    # Utworzenie floty obcych
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Utworzenie grupy przeznaczonej do przechowywania pocisków
    bullets = Group()

#Rozpoczęcie pętli głównej
    while True:
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)
        if stats.game_active:
            # Oczekiwanie na naciśnięcie klawisza

            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, bullets, aliens, ship, sb)
            # aktualizacja ekranu z game functions

        gf.update_screen(ai_settings, screen, sb, ship, aliens, bullets, play_button, stats)

run_game()