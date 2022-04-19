import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

my_style = LS('#333366', base_style=LCS)
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.force_uri_protocol = 'http'
chart.title = 'Projekty Pythona'
chart.x_labels = ['public-apis', 'system-design-premier', 'Python']

plot_dicts =[
    {'value': 189533, 'label': 'Opis projektu public-apis'},
    {'value': 174486, 'label': 'Opis projektu system-design-premier'},
    {'value': 134648, 'label': 'Opis projektu Python'},
]
chart.add('', plot_dicts)
chart.render_to_file('bar_descriptions.svg')