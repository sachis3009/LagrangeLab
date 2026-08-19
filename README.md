# 🛰️ LagrangeLab

### CR3BP • Interactive Space Dynamics Simulator

LagrangeLab is an interactive simulator that visualizes the five Lagrange points in a two-body system and demonstrates satellite dynamics using the **Circular Restricted Three-Body Problem (CR3BP)**.

The project combines numerical computation, astronomy concepts, and interactive visualization to make Lagrange-point dynamics easier to understand and explore.

---

## 🚀 Problem

Lagrange points are special locations in a two-body system where the gravitational influence of the two primary bodies and the motion of a smaller object create equilibrium configurations.

Although the concept is important in orbital mechanics and space mission design, understanding the locations and stability of these points can be difficult using equations alone.

**LagrangeLab provides an interactive way to visualize and explore these locations and their dynamics.**

---

## 💡 Our Solution

LagrangeLab allows users to:

* Select a predefined **Earth–Moon** system
* Select a predefined **Sun–Earth** system
* Create a **custom two-body system**
* Calculate all five Lagrange points
* Visualize L1, L2, L3, L4 and L5
* Select a Lagrange point for simulation
* Apply a small perturbation to the selected point
* Numerically simulate satellite motion
* Explore the stability characteristics of the selected point

---

## 🌌 Scientific Approach

The simulator uses the **Circular Restricted Three-Body Problem (CR3BP)**.

The two primary bodies are assumed to:

* Have fixed masses
* Orbit their common barycenter in circular orbits
* Move in the normalized rotating reference frame

The satellite is treated as a body with negligible mass compared with the two primary bodies.

The mass parameter is defined as:

[
\mu = \frac{m_2}{m_1 + m_2}
]

The normalized positions of the two primary bodies are:

[
x_1=-\mu
]

[
x_2=1-\mu
]

The distance between the two primary bodies is normalized to 1.

---

## 📍 Calculating the Lagrange Points

### L1, L2 and L3

The three collinear Lagrange points are calculated numerically by solving the equilibrium condition:

[
\frac{\partial\Omega}{\partial x}=0
]

LagrangeLab uses the **Brent root-finding algorithm** through SciPy to numerically determine these equilibrium positions.

### L4 and L5

The triangular points are calculated analytically.

They form equilateral triangles with the two primary bodies:

[
L_4 =
\left(
\frac{1}{2}-\mu,
\frac{\sqrt{3}}{2}
\right)
]

[
L_5 =
\left(
\frac{1}{2}-\mu,
-\frac{\sqrt{3}}{2}
\right)
]

---

## 🛰️ Satellite Simulation

A small disturbance is applied to the selected Lagrange point so that its dynamical behavior can be observed.

The satellite equations of motion include:

* Gravitational acceleration
* Centrifugal effects
* Coriolis effects

The resulting system of differential equations is numerically integrated using SciPy's `solve_ivp` solver.

This allows LagrangeLab to visualize how a satellite behaves when displaced from an equilibrium location.

---

## ⚖️ Stability

The collinear points **L1, L2 and L3 are dynamically unstable**. Objects placed near these points generally require orbital corrections or station-keeping.

L4 and L5 have a different stability behavior.

For sufficiently small mass ratios, specifically below the classical Routh stability threshold:

[
\mu \approx 0.03852
]

the triangular points can be linearly stable to small perturbations.

---

## ✨ Features

### Interactive System Selection

Choose between:

* 🌍 Earth–Moon
* ☀️ Sun–Earth
* 🪐 Custom system

### Lagrange Point Visualization

Visualize all five Lagrange points and their positions relative to the two primary bodies.

### Interactive Simulation

Select a Lagrange point and run a numerical satellite simulation.

### Animated Visualization

Observe the primary bodies, Lagrange points, satellite, and satellite trajectory in an animated space visualization.

### Scientific Interpretation

The application provides an interpretation of the selected point, including whether it is collinear or triangular and its expected stability behavior.

---

## 🛠️ Technology Stack

* **Python**
* **Streamlit** — interactive web application
* **NumPy** — numerical computation
* **SciPy** — root finding and differential-equation integration
* **Plotly** — interactive visualization
* **GitHub** — version control and project hosting

---

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/sachis3009/LagrangeLab.git
```

Navigate into the project:

```bash
cd LagrangeLab
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📊 Assumptions & Limitations

LagrangeLab uses the Circular Restricted Three-Body Problem, which is an idealized model.

The model assumes:

* Circular orbits of the two primary bodies
* Point-mass gravitational bodies
* Negligible satellite mass
* No atmospheric drag
* No solar radiation pressure
* No additional gravitational bodies
* Normalized rotating-frame coordinates

Therefore, the simulation is intended primarily for **educational visualization and exploration**, rather than high-fidelity mission planning.

---

## 🎥 Demo

**Loom demonstration:**
*To be added after recording the final demonstration.*

---

## 🔮 Future Scope

Possible extensions include:

* More realistic ephemeris-based orbital models
* High-fidelity spacecraft propagation
* Station-keeping simulations
* Halo and Lissajous orbit visualization
* Jacobi constant visualization
* 3D orbital visualization
* Additional planetary systems
* Mission-design applications

---

## 👩‍💻 Project

**LagrangeLab**
An interactive exploration of Lagrange points and three-body dynamics.

