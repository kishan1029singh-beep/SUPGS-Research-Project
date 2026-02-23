# CO2 vs Vehicle Growth Graph
# Author: Kishan Singh

import matplotlib.pyplot as plt

# Sample data (example model)
vehicles = [10, 20, 30, 40, 50, 60]
co2_without_system = [20, 35, 50, 65, 80, 95]
co2_with_supgs = [20, 32, 45, 57, 70, 82]

# Plot graph
plt.plot(vehicles, co2_without_system, label="Without Green System")
plt.plot(vehicles, co2_with_supgs, label="With SUPGS Model")

# Labels
plt.xlabel("Vehicle Growth")
plt.ylabel("CO2 Level")
plt.title("CO2 Reduction using SUPGS Model")

plt.legend()
plt.show()
