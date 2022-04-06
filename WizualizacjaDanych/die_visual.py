import pygal

from die import Die

die_1 = Die(10)
die_2 = Die(10)
results = []
throws = 10000
for roll_num in range(throws):
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
hist.force_uri_protocol = 'https'

hist.title = f"Wyniki rzucania kośćmi D{die_1.num_sides} + D{die_2.num_sides} {throws} razy."
hist.x_labels = [str(x) for x in range(2, (die_1.num_sides + die_2.num_sides) + 1)]
hist.x_title = "Wynik"
hist.y_title = "Częstotliwość występowania wartości."
hist.add(f'D{die_1.num_sides} + D{die_2.num_sides}', frequencies)
hist.render_to_file('die_visual.svg')
