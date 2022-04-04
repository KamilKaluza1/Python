import pygal

from die import Die

die_1 = Die()
die_2 = Die()
results = []
for roll_num in range(1000):
    result = die_2.roll() + die_1.roll()
    results.append(result)

# Analiza wyników
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
for value in range(2, max_result + 1):
    frequency = results.count(value)
    frequencies.append(frequency)

# Wizualizacja wyników
hist = pygal.Bar()
hist.force_uri_protocol = 'http'

hist.title = "Wyniki rzucania dwiema kośćmi D6 tysiąc razy."
hist.x_labels = [str(x) for x in range(2, 13)]
hist.x_title = "Wynik"
hist.y_title = "Częstotliwość występowania wartości."
hist.add('D6 + D6', frequencies)
hist.render_to_file('die_visual.svg')
