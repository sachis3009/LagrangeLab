import rebound


def run_rebound_simulation():
    sim = rebound.Simulation()

    # Normalized astronomical units
    sim.units = ("AU", "yr", "Msun")

    # Primary body: Sun
    sim.add(m=1.0)

    # Secondary body: Earth
    sim.add(m=3.003e-6, a=1.0)

    # Small test satellite
    sim.add(
        m=0.0,
        a=1.01,
        e=0.01
    )

    # Center the system on its center of mass
    sim.move_to_com()

    # High-accuracy REBOUND integrator
    sim.integrator = "ias15"

    times = []
    satellite_x = []
    satellite_y = []

    # Integrate the system
    for i in range(101):

        time = i / 100

        sim.integrate(time)

        satellite = sim.particles[2]

        times.append(time)
        satellite_x.append(satellite.x)
        satellite_y.append(satellite.y)

    return times, satellite_x, satellite_y


if __name__ == "__main__":

    times, x, y = run_rebound_simulation()

    print("REBOUND simulation completed!")
    print(f"Initial satellite position: ({x[0]:.4f}, {y[0]:.4f})")
    print(f"Final satellite position:   ({x[-1]:.4f}, {y[-1]:.4f})")