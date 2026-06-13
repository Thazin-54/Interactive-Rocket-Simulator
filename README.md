# 🚀 The Space Academy: Interactive Atmospheric Rocket Simulator

A universally accessible, web-based computational flight dynamics tool engineered to bridge the gap between abstract aerospace physics and intuitive visual learning.

## 🌐 Live Web Application
Interact with the live, deployed physics model here: **https://interactive-rocket-simulator.streamlit.app/**

## 🎯 Project Impact & Design Intent
Aerospace engineering concepts are often locked behind intimidating, math-heavy textbooks or costly proprietary software suites. This platform serves as an open-access educational bridge:
* **For Engineering Students:** Provides a dynamic sandbox to validate numeric integration methods, track powered flight-to-ballistic transitions, and observe structural load variances (Max Q Profiles).
* **For Non-Engineers:** Strips away jargon barriers using clean interactive tooltips, real-world baseline benchmarks (e.g., matching altitudes to commercial flight limits), and preconfigured launch vehicle presets.

## 🛠️ Core Engineering Features Implemented
* **Variable Mass Depletion:** Incorporates real-time structural mass reduction over time ($\dot{m} = m_{fuel}/t_{burn}$) as propellant burns, modifying vehicle inertia dynamically.
* **Exponential Atmospheric Layering:** Models shifting aerodynamic fluid density ($\rho$) relative to altitude via the standard exponential decay equation: $\rho = \rho_0 e^{-y/8500}$.
* **Two-Dimensional Kinematics & Drag:** Tracks 2D trajectory arrays ($x, y$) by continuously breaking down thrust and aerodynamic drag components over incremental time steps ($dt = 0.2s$).
* **Live Dynamic Telemetry Replay:** Uses sequential Plotly frames to generate real-time playback animations of the flight course overlaid on top of a static pre-calculated predictive flight path.

## 🎛️ Technology Stack
* **Language:** Python 3
* **Interface & Session Architecture:** Streamlit Cloud (with memory state caching)
* **Mathematical Compute Engine:** NumPy
* **Data Visualization Graphics:** Plotly Dark Templates
