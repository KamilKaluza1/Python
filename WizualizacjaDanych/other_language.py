# Wykonaj wywołanie API, aby generowało wykres pokazujący
# najpopularniejsze projekty w wybranym języku. Spróbuj przygotować wykres dla języków takich
# jak JavaScript, Ruby, C, Java, Perl, Haskell i Go.
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.


def get_git_repos_info(language):
    url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars'
    r = requests.get(url)
    print(f'Kod stanu: {r.status_code}'
          f'\nWybrany język: {language}')

    # Umieszczenie odpowiedzi API w zmiennej.
    response_dict = r.json()
    print(f'Całkowita liczba repozytoriów:{response_dict["total_count"]}')

    # Przetworzenie informacji o repozytoriach.
    repo_dicts = response_dict['items']
    print(f"Liczba zwróconych repozytoriów: {len(repo_dicts)}")

    # Przeanalizowanie pierwszego repozytorium
    repo_dict = repo_dicts[0]

    names, plot_dicts = [], []
    for repo_dict in repo_dicts:
        names.append(repo_dict["name"])
        plot_dict = {
            'value': repo_dict['stargazers_count'],
            'label': repo_dict['description'],
            'xlink': repo_dict['html_url']
        }
        plot_dicts.append(plot_dict)

    my_config = pygal.Config()
    my_config.x_label_rotation =45
    my_config.show_legend = False
    my_config.title_font_size = 24
    my_config.label_font_size = 14
    my_config.major_label_font_size = 18
    my_config.truncate_label =15
    my_config.show_y_guides = False
    my_config.width = 1000

    # Utworzenie wizualizacji
    my_style = LS('#333366', base_style=LCS)
    chart = pygal.Bar(my_config, style=my_style)
    chart.force_uri_protocol = 'https'
    chart.title = f'Oznaczone największą liczbą gwiazdek projekty {language} na serwisie GitHub'
    chart.x_labels = names
    chart.add("", plot_dicts)
    chart.render_to_file('other_language.svg')

get_git_repos_info("Go")