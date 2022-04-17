import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightStyle as LS

# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print("Kod stanu:", r.status_code)
# Umieszczenie odpowiedzi API w zmiennej.
response_dict = r.json()
print("Całkowita liczba repozytoriów:", response_dict['total_count'])

# Przetworzenie informacji o repozytoriach.
repo_dicts = response_dict['items']
print("Liczba zwróconych repozytoriów:", len(repo_dicts))
# Przeanalizowanie pierwszego repozytorium.
repo_dict = repo_dicts[0]

names, stars = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict["name"])
    stars.append(repo_dict["stargazers_count"])

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

# Utworzenie wizualizacji
my_style = LS(base_style=LCS)
chart = pygal.Bar(my_config, style=my_style)
chart.force_uri_protocol = "http"
chart.title = 'Oznaczone największą liczbą gwiazdek projekty Pythona w serwisie github'
chart.x_labels = names
chart.add("", stars)
chart.render_to_file('python_repos.svg')