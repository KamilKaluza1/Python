from pygal.maps.world import World

wm = World()
wm.force_uri_protocol = 'https'
wm.title = "Wielkość populacji w krajach Ameryki Północnej"
wm.add('Amaryka Północna', {'ca': 34126000, 'us': 309349000, 'mx': 113423000})

wm.render_to_file('na_populations.svg')