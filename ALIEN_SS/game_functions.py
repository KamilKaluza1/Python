import sys
import pygame
from ALIEN_SS.bullet import Bullet
from ALIEN_SS.alien import Alien
from time import sleep


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_aliens_bottoms(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ Sprawdzanie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Tak samo, jak w przypadku zderzenia z obcym
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ Reakcja na uderzenie obcego w statek kosmiczny"""
    if stats.ships_left > 0:
        # Zmniejszenie wartości przechowywanej w ship_left
        stats.ships_left -= 1
        sb.prep_ships()

        # Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()

        # Utworzenie nowej floty u wyśrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        # Gra kończy się a kursor staje się widzialny
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_key_down_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb):
    """ Reakcja-wciśnięcie klawisza """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_g:
        if not stats.game_active:
            start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Wystrzelenie pocisku, jeżeli nie przekroczono ustalonego limitu
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_key_up_events(event, ship):
    """Reakcja na zwolnienie klawisza"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
    """Reakcja na zdarzenia generowane przez klawiaturę i mysz"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb)

        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    # Znika kursor
    pygame.mouse.set_visible(False)
    # Resetuje ilość statków zmienia status gry na aktywny
    stats.reset_stats()
    stats.game_active = True
    # Wyzerowanie obrazów tablicy wyników
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # Usuniecie obcych i pocisków z listy
    aliens.empty()
    bullets.empty()
    # Utworzenie nowej floty, wyśrodkowanie statku
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    """ Rozpoczęcie nowej gry po kliknięciu przycisku gra przez użytkownika """
    # Przycisk zostaje użyty, jeżeli naciśniesz w prostokacie gra
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # Przycisk spełnia swoją funkcję, jeżeli go naciśniesz i status gry jest nieaktywny
    if button_clicked and not stats.game_active:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)
        # Wyzerowanie ustawień dotyczących gry
        ai_settings.initialize_dynamic_settings()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    # uaktualnienie położenia pocisków
    bullets.update()
    # Usunięcie pocisków, które znajdują się poza ekranem
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # Inkrementacja numeru poziomu
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    """ Utworzenie pełnej floty obcych """
    # Utworzenie obcego i ustalenie liczby obcych, którzy zmieszczą się w rzędzie.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """ Ustalenie ile rzędów zmieści się na ekranie """
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """ Ustalenie liczby obcych, którzy zmieszczą się w rzędzie """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Utworzenie obcego i umieszczenie go w rzędzie """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (2 * alien.rect.height) + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_aliens(ai_settings, stats, screen, bullets, aliens, ship, sb):
    """ Sprawdzanie, czy flota znajduje się przy krawędzi ekranu, a następnie uaktualnienie położenia wszystkich
    obcych we flocie """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
    check_aliens_bottoms(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_fleet_edges(ai_settings, aliens):
    """ Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Przesunięcie całej floty w dół i zmiana kierunku, w którym się porusza"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_screen(ai_settings, screen, sb, ship, aliens, bullets, play_button, stats):
    # Odświeżenie ekranu w każdej iteracji pętli
    screen.fill(ai_settings.bg_color)
    # Ponowne wyświetlanie wszystkich pocisków pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Wyświetlanie statku
    ship.blitme()
    # Wyświetlanie floty obcych
    aliens.draw(screen)
    # Wyświetlanie informacji o punktacji
    sb.show_score()
    # Wyświetlanie przycisku, gdy gra jest nieaktywna
    if not stats.game_active:
        play_button.draw_button()
    # Wyświetlanie zmodyfikowanego ekranu
    pygame.display.flip()
