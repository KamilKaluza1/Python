import pygal
import requests
from operator import itemgetter
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f'Kod stanu: {r.status_code}')

# Przetworzenie informacji o każdym artykule.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:20]:
    # Przygotowanie oddzielnego wywołania API dla każdego artykułu.
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()

    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)
        }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)
names, plot_dicts = [], []
for submission_dict in submission_dicts:
    names.append(str(submission_dict['title']))
    plot_dict = {
        'value': submission_dict['comments'],
        'label': submission_dict['title'],
        'xlink': submission_dict['link']
    }
    plot_dicts.append(plot_dict)

my_config = pygal.Config
my_config.x_label_rotation = 35
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 20
my_config.show_y_guides = False
my_config.width = 900

# Utworzenie wizualizacji
my_style = LS('#333366', base_style=LCS)
chart = pygal.Bar(my_config, style=my_style)
chart.force_uri_protocol = 'https'
chart.title = "Most commented article"
chart.x_labels = names
chart.add("", plot_dicts)
chart.render_to_file('most_commented.svg')