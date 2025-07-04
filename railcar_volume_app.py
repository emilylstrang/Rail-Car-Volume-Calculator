
import streamlit as st
import numpy as np
from scipy.optimize import root_scalar

# Set page configuration
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")

st.title("🚂 Railcar Volume Calculator")
st.markdown("Select a tank profile and enter either a fill height (in cm) or a target volume to compute the result in gallons, liters, or height.")

# Define polynomial coefficients for each tank
# These are placeholders; replace with actual coefficients when available
tank_profiles = {
    "Tank A (SKSX117122)": [-2.0529e-6, 5.5890e-4, -0.074798, 5.6698, 102.1894, -11.6755],
    "Tank B": [0, 0, 0, 0, 100, 0],  # Example linear tank (placeholder)
    "Tank C": [1e-6, -2e-4, 0.01, 0.5, 90, 5]  # Example custom tank (placeholder)
}

selected_tank = st.selectbox("Select Tank Profile:", list(tank_profiles.keys()))
coefs = tank_profiles[selected_tank]

st.header("📥 Input Mode")
mode = st.radio("Select input type:", ["Height (cm)", "Volume (gallons)", "Volume (liters)"])

if mode == "Height (cm)":
    height_cm = st.number_input("Fill Height (cm)", min_value=0.0, max_value=100.0, step=0.1)
    height_in = height_cm / 2.54
    volume_gal = np.polyval(coefs, height_in)
    volume_liters = volume_gal * 3.78541

    st.subheader("📊 Results")
    st.write(f"**Volume in Gallons:** {volume_gal:,.2f} gal")
    st.write(f"**Volume in Liters:** {volume_liters:,.2f} L")

elif mode == "Volume (gallons)":
    target_gal = st.number_input("Target Volume (gallons)", min_value=0.0)

    def gallons_error(h):
        return np.polyval(coefs, h) - target_gal

    result = root_scalar(gallons_error, bracket=[0, 100], method='brentq')

    if result.converged:
        height_in = result.root
        height_cm = height_in * 2.54
        st.subheader("📊 Results")
        st.write(f"**Required Height:** {height_cm:.2f} cm")
    else:
        st.error("Could not calculate height for the given volume.")

elif mode == "Volume (liters)":
    target_liters = st.number_input("Target Volume (liters)", min_value=0.0)
    target_gal = target_liters / 3.78541

    def liters_error(h):
        return np.polyval(coefs, h) - target_gal

    result = root_scalar(liters_error, bracket=[0, 100], method='brentq')

    if result.converged:
        height_in = result.root
        height_cm = height_in * 2.54
        st.subheader("📊 Results")
        st.write(f"**Required Height:** {height_cm:.2f} cm")
    else:
        st.error("Could not calculate height for the given volume.")

st.markdown("---")
st.caption("Model based on selected empirical or theoretical gauge table.")
