import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# Page config
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")

st.title("🚂 Railcar Volume Calculator")
st.markdown(
    "Enter a fill height (cm) or target volume (gallons or liters) "
    "to get the corresponding volume or height based on the empirical tank chart."
)

# Tank chart data (height in inches vs volume in gallons)
height_in = np.array([
    0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50,
    2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00,
    5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50,
    7.75, 8.00, 8.25, 8.50, 8.75
])
volume_gal = np.array([
    23, 47, 72, 98, 125, 153, 182, 212, 242, 274,
    306, 339, 373, 408, 443, 479, 516, 553, 591, 629,
    669, 709, 749, 790, 832, 874, 916, 960, 1004, 1048,
    1093, 1138, 1184, 1230, 1277
])

# Interpolation functions
volume_from_height = interp1d(height_in, volume_gal, kind='cubic', fill_value="extrapolate")
height_from_volume = interp1d(volume_gal, height_in, kind='cubic', fill_value="extrapolate")

st.header("📥 Input Mode")
mode = st.radio("Select input type:", ["Height (cm)", "Volume (gallons)", "Volume (liters)"])

if mode == "Height (cm)":
    height_cm = st.number_input("Fill Height (cm)", min_value=0.0, max_value=22.2, step=0.1)
    height_in_val = height_cm / 2.54
    volume = volume_from_height(height_in_val)
    volume_liters = volume * 3.78541

    st.subheader("📊 Results")
    st.write(f"**Volume:** {volume:.2f} gallons")
    st.write(f"**Volume:** {volume_liters:.2f} liters")

elif mode == "Volume (gallons)":
    target_gal = st.number_input("Target Volume (gallons)", min_value=23.0, max_value=1277.0, step=1.0)
    height_in_val = height_from_volume(target_gal)
    height_cm = height_in_val * 2.54

    st.subheader("📊 Results")
    st.write(f"**Required Fill Height:** {height_cm:.2f} cm")

elif mode == "Volume (liters)":
    target_liters = st.number_input("Target Volume (liters)", min_value=87.1, max_value=4834.7, step=1.0)
    target_gal = target_liters / 3.78541
    height_in_val = height_from_volume(target_gal)
    height_cm = height_in_val * 2.54

    st.subheader("📊 Results")
    st.write(f"**Required Fill Height:** {height_cm:.2f} cm")

st.markdown("---")
st.caption("Based on provided empirical tank gauge chart data.")
