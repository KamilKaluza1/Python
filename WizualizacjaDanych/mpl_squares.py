import matplotlib.pyplot as plt

input_values = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]
plt.plot(input_values, squares, linewidth=5)

# Zdefiniowanie tytułu wykresu i etykiety osi
plt.title("Kwadraty liczb", size=24)
plt.xlabel("Wartość", size=14)
plt.ylabel("Kwadraty wartości", size=14)

# Zdefiniowanie wielkości etykiet
plt.tick_params(axis='both', labelsize=14)

plt.show()
