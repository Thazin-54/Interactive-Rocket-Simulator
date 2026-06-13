import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- WEBSITE PAGE CONFIGURATION ---
st.set_page_config(page_title="AeroSim Space Academy", layout="wide")

# --- WEBSITE HEADER & MISSION STATEMENT ---
st.title("🚀 The Space Academy: Interactive Rocket Simulator")
st.markdown("""
### Welcome to Rocket Science — Made Simple!
You don't need an engineering degree to understand how rockets go to space. 
Use the **Control Center on the left** to design your rocket. Watch the charts update instantly, 
and hit the **Launch Engine** button to see your flight path in action!
""")

# --- REAL ROCKET PRESETS ---
PRESETS = {
    "Custom Rocket (Your Design)": [500, 1000, 0.5, 0.3, 40000, 25, 80],
    "Light Weather Rocket (Sounding Rocket)": [150, 200, 0.2, 0.25, 8000, 12, 85],
    "Heavy Orbital Booster (Falcon 9 Style)": [2000, 3000, 1.8, 0.4, 95000, 45, 75]
}

st.sidebar.header("🎯 Step 1: Choose a Rocket Setup")
preset_choice = st.sidebar.selectbox("Load a Real-World Style Preset:", list(PRESETS.keys()))

# --- INITIALIZE SESSION STATE FOR SLIDERS ---
vals = PRESETS[preset_choice]
keys = ["dry_mass", "fuel_mass", "diameter", "cd", "thrust", "burn_time", "launch_angle"]

# If the user switches presets, force the state to update instantly
if "last_preset" not in st.session_state or st.session_state["last_preset"] != preset_choice:
    st.session_state["last_preset"] = preset_choice
    for k, v in zip(keys, vals):
        st.session_state[k] = v

# Reset Button Configuration
if st.sidebar.button("🔄 Reset Rocket to Default", use_container_width=True):
    for k, v in zip(keys, PRESETS["Custom Rocket (Your Design)"]):
        st.session_state[k] = v
    st.rerun()

st.sidebar.markdown("---")

# --- CONTROL PANEL SLIDERS ---
st.sidebar.header("🛠️ Step 2: Tweak the Designs")

dry_mass = st.sidebar.slider("Rocket Structural Weight (kg)", 100, 2000, key="dry_mass", step=50)
st.sidebar.caption("The empty metal shell, computers, and payload. **Heavier rockets climb slower.**")

fuel_mass = st.sidebar.slider("Fuel Weight (Propellant) (kg)", 100, 3000, key="fuel_mass", step=50)
st.sidebar.caption("More fuel means the engine fires longer, but makes the rocket heavy at liftoff.")

diameter = st.sidebar.slider("Rocket Width / Diameter (meters)", 0.2, 2.0, key="diameter", step=0.1)
st.sidebar.caption("Wider rockets smash into more air molecules, creating **higher air resistance (Drag)**.")

cd = st.sidebar.slider("Aerodynamic Shape Coefficient (Cd)", 0.1, 1.0, key="cd", step=0.05)
st.sidebar.caption("A sharp needle nose cone is around 0.15 (sleek). A flat box is 1.0 (blocks air).")

st.sidebar.header("🔥 Step 3: Propulsion & Steering")

thrust = st.sidebar.slider("Engine Power (Thrust in Newtons)", 5000, 100000, key="thrust", step=1000)
st.sidebar.caption("The raw pushing force of the fire. **Must be strong enough to lift the weight!**")

burn_time = st.sidebar.slider("Engine Firing Time (seconds)", 5, 60, key="burn_time", step=1)
st.sidebar.caption("How many seconds the engine burns before running completely empty out of fuel.")

launch_angle = st.sidebar.slider("Launch Angle (Degrees)", 45, 90, key="launch_angle", step=1)
st.sidebar.caption("90° goes straight up. 75° tilts the rocket slightly to travel across the land.")

# --- THE SIMULATION LAUNCH ENGINE ---
g = 9.81
rho_0 = 1.225  
radius = diameter / 2
area = np.pi * (radius ** 2)  
burn_rate = fuel_mass / burn_time

dt = 0.2 
time_steps = np.arange(0, 200, dt)

altitudes, x_positions, velocities, dynamic_pressures, times = [], [], [], [], []
x, y = 0.0, 0.0
v_x, v_y = 0.0, 0.0

for t in time_steps:
    if t <= burn_time:
        current_mass = (dry_mass + fuel_mass) - (burn_rate * t)
        current_thrust = thrust
    else:
        current_mass = dry_mass
        current_thrust = 0.0
        
    rho = rho_0 * np.exp(-y / 8500.0)
    v = np.sqrt(v_x**2 + v_y**2)
    flight_angle = np.arctan2(v_y, v_x) if v > 0 else np.radians(launch_angle)
    
    drag = 0.5 * rho * (v**2) * cd * area
    q = 0.5 * rho * (v**2)  
    
    drag_x = drag * np.cos(flight_angle)
    drag_y = drag * np.sin(flight_angle)
    
    thrust_x = current_thrust * np.cos(np.radians(launch_angle)) if t <= burn_time else 0
    thrust_y = current_thrust * np.sin(np.radians(launch_angle)) if t <= burn_time else 0
    
    accel_x = (thrust_x - drag_x) / current_mass
    accel_y = ((thrust_y - drag_y) / current_mass) - g
    
    v_x += accel_x * dt
    v_y += accel_y * dt
    x += v_x * dt
    y += v_y * dt
    
    if y < 0 and t > burn_time:
        y = 0
        break
        
    altitudes.append(y)
    x_positions.append(x)
    velocities.append(v)
    dynamic_pressures.append(q)
    times.append(t)

# --- JARGON DICTIONARY FOR NON-ENGINEERS ---
with st.expander("💡 New to Space Science? Click here to learn what these terms mean in simple English"):
    st.markdown("""
    * **Apogee (Max Altitude):** This is the highest point your rocket reaches before its upward energy runs out, causing it to stall and start falling back down.
    * **V-Max (Top Speed):** The fastest speed your rocket moves. This happens exactly when the engine shuts off because there's no more fire pushing it forward!
    * **Max Q (Maximum Structural Stress):** As a rocket accelerates through the sky, it hits air molecules. The faster it goes, the harder the air pushes back. Eventually, it reaches a peak crunch point called **Max Q**. After this point, the air gets so thin that the shaking stops.
    """)

# --- TELEMETRY SUMMARY REPORT WITH REAL WORLD COMPARISONS ---
st.subheader("📊 Flight Results & Real-World Comparisons")

max_alt_km = max(altitudes) / 1000
max_vel = max(velocities)
max_q_pa = max(dynamic_pressures)

# Real world baseline comparisons logic
if max_alt_km < 10:
    alt_comparison = "✈️ Below commercial airplane cruise altitude (10 km)."
elif max_alt_km < 50:
    alt_comparison = "🎈 Inside the Stratosphere! Higher than weather balloons."
else:
    alt_comparison = "🌌 Edge of Space! Approaching Mesosphere limits."

if max_vel < 343:
    vel_comparison = "🚗 Slower than the speed of sound (Subsonic)."
else:
    vel_comparison = "⚡ Breaking the Sound Barrier! Faster than a jet fighter plane."

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Highest Altitude Reached", f"{round(max_alt_km, 2)} km")
    st.info(alt_comparison)
with col2:
    st.metric("Top Speed Achieved", f"{round(max_vel, 1)} m/s")
    st.info(vel_comparison)
with col3:
    st.metric("Peak Structural Stress (Max Q)", f"{round(max_q_pa, 0)} Pascals")
    st.info(f"💨 Peak wind force hit: {round(max_q_pa / 100, 1)} kg per sq. meter.")

st.markdown("---")

# --- ANIMATION SYSTEM ---
step = max(1, len(times) // 40)
anim_x = x_positions[::step]
anim_y = altitudes[::step]

fig_anim = go.Figure(
    data=[
        go.Scatter(x=x_positions, y=altitudes, mode="lines", name="Predicted Course", line=dict(color="rgba(255,255,255,0.2)", width=2, dash="dash")),
        go.Scatter(x=[anim_x[0]], y=[anim_y[0]], mode="lines+markers", name="Rocket Position", line=dict(color="yellow", width=4), marker=dict(size=10))
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, max(x_positions) * 1.1], title="Distance Traveled Across Ground (meters)"),
        yaxis=dict(range=[0, max(altitudes) * 1.1], title="Height in the Sky (meters)"),
        title="🎬 Live Mission Trajectory Replay",
        template="plotly_dark",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="🔺 Ignition & Launch!", method="animate", args=[None, {"frame": {"duration": 60, "redraw": False}, "fromcurrent": True}])]
        )]
    ),
    frames=[go.Frame(data=[
        go.Scatter(x=x_positions, y=altitudes), 
        go.Scatter(x=anim_x[:i], y=anim_y[:i], mode="lines+markers", line=dict(color="yellow", width=4), marker=dict(size=10)) 
    ]) for i in range(1, len(anim_x)+1)]
)

st.plotly_chart(fig_anim, use_container_width=True)

# --- SCIENTIFIC DATA TABS FOR ENGINEERING STUDENTS ---
st.subheader("📉 Technical Engineering Visualizations")
tab1, tab2 = st.tabs(["Velocity Analysis", "Aerodynamic Pressure Data"])

with tab1:
    fig_v = go.Figure(go.Scatter(x=times, y=velocities, line=dict(color='cyan', width=2.5)))
    fig_v.update_layout(title="Velocity Profile (Engine Burn vs Ballistic Coasting)", template="plotly_dark", xaxis_title="Time (seconds)", yaxis_title="Velocity (m/s)")
    st.plotly_chart(fig_v, use_container_width=True)
    st.caption("Notice how velocity accelerates until your chosen engine burn time finishes, then drops due to gravity and air friction.")

with tab2:
    fig_q = go.Figure(go.Scatter(x=times, y=dynamic_pressures, line=dict(color='red', width=2.5)))
    fig_q.update_layout(title="Dynamic Fluid Pressure (Q Curve)", template="plotly_dark", xaxis_title="Time (seconds)", yaxis_title="Pressure (Pa)")
    st.plotly_chart(fig_q, use_container_width=True)
    st.caption("This curve shows structural load. It peaks where high velocity meets thick atmospheric density layers.")