import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

# -----------------------------
# PAGE
# -----------------------------

st.set_page_config(
    page_title="LagrangeLab",
    page_icon="🛰️",
    layout="wide"
)
# -----------------------------
# SPACE UI
# -----------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(80, 40, 150, 0.25), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(0, 150, 255, 0.18), transparent 30%),
        radial-gradient(circle at 50% 80%, rgba(100, 40, 180, 0.15), transparent 35%),
        #050816;
    color: #f5f7ff;
}
/* Improve text readability */

body,
.stApp {
    color: #D1D5DB;
}

p,
label,
.stCaption,
[data-testid="stCaptionContainer"] {
    color: #B8C1D1 !important;
}

h1 {
    color: #E5E7EB !important;
}

h2 {
    color: #DDE3EE !important;
}

h3 {
    color: #CBD5E1 !important;
}

.stMarkdown {
    color: #CBD5E1;
}

[data-testid="stMetricLabel"] {
    color: #AEB8C8 !important;
}

[data-testid="stMetricValue"] {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080b1c 0%,
            #050816 100%
        );
    border-right: 1px solid rgba(120, 100, 255, 0.25);
}

h1, h2, h3 {
    color: #ffffff;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(120, 100, 255, 0.5);
    background: linear-gradient(
        90deg,
        #6d4aff,
        #3b82f6
    );
    color: white;
    font-weight: 700;
    padding: 0.7rem;
}

.stButton > button:hover {
    border-color: #ffffff;
    box-shadow: 0 0 20px rgba(90, 100, 255, 0.5);
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 15px;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# HERO HEADER
# -----------------------------

st.markdown(
    """
    # 🛰️ LAGRANGELAB

    ### CR3BP • SPACE DYNAMICS SIMULATOR

    **Explore gravitational balance points and simulate satellite
    dynamics in a two-body system.**
    """
)
# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("## 🎛️ Mission Control")
st.sidebar.caption("Configure your gravitational system")

preset = st.sidebar.selectbox(
    "Choose a system",
    ["Earth-Moon", "Sun-Earth", "Custom"]
)

if preset == "Earth-Moon":
    m1 = 5.972e24
    m2 = 7.348e22
    distance_km = 384400.0

elif preset == "Sun-Earth":
    m1 = 1.989e30
    m2 = 5.972e24
    distance_km = 149597870.0

else:
    m1 = st.sidebar.number_input(
        "Body 1 mass (kg)",
        min_value=1e20,
        value=5.972e24,
        format="%.3e"
    )

    m2 = st.sidebar.number_input(
        "Body 2 mass (kg)",
        min_value=1e18,
        value=7.348e22,
        format="%.3e"
    )

    distance_km = st.sidebar.number_input(
        "Distance between bodies (km)",
        min_value=1000.0,
        value=384400.0
    )

point_choice = st.sidebar.selectbox(
    "Satellite starting point",
    ["L1", "L2", "L3", "L4", "L5"]
)

simulation_time = st.sidebar.slider(
    "Simulation time",
    1.0,
    30.0,
    10.0,
    1.0
)

run = st.sidebar.button(
    "🚀  RUN SIMULATION",
    use_container_width=True
)

# -----------------------------
# MASS RATIO
# -----------------------------

mu = m2 / (m1 + m2)

# Normalized rotating coordinate system
# Body 1 = (-mu, 0)
# Body 2 = (1-mu, 0)

x1 = -mu
x2 = 1 - mu


# -----------------------------
# EFFECTIVE FORCE EQUATION
# -----------------------------

def dOmega_dx(x):

    r1 = abs(x + mu)
    r2 = abs(x - 1 + mu)

    return (
        x
        - (1 - mu) * (x + mu) / r1**3
        - mu * (x - 1 + mu) / r2**3
    )


# -----------------------------
# L1, L2, L3
# -----------------------------

def calculate_collinear_points():

    eps = 1e-6

    L1 = brentq(
        dOmega_dx,
        x1 + eps,
        x2 - eps
    )

    L2 = brentq(
        dOmega_dx,
        x2 + eps,
        5
    )

    L3 = brentq(
        dOmega_dx,
        -5,
        x1 - eps
    )

    return L1, L2, L3


L1, L2, L3 = calculate_collinear_points()

# L4 and L5 form equilateral triangles

L4 = (
    0.5 - mu,
    np.sqrt(3) / 2
)

L5 = (
    0.5 - mu,
    -np.sqrt(3) / 2
)

points = {
    "L1": (L1, 0.0),
    "L2": (L2, 0.0),
    "L3": (L3, 0.0),
    "L4": L4,
    "L5": L5
}


# -----------------------------
# DISPLAY VALUES
# -----------------------------

st.header("🌌 Lagrange Point Map")
st.caption(
    "Visualizing the gravitational architecture of the selected two-body system."
)
cols = st.columns(5)

for i, name in enumerate(points):

    x, y = points[name]

    with cols[i]:
        st.metric(
            name,
            f"x = {x:.4f}"
        )


# -----------------------------
# VISUALIZE ALL FIVE POINTS
# -----------------------------

fig = go.Figure()


# Body 1

body1_name = "Earth" if preset == "Earth-Moon" else "Sun" if preset == "Sun-Earth" else "Body 1"

fig.add_trace(
    go.Scatter(
        x=[x1],
        y=[0],
        mode="markers+text",
        marker=dict(
    size=35,
    symbol="circle"
),
        text=[f"🌍 {body1_name}"],
        textposition="bottom center",
        name=body1_name
    )
)


# Body 2

body2_name = "Moon" if preset == "Earth-Moon" else "Earth" if preset == "Sun-Earth" else "Body 2"

fig.add_trace(
    go.Scatter(
        x=[x2],
        y=[0],
        mode="markers+text",
        marker=dict(
    size=22,
    symbol="circle"
),
        text=[f"🌙 {body2_name}"],
        textposition="bottom center",
        name=body2_name
    )
)


# Lagrange points

lx = [points[p][0] for p in points]
ly = [points[p][1] for p in points]

fig.add_trace(
    go.Scatter(
        x=lx,
        y=ly,
        mode="markers+text",
        marker=dict(size=10),
        text=list(points.keys()),
        textposition="top center",
        name="Lagrange Points"
    )
)

# Highlight selected Lagrange point

selected_x, selected_y = points[point_choice]

fig.add_trace(
    go.Scatter(
        x=[selected_x],
        y=[selected_y],
        mode="markers+text",
        marker=dict(
            size=22,
            symbol="circle-open",
            line=dict(width=4)
        ),
        text=[f"Selected: {point_choice}"],
        textposition="top center",
        name=f"Selected {point_choice}"
    )
)

fig.update_layout(
    title="Lagrange Point Map",
    xaxis_title="Normalized X",
    yaxis_title="Normalized Y",
    height=600,
    xaxis=dict(zeroline=True),
    yaxis=dict(
        zeroline=True,
        scaleanchor="x",
        scaleratio=1
    )
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# SATELLITE SIMULATION
# -----------------------------

def equations(t, state):

    x, y, vx, vy = state

    r1 = np.sqrt(
        (x + mu)**2 + y**2
    )

    r2 = np.sqrt(
        (x - 1 + mu)**2 + y**2
    )

    ax = (
        x
        - (1 - mu) * (x + mu) / r1**3
        - mu * (x - 1 + mu) / r2**3
        + 2 * vy
    )

    ay = (
        y
        - (1 - mu) * y / r1**3
        - mu * y / r2**3
        - 2 * vx
    )

    return [
        vx,
        vy,
        ax,
        ay
    ]
# -----------------------------
# ANIMATION HELPERS
# -----------------------------

def rotate_point(x, y, theta):
    """
    Convert a point from the rotating CR3BP frame
    into an inertial-looking frame for visualization.
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    xr = x * cos_t - y * sin_t
    yr = x * sin_t + y * cos_t

    return xr, yr
def create_animated_simulation(
    trajectory_x,
    trajectory_y,
    point_choice,
    preset,
    x1,
    x2,
    points,
    mu
):

    frame_count = 180

    indices = np.linspace(
        0,
        len(trajectory_x) - 1,
        frame_count
    ).astype(int)

    frames = []

    body1_name = (
        "Earth"
        if preset == "Earth-Moon"
        else "Sun"
        if preset == "Sun-Earth"
        else "Body 1"
    )

    body2_name = (
        "Moon"
        if preset == "Earth-Moon"
        else "Earth"
        if preset == "Sun-Earth"
        else "Body 2"
    )

    # ---------------------------------
    # INITIAL FIGURE
    # ---------------------------------

    fig = go.Figure()

    # Stars
    np.random.seed(42)

    stars_x = np.random.uniform(-3, 3, 180)
    stars_y = np.random.uniform(-3, 3, 180)

    fig.add_trace(
        go.Scatter(
            x=stars_x,
            y=stars_y,
            mode="markers",
            marker=dict(
                size=2,
                color="white",
                opacity=0.55
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

        # Body 1 glow
    fig.add_trace(
        go.Scatter(
            x=[x1],
            y=[0],
            mode="markers",
            marker=dict(
                size=90,
                color="rgba(255,190,50,0.12)"
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Body 1
    fig.add_trace(
        go.Scatter(
            x=[x1],
            y=[0],
            mode="markers+text",
            marker=dict(
                size=44,
                color="#FDB813",
                line=dict(
                    width=3,
                    color="#FFF4B0"
                )
            ),
            text=[body1_name],
            textposition="bottom center",
            name=body1_name
        )
    )
            # Body 2 glow
    fig.add_trace(
        go.Scatter(
            x=[x2],
            y=[0],
            mode="markers",
            marker=dict(
                size=75,
                color="rgba(100,170,255,0.16)"
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Body 2
    fig.add_trace(
        go.Scatter(
            x=[x2],
            y=[0],
            mode="markers+text",
            marker=dict(
                size=29,
                color="#BFC7D5",
                line=dict(
                    width=3,
                    color="#FFFFFF"
                )
            ),
            text=[body2_name],
            textposition="bottom center",
            name=body2_name
        )
    )
    # Lagrange points
    lx = [
        points[p][0]
        for p in points
    ]

    ly = [
        points[p][1]
        for p in points
    ]

    fig.add_trace(
        go.Scatter(
            x=lx,
            y=ly,
            mode="markers+text",
            marker=dict(
                size=9,
                color="#A78BFA"
            ),
            text=list(points.keys()),
            textposition="top center",
            name="Lagrange Points"
        )
    )

    # Selected point
    selected_x = points[point_choice][0]
    selected_y = points[point_choice][1]

    fig.add_trace(
        go.Scatter(
            x=[selected_x],
            y=[selected_y],
            mode="markers",
            marker=dict(
                size=32,
                color="rgba(167,139,250,0.25)",
                line=dict(
                    width=5,
                    color="#C4B5FD"
                )
            ),
            name=f"Selected {point_choice}"
        )
    )

    # Satellite trail
    fig.add_trace(
        go.Scatter(
            x=[trajectory_x[0]],
            y=[trajectory_y[0]],
            mode="lines",
            line=dict(
                width=3,
                color="#60A5FA"
            ),
            name="Satellite Trail"
        )
    )

    # Satellite
    fig.add_trace(
        go.Scatter(
            x=[trajectory_x[0]],
            y=[trajectory_y[0]],
            mode="markers",
            marker=dict(
                size=12,
                symbol="diamond",
                color="white",
                line=dict(
                    width=2,
                    color="#60A5FA"
                )
            ),
            name="Satellite"
        )
    )

    # ---------------------------------
    # ANIMATION
    # ---------------------------------

    for frame_number, idx in enumerate(indices):

        theta = (
            2 * np.pi * frame_number / frame_count
        )

        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # Bodies

        body1_x = x1 * cos_t
        body1_y = x1 * sin_t

        body2_x = x2 * cos_t
        body2_y = x2 * sin_t

        # Lagrange points

        current_lx = []
        current_ly = []

        for name in points:

            px, py = points[name]

            rx = px * cos_t - py * sin_t
            ry = px * sin_t + py * cos_t

            current_lx.append(rx)
            current_ly.append(ry)

        # Selected point

        sx, sy = points[point_choice]

        selected_rx = sx * cos_t - sy * sin_t
        selected_ry = sx * sin_t + sy * cos_t

        # Satellite

        sat_x = trajectory_x[idx]
        sat_y = trajectory_y[idx]

        sat_rx = sat_x * cos_t - sat_y * sin_t
        sat_ry = sat_x * sin_t + sat_y * cos_t

        # Trail

        trail_start = max(
            0,
            idx - 100
        )

        trail_indices = np.linspace(
            trail_start,
            idx,
            40
        ).astype(int)

        trail_x = []
        trail_y = []

        for trail_idx in trail_indices:

            tx = trajectory_x[trail_idx]
            ty = trajectory_y[trail_idx]

            rx = tx * cos_t - ty * sin_t
            ry = tx * sin_t + ty * cos_t

            trail_x.append(rx)
            trail_y.append(ry)

        frames.append(
            go.Frame(
                data=[

                    go.Scatter(
                        x=[body1_x],
                        y=[body1_y]
                    ),

                    go.Scatter(
                        x=[body1_x],
                        y=[body1_y]
                    ),

                    go.Scatter(
                        x=[body2_x],
                        y=[body2_y]
                    ),

                    go.Scatter(
                        x=[body2_x],
                        y=[body2_y]
                    ),

                    go.Scatter(
                        x=current_lx,
                        y=current_ly
                    ),

                    go.Scatter(
                        x=[selected_rx],
                        y=[selected_ry]
                    ),

                    go.Scatter(
                        x=trail_x,
                        y=trail_y
                    ),

                    go.Scatter(
                        x=[sat_rx],
                        y=[sat_ry]
                    )
                ],
                name=str(frame_number)
            )
        )

    fig.frames = frames

    # ---------------------------------
    # LAYOUT
    # ---------------------------------

    fig.update_layout(

        height=700,

        paper_bgcolor="#050816",
        plot_bgcolor="#050816",

        font=dict(
            color="#E5E7EB"
        ),

        xaxis=dict(
            title="Normalized X",
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title="Normalized Y",
            showgrid=False,
            zeroline=False,
            scaleanchor="x",
            scaleratio=1
        ),

        legend=dict(
            bgcolor="rgba(5,8,22,0.7)"
        ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.02,
                y=1.08,
                buttons=[
                    dict(
                        label="▶ START",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(
                                    duration=40,
                                    redraw=True
                                ),
                                transition=dict(
                                    duration=0
                                ),
                                fromcurrent=True,
                                mode="immediate"
                            )
                        ]
                    )
                ]
            )
        ],

        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20
        )
    )

    return fig
if run:
    # -------------------------
    # SIMULATION INFORMATION
    # -------------------------

    st.subheader("Simulation Information")

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Selected Point",
            point_choice
        )

    with info2:
        point_type = (
            "Collinear"
            if point_choice in ["L1", "L2", "L3"]
            else "Triangular"
        )

        st.metric(
            "Point Type",
            point_type
        )

    with info3:
        st.metric(
            "Body Separation",
            f"{distance_km:,.0f} km"
        )

    start_x, start_y = points[point_choice]
    

    # Small disturbance from the exact Lagrange point
    start_x += 0.002

    initial_state = [
        start_x,
        start_y,
        0.0,
        0.0
    ]

    times = np.linspace(
        0,
        simulation_time,
        2000
    )

    result = solve_ivp(
        equations,
        [0, simulation_time],
        initial_state,
        t_eval=times,
        rtol=1e-9,
        atol=1e-11
    )

    trajectory_x = result.y[0]
    trajectory_y = result.y[1]

   # -------------------------
# ANIMATED SPACE SIMULATION
# -------------------------

    st.header("🌌 Live Space Simulation")
    st.caption(
    "Watch the primary bodies, Lagrange points, and satellite "
    "evolve in an animated rotating system."
)
    animated_fig = create_animated_simulation(
    trajectory_x,
    trajectory_y,
    point_choice,
    preset,
    x1,
    x2,
    points,
    mu
)
    animated_fig = create_animated_simulation(
        trajectory_x,
        trajectory_y,
        point_choice,
        preset,
        x1,
        x2,
        points,
        mu
    )

    st.plotly_chart(
        animated_fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "scrollZoom": False
        }
    )
# -------------------------
# INTERPRETATION
# -------------------------

st.header("Scientific Interpretation")

if point_choice in ["L1", "L2", "L3"]:

    st.warning(
        f"{point_choice} is a collinear Lagrange point. "
        "It is dynamically unstable, so a satellite placed "
        "near it generally requires station-keeping corrections."
    )

else:

    if mu < 0.03852:

        st.success(
            f"{point_choice} is a triangular Lagrange point. "
            "For this mass ratio, small perturbations can remain "
            "bounded around the triangular point."
        )

    else:

        st.warning(
            f"{point_choice} is a triangular point, but the "
            "current mass ratio exceeds the classical stability "
            "threshold."
        )

st.info(
    "The simulation uses the Circular Restricted Three-Body "
    "Problem (CR3BP) in a rotating reference frame."
)


# -----------------------------
# SCIENCE SECTION
# -----------------------------
# -----------------------------
# SCIENCE SECTION
# -----------------------------

st.header("🧠 Understanding Lagrange Points")
st.caption(
    "The five equilibrium locations created by the interaction "
    "of gravity and orbital motion."
)

st.write(
    """
    Lagrange points are special locations in a two-body system
    where gravitational forces and the rotating reference frame
    create equilibrium configurations for a much smaller object.

    L1 lies between the two bodies.

    L2 lies beyond the smaller body.

    L3 lies beyond the larger body.

    L4 and L5 form equilateral triangles with the two primary bodies.
    """
)

st.caption(
    "Coordinates are normalized so that the distance between "
    "the two primary bodies equals 1."
)