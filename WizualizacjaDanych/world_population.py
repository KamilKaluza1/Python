import json

# Wczytanie danych i umieszczenie ich na liście
filename = 'population_data.json'
with open(filename) as f:
    pop_data = json.load(f)

# Wyświetlenie populacji poszczególnych państw w 2010 roku.
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        print(f'{country_name}: {population}')