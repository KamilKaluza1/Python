import matplotlib.pyplot as plt
x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]


plt.scatter(x_values, y_values, s=40)
# Zdefiniowanie tytułu wykresu i etykiety osi
plt.title("Kwadraty liczb", size=24)
plt.xlabel("Wartość", size=14)
plt.ylabel("Kwadraty wartości", size=14)

# Zdefiniowanie wielkości etykiet
plt.tick_params(axis="both", which="major", labelsize=14)
# Zdefiniowanie zakresu dla każdej osi.
plt.axis([0, 1100, 0, 1100000])
plt.show()
