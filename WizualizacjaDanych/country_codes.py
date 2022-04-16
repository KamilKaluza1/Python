from pygal.maps.world import COUNTRIES

def get_country_code(country_name):
    """ Zwraca stosowany przez Pygal dwuznakowy kod państwa przypisany danemu państwu. """
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
