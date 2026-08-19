# 🌌 LagrangeLab

### Interactive Lagrange Point & Orbital Dynamics Simulator

LagrangeLab is an interactive scientific simulator for exploring the five **Lagrange points (L1–L5)** in a two-body gravitational system.

The project combines numerical physics, orbital simulation, scientific animation, and an interactive web interface to make the dynamics of Lagrange points easier to understand.

---

## 🚀 Features

* 🌍 Earth–Moon preset
* ☀️ Sun–Earth preset
* ⚙️ Custom two-body systems
* 📍 Numerical calculation of L1–L5
* 🛰️ Circular Restricted Three-Body Problem (CR3BP) simulation
* 🌀 Satellite trajectory visualization
* ✨ Animated moving primary bodies
* 📊 Interactive Plotly visualizations
* 🔬 Scientific interpretation of Lagrange point stability
* 🎬 Manim scientific animation
* 🌌 REBOUND orbital dynamics simulation

---

## 🧠 Physics & Numerical Methods

LagrangeLab uses the normalized mass ratio

[
\mu = \frac{m_2}{m_1+m_2}
]

The primary bodies are represented in normalized rotating coordinates as

[
x_1=-\mu,\qquad x_2=1-\mu
]

The collinear Lagrange points **L1, L2 and L3** are calculated numerically using `scipy.optimize.brentq`.

The triangular points are calculated as

[
L_4=\left(\frac12-\mu,\frac{\sqrt3}{2}\right)
]

[
L_5=\left(\frac12-\mu,-\frac{\sqrt3}{2}\right)
]

Satellite dynamics include gravitational, centrifugal and Coriolis terms and are integrated using `scipy.integrate.solve_ivp`.

The classical stability threshold

[
\mu \approx 0.03852
]

is used to interpret the stability of L4 and L5.

---

## 🪐 REBOUND

LagrangeLab includes a genuine orbital dynamics simulation using **REBOUND**.

The REBOUND simulation contains:

* Sun
* Earth
* Test satellite
* IAS15 high-accuracy integrator

The implementation is contained in:

`rebound_simulation.py`

REBOUND is used to demonstrate numerical N-body/orbital dynamics independently from the interactive CR3BP visualization.

---

## 🎬 Manim

A scientific animation was created using **Manim Community**.

The animation demonstrates:

* Two primary bodies
* L1–L5
* Lagrange point locations
* Satellite motion
* Scientific labels and explanation

Source:

`manim_scene.py`

Rendered animation:

`assets/LagrangeLabScene.mp4`

---

## 💻 Technology Stack

| Technology     | Purpose                                         |
| -------------- | ----------------------------------------------- |
| **Python**     | Core implementation                             |
| **Streamlit**  | Interactive web application                     |
| **Plotly**     | Interactive visualization and animation         |
| **NumPy**      | Numerical computation                           |
| **SciPy**      | Lagrange point calculations and ODE integration |
| **REBOUND**    | Orbital/N-body simulation                       |
| **Manim**      | Scientific animation                            |
| **SymPy**      | Symbolic mathematics                            |
| **Pandas**     | Data handling                                   |
| **Matplotlib** | Supporting visualization                        |

---

## ▶️ Running LagrangeLab

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📁 Project Structure

```text
LagrangeLab/
│
├── app.py
├── rebound_simulation.py
├── manim_scene.py
├── requirements.txt
├── README.md
│
└── assets/
    └── LagrangeLabScene.mp4
```

---

## 🎯 Why LagrangeLab?

Lagrange points are important regions in space where gravitational and orbital dynamics create useful equilibrium configurations.

They have applications in:

* Space telescopes
* Satellite missions
* Orbital station-keeping
* Deep-space exploration
* Mission planning

LagrangeLab turns these concepts into an interactive environment where users can change the two-body system and observe how the gravitational architecture changes.

---

## 🏆 Hackathon Submission

**Project:** LagrangeLab

**GitHub:** https://github.com/sachis3009/LagrangeLab

**Demo:** Demo: https://www.loom.com/share/2958e43c42d54d0dac4ffb59da2a17c7

---

## 👩‍💻 Built For

A scientific computing and space-dynamics hackathon project demonstrating the combination of:

**Physics + Numerical Methods + Orbital Simulation + Scientific Visualization + Interactive Computing**

---

## 📜 License

This project was created for educational and hackathon purposes.

