import matplotlib.pyplot as plt
from random_walk import RandomWalk

while True:
    rw = RandomWalk(50)
    rw.fill_walk()
    # Określenie wielkości okna
    plt.figure(figsize=(14, 6))
    point_numbers = list(range(rw.num_points))
    plt.plot(rw.x_values, rw.y_values, linewidth=0.5)
    # Oznaczenie punktu początku i końca RW
    plt.scatter(0, 0, c='green', edgecolors='none', s=100)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c="red", edgecolors='none', s=100)

    # Ukrycie osi
    plt.axis("off")

    plt.show()

    keep_running = input("Utworzyć kolejne błądzenie losowe? (Y/N)")
    if keep_running == 'n':
        break
