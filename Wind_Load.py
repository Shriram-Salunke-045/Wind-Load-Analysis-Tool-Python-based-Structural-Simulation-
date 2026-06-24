import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Wind Turbine Tower Model
# -----------------------------
height = 80  # meters
nodes = 20
z = np.linspace(0, height, nodes)

# -----------------------------
# 2. Material / Structural Properties
# -----------------------------
E = 2.1e11       # Young's Modulus (Pa)
I = 1.2e-3       # Moment of inertia (m^4)
m_total = 5000   # total mass (kg)

# mass distribution (linear)
mass = np.linspace(300, 100, nodes)

# -----------------------------
# 3. Natural Frequency (simplified cantilever beam)
# -----------------------------
def natural_frequency(E, I, m, L):
    return (1 / (2 * np.pi)) * np.sqrt((3 * E * I) / (m * L**3))

fn = natural_frequency(E, I, m_total, height)
print("Natural Frequency (Hz):", fn)

# -----------------------------
# 4. Wind Model (Turbulent + Gust)
# -----------------------------
time = np.linspace(0, 60, 300)

base_wind = 12  # m/s
gust = 5 * np.sin(0.2 * time)  # turbulence
wind_speed = base_wind + gust

rho = 1.225
Cd = 1.2
area = 8  # projected area per node

# -----------------------------
# 5. Wind Force at Each Node
# -----------------------------
forces_time = []

for v in wind_speed:
    force_nodes = 0.5 * rho * Cd * area * v**2 * (z / height)
    forces_time.append(force_nodes)

forces_time = np.array(forces_time)

# -----------------------------
# 6. Tower Dynamic Response (SDOF approximation)
# -----------------------------
omega_n = 2 * np.pi * fn
zeta = 0.05  # damping ratio

response = []

for i, f in enumerate(forces_time):
    excitation = np.sum(f)
    
    # dynamic amplification factor (simplified)
    r = (omega_n / (2 * np.pi * np.mean(wind_speed)))
    daf = 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)
    
    response.append(excitation * daf / 1e5)

response = np.array(response)

# -----------------------------
# 7. Fatigue Damage (Simplified Miner’s Rule)
# -----------------------------
cycles = len(time)
stress_range = forces_time.max(axis=1) / 1000

damage = np.sum((stress_range / np.max(stress_range))**3) / cycles

print("Fatigue Damage Index:", damage)

# -----------------------------
# 8. Visualization
# -----------------------------

# Wind speed
plt.figure()
plt.plot(time, wind_speed)
plt.title("Wind Speed Variation (Turbulence + Gust)")
plt.xlabel("Time (s)")
plt.ylabel("Wind Speed (m/s)")
plt.grid()
plt.show()

# Load distribution snapshot
plt.figure()
plt.plot(forces_time[-1], z)
plt.title("Wind Load Distribution Along Tower (Final Snapshot)")
plt.xlabel("Force (N)")
plt.ylabel("Height (m)")
plt.grid()
plt.show()

# Structural response
plt.figure()
plt.plot(time, response)
plt.title("Tower Dynamic Response")
plt.xlabel("Time (s)")
plt.ylabel("Response Amplitude")
plt.grid()
plt.show()