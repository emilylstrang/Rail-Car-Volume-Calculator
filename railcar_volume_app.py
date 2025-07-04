import streamlit as st
import numpy as np
from scipy.optimize import root_scalar

# Set page configuration
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")

st.title("🚂 Railcar Volume Calculator")
st.markdown(
    "Select a tank profile and enter either a fill height (cm) or a target volume "
    "(gallons or liters) to compute the corresponding volume or height."
)

# Define polynomial coefficients for each tank profile
# Note: Coefficients map height (inches) to volume (gallons)
tank_profiles = {
    "Tank A (SKSX117122)": [-2.0529e-6, 5.5890e-4, -0.074798, 5.6698, 102.1894, -11.6755],
    "Tank B (Example Linear)": [0, 0, 0, 0, 100, 0],  # Placeholder linear model
    "Tank C (Custom)": [1e-6, -2e-4, 0.01, 0.5, 90, 5],  # Placeholder custom model
}

selected_tank = st.selectbox("Select Tank Profile:", list(tank_profiles.keys()))
coefs = tank_profiles[selected_tank]

st.header("📥 Input Mode")
mode = st.radio("Select input type:", ["Height (cm)", "Volume (gallons)", "Volume (liters)"])

def volume_from_height(height_in):
    """Calculate volume in gallons from height in inches using polynomial."""
    return np.polyval(coefs, height_in)

if mode == "Height (cm)":
    height_cm = st.number_input("Fill Height (cm)", min_value=0.0, max_value=254.0, step=0.1)
    height_in = height_cm / 2.54
    volume_gal = volume_from_height(height_in)
    volume_liters = volume_gal * 3.78541

    st.subheader("📊 Results")
    st.write(f"**Volume:** {volume_gal:,.2f} gallons")
    st.write(f"**Volume:** {volume_liters:,.2f} liters")

elif mode == "Volume (gallons)":
    target_gal = st.number_input("Target Volume (gallons)", min_value=0.0, step=0.1)

    def error_func(h):
        return volume_from_height(h) - target_gal

    try:
        result = root_scalar(error_func, bracket=[0, 100], method='brentq')
        if result.converged:
            height_in = result.root
            height_cm = height_in * 2.54
            st.subheader("📊 Results")
            st.write(f"**Required Fill Height:** {height_cm:.2f} cm")
        else:
            st.error("Calculation did not converge. Please check input values.")
    except ValueError:
        st.error("Target volume is out of range for this tank profile.")

elif mode == "Volume (liters)":
    target_liters = st.number_input("Target Volume (liters)", min_value=0.0, step=0.1)
    target_gal = target_liters / 3.78541

    def error_func(h):
        return volume_from_height(h) - target_gal

    try:
        result = root_scalar(error_func, bracket=[0, 100], method='brentq')
        if result.converged:
            height_in = result.root
            height_cm = height_in * 2.54
            st.subheader("📊 Results")
            st.write(f"**Required Fill Height:** {height_cm:.2f} cm")
        else:
            st.error("Calculation did not converge. Please check input values.")
    except ValueError:
        st.error("Target volume is out of range for this tank profile.")

st.markdown("---")
st.caption("Model based on selected empirical or theoretical gauge tables.")
