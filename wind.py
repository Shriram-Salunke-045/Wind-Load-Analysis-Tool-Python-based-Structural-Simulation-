import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Wind Parameters
# -----------------------------
wind_speed = 12  # m/s
air_density = 1.225  # kg/m^3
drag_coefficient = 1.2
area = 10  # m^2 (projected area of structure)

# -----------------------------
# 2. Wind Load Calculation
# -----------------------------
def calculate_wind_force(v, rho, Cd, A):
    return 0.5 * rho * Cd * A * v**2

force = calculate_wind_force(wind_speed, air_density, drag_coefficient, area)

print("Wind Force (N):", force)

# -----------------------------
# 3. Moment Calculation
# -----------------------------
height = 20  # m (tower height)
moment = force * height

print("Bending Moment (N.m):", moment)

# -----------------------------
# 4. Coordinate Transformation (2D example)
# -----------------------------
theta = np.radians(30)  # wind direction angle

rotation_matrix = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

force_vector = np.array([force, 0])  # wind in x-direction

transformed_force = rotation_matrix @ force_vector

print("Transformed Force Vector:", transformed_force)

# -----------------------------
# 5. Load Distribution (Height-wise)
# -----------------------------
heights = np.linspace(0, height, 10)
load_distribution = force * (heights / height)  # linear distribution

# -----------------------------
# 6. Visualization
# -----------------------------
plt.figure(figsize=(6,4))
plt.plot(load_distribution, heights, marker='o')
plt.xlabel("Wind Load (N)")
plt.ylabel("Height (m)")
plt.title("Wind Load Distribution on Tower")
plt.grid()
plt.show()