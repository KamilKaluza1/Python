import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from random import randint
from time import sleep
import pygame.font


class Button:
    def __init__(self, screen, msg):
        """Inicjalizajca początkowych wartości """
        # Zaciągnięcie obiektu scren
        self.screen = screen
        # Utworzenie prostokąta obiektu
        self.screen_rect = self.screen.get_rect()
        # Nadanie wartości wysokości szerokości kolorów przycisku
        self.wight, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.bg_color = (0, 0, 255)
        # Nadanie stylu i rozmiaru czcionki
        self.font = pygame.font.SysFont(None, 48)
        # Utworzenie prostokąta przycisku
        self.rect = pygame.Rect(0, 0, self.wight, self.height)
        # Ustawienie środka przycisku na środku ekranu
        self.rect.center = self.screen_rect.center
        # Przygotowanie wiadomości
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Umieszczenie komunikatu w wygenerowanym obrazie i wyśrodkowanie komunikatu na przycisku"""
        # Utworzenie obrazu komunikatu
        self.msg_image = self.font.render(msg, True, self.text_color, self.bg_color)
        # Utworzenie obiektu prostokąta obrazu komunikatu
        self.msg_image_rect = self.msg_image.get_rect()
        # Umieszczenie komunikatu w środku przycisku
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Wyświetlenie pustego przycisku, a następnie komunikat na nim  """
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



class Enemy(Sprite):
    """ Wróg kwadrat niebieski co popyla w dół i górę """
    def __init__(self, ai_settings, screen):
        super(Enemy, self).__init__()
        # Inicjalizowanie ekranu i ustawień
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        # strzorzenie kwadratu
        self.rect = pygame.Rect(0, 0, ai_settings.enemy_wight, ai_settings.enemy_height)
        # Ustawienie kwadratu w prawym górnym rogu
        self.rect.top = self.screen_rect.top
        self.rect.right = self.screen_rect.right
        self.color = self.ai_settings.enemy_color
        self.speed = 2

    def draw_enemy(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        # Nieskończony opad tego samego kwadratu
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.rect.y = 0


class Bullet(Sprite):
    # Inicjalizacja klasy
    def __init__(self, ai_settings, screen, ship):
        # Tworzenie klasy dziedziczącej po sprite
        super(Bullet, self).__init__()
        # Pobieranie elementów
        self.ai_settings = ai_settings
        self.screen = screen
        self.ship = ship
        # Stworzenie prostokąta w punkcie 0,0 xy- lewy góryny róg  i nadanie mu szerokości i wyskokości
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        # Przeniesienie go na czubek statku
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right
        # Umożliwiamy użycie wartości zmięnnoprzecinkowych
        self.x = float(self.rect.x)
        # Kolor pocisku
        self.color = (255, 0, 0)

    def update(self, ai_settings):
        # Pocisk leci w prawo z prędkosćią z ustawień
        self.x += ai_settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        # rysuje sprajta metodą draw
        pygame.draw.rect(self.screen, self.color, self.rect)


class Ship:
    """ Tworzenie Klasy statku kosmicznego """
    def __init__(self, ai_settings, screen):
        # Wczytujemy obiekt ustawień i ekranu
        self.ai_settings = ai_settings
        self.screen = screen
        # Wczytujemy obraz statku tworzymy jego prostokąt oraz prostokąt ekranu
        self.image = pygame.image.load("ship_poziomo.png")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        # Ustawienie statku kosmicznego z lewej strony ekranu i
        self.rect.left = self.screen_rect.left
        self.rect.centery = self.screen_rect.centery
        # Wskaźniki poruszania się w górę i w dół (nieaktywne)
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """ WYświetlanie statku kosmicznego w aktualnym położeniu jego """
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_up and self.rect.top >= 0:
            self.rect.centery -= 1
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.centery += 1


class Settings:
    """ Klasa ustawień podsrtawowych"""
    def __init__(self):
        # Nadaje wartości szerokości wysokości i koloru tła
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (233, 233, 233)
        # A dam se tutaj szerokości, wysokość, szybkość pocisku jak bym miał coś zmienić
        self.bullet_width = 30
        self.bullet_height = 30
        self. bullet_speed = 1
        # Ustawienia wroga
        self.enemy_wight = 30
        self.enemy_height = 30
        self.enemy_color = (0, 0, 255)
        self.enemy_speed_factor = 2
        # Czy gra jest aktywna
        self.game_active = False
        # Ile mamy szns
        self.lives = 1

def reset_game(ai_settings, bullets, enemys):
    ai_settings.lives = 3

    bullets.empty()
    enemys.empty()
    ai_settings.game_active = True




def check_play_button(play_button, mouse_x, mouse_y, ai_settings, bullets, enemys):
    """ Rozpoczęcie nowej gry po kliknięciu w przycisk użytkownika """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not ai_settings.game_active:
        reset_game(ai_settings, bullets, enemys)

def check_events(ship, bullets, ai_settings, screen, play_button, enemys):
    """ Sprawdza zdażenia generowane przez klawiature i mysz"""
    for event in pygame.event.get():
        # jeżeli wystąpi naciśnięcie krzyżyka zamykam
        if event.type == pygame.QUIT:
            sys.exit()
        # sprawdza reakcje na wciśnięcie przycisku
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullets, ai_settings, screen)
        # reakcja na zwolnienie gusika
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y, ai_settings, bullets, enemys)


def check_keydown_events(event, ship, bullets, ai_settings, screen):
    """ działanie poszczegónych wciśnięć guzika """
    # jeżeli naciśniemy strzałke w górę poleci do góry statek
    if event.key == pygame.K_UP:
        ship.moving_up = True
    # jeżeli naciśniemy strzałke w górę poleci na dół statek
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # jeżeli naciśniemy spacje a liczba naboii nie jest przekroczona stzelamy
    elif event.key == pygame.K_SPACE:
        if len(bullets) <= 3:
            bullet = Bullet(ai_settings, screen, ship)
            bullets.add(bullet)


def check_keyup_events(event, ship):
    """Reakcja na zwolnienie przycisku"""
    # Jeżeli puścimy strzałke statek powraca do stagnacji
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def bullet_update(bullets, ai_settings):
    """ aktualizacja pocisków """
    # Z racji że nie mozemy użyć metody draw bullets na grupe iterujemy przez jej skłądniki odświerzając pokoleji każdy
    # W każdym powturzeniu pętli
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Jak dotrze do prawej krawędzi usuwamy celem optymalizacji
    for bullet in bullets.copy():
        if bullet.rect.left >= ai_settings.screen_width:
            bullets.remove(bullet)
            ai_settings.lives -= 1



def enemy_update(ai_settings, screen, enemys, bullets):
    # W każdej iteracji pętli wyświetlamy każdego wroga z grupy jak w bulletsach
    for enemy in enemys.sprites():
        enemy.draw_enemy()
    # Jak nie ma nic w grupie robimy wroga
    if not enemys.sprites():
        make_enemy(ai_settings, screen, enemys)
    # Jak wykryjemy zdarzenie bullet z enemy too...
    if pygame.sprite.groupcollide(enemys, bullets, True, True):
        # Usuwamy wszystkich wrogów i pociski
        enemys.empty()
        bullets.empty()
        # Dajemy pause
        sleep(0.5)



def make_enemy(ai_settings, screen, enemys):
    """ Dodaje wroga w losowym miescu na y"""
    enemy = Enemy(ai_settings, screen)
    enemy.rect.y = randint(1, 800)
    enemys.add(enemy)


def run_game():
    # Inicjalizuje pygame
    pygame.init()
    # Tworze obiekt klasy ustawień
    ai_settings = Settings()
    # Tworze okno gry
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # Nadaje nagłówek gry
    pygame.display.set_caption("Inna Gra")
    # Tworzenie obiektu statku
    ship = Ship(ai_settings, screen)
    # Utworzenie Grupy naboii
    bullets = Group()
    # Utworzenie wroga
    enemys = Group()
    # Utworzenie przycisku
    play_button = Button(screen, "GRA")


# Rozpoczęcie głównej pętli zdażeń
    while True:
        # Oczekuje na zdażenie nadawane przez klawiature i mysz
        check_events(ship, bullets, ai_settings, screen, play_button, enemys)
        if ai_settings.lives <= 0:
            ai_settings.game_active = False
        if not ai_settings.game_active:
            play_button.draw_button()


        if ai_settings.game_active:
            # Aktualizacja obrazu statku
            ship.update()
            # Cały czas aktualizujemy położenie zgodnie z metodą w klasie
            enemys.update()
            # Aktualizowanie położenia naboi
            bullets.update(ai_settings)


        # Wypełnienie ekranu
        screen.fill(ai_settings.bg_colour)
        # Wyświetlanie statku
        ship.blitme()
        # Aktualizacja nabojów
        bullet_update(bullets, ai_settings)
        # Aktualizaowanie wrogów
        enemy_update(ai_settings, screen, enemys, bullets)
        # Jeżeli wykożystałeś życia wyświetla się przycisk gra i czeka na reakcje
        if not ai_settings.game_active:
            play_button.draw_button()
        # Odświerzanie ekranu
        pygame.display.flip()





# Włączenie zdefiniowanej  gry
run_game()
