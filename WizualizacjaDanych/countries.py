from pygal.maps.world import COUNTRIES

list = []
for country_code in sorted(COUNTRIES.keys()):
    print(country_code, COUNTRIES[country_code])
    list.append(country_code)
print(len(list))
