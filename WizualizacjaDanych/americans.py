from pygal.maps.world import World

wm = World()
wm.force_uri_protocol = "http"
wm.title = "Ameryka północna, Środkowa i Południowa"

wm.add('Ameryka Północna', ['ca', 'mx', 'us'])
wm.add('Amaryka Środkowa', ['bz', 'cr', 'gt', 'hn', 'ni', 'pa', 'sv'])
wm.add('Amaryka Południowa', ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'gf', 'gy', 'pe', 'py', 'sr', 'uy', 've'])
wm.render_to_file('americans.svg')