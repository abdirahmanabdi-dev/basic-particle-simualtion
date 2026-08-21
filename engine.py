import taichi as ti
import taichi.math as tm

# Number of particles
n = 3
# Constants
k_constant = 8.99E9
e_charge = 1.69E-19
e_mass = 9.1E-31

# Particle Information
positions = ti.Vector.field(3, dtype=float, shape=n)

acceleration = ti.Vector.field(3, dtype=float, shape=n)
velocities = ti.Vector.field(3, dtype=float, shape=n)

forces = ti.Vector.field(3, dtype=float, shape=n)

# Intial Conditions
positions[0] = ti.Vector([0, -1.0, 0.0])
positions[1] = ti.Vector([1.0, 0.0, 0.0])
positions[2] = ti.Vector([0.0, 1.0, 0.0])

velocities[0] = ti.Vector([0.0, 0.0, 0.0])
velocities[1] = ti.Vector([0.0, 0.0, 0.0])
velocities[2] = ti.Vector([0.0, 0.0, 0.0])

charges = ti.field(dtype=float, shape=n)
masses = ti.field(dtype=float, shape=n)

# Intialise it now
charges[0] = 1 * e_charge
charges[1] = -1 * e_charge
charges[2] = -1 * e_charge

masses[0] = e_mass
masses[1] = e_mass
masses[2] = e_mass

@ti.kernel
def calculate_forces():
 for i in positions:
    forces[i] = ti.Vector([0., 0., 0.])

    for j in range(n):
        if i == j:
            continue

        r_vec = positions[i] - positions[j]
        r = r_vec.norm()

        direction = r_vec.normalized()

        force_magnitude = (
            k_constant
            * charges[i]
            * charges[j]
            / (r * r)
        )

        forces[i] += direction * force_magnitude

@ti.kernel
def calculate_accel():
    for i in forces:
        acceleration[i] = forces[i] / masses[i]

@ti.kernel
def update_velocity(dt: float):
    for i in velocities:
        velocities[i] += acceleration[i] * dt

@ti.kernel
def update_position(dt: float):
    for i in positions:
        positions[i] += velocities[i] * dt