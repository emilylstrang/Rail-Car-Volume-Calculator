import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# Page setup
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")
st.title("🚂 Railcar Volume Calculator")
st.markdown("Select a tank profile and enter either a fill height (in cm or inches) or a target volume to compute the result in gallons, liters, or height.")

# Tank profiles (full datasets with 0.25" increments)
with open("data_sksx117122.csv") as f:
    sksx117122 = f.read()

with open("data_tclx290169.csv") as f:
    tclx290169 = f.read()

profiles = {
    "SKSX117122": sksx117122,
    "TCLX290169": tclx290169
}

# Tank selection
selected_profile = st.selectbox("Select Tank Profile:", list(profiles.keys()))
try:
    data = [tuple(map(float, line.split(","))) for line in profiles[selected_profile].strip().split("\n")]
except Exception as e:
    st.error("❌ Failed to parse tank data. Check that each line has two numbers separated by a comma.")
    st.stop()

height_in, volume_gal = zip(*data)

# Interpolation
volume_interp = interp1d(height_in, volume_gal, kind='linear', fill_value="extrapolate")
height_interp = interp1d(volume_gal, height_in, kind='linear', fill_value="extrapolate")

# Input Mode
st.header("📥 Input Mode")
mode = st.radio("Select input type:", ["Height (cm)", "Height (inches)", "Volume (gallons)", "Volume (liters)"])

max_height_cm = float(height_in[-1] * 2.54)
max_height_in = float(height_in[-1])
max_volume = float(volume_gal[-1])

if mode == "Height (cm)":
    fill_height_cm = st.number_input("Enter fill height (cm):", min_value=0.0, max_value=max_height_cm, step=0.01)
    fill_height_in = fill_height_cm / 2.54
    volume = float(volume_interp(fill_height_in))
    st.subheader("📊 Results")
    st.write(f"**Volume in Gallons:** {volume:,.2f} gal")
    st.write(f"**Volume in Liters:** {volume * 3.78541:,.2f} L")

elif mode == "Height (inches)":
    fill_height_in = st.number_input("Enter fill height (inches):", min_value=0.0, max_value=max_height_in, step=0.01)
    volume = float(volume_interp(fill_height_in))
    st.subheader("📊 Results")
    st.write(f"**Volume in Gallons:** {volume:,.2f} gal")
    st.write(f"**Volume in Liters:** {volume * 3.78541:,.2f} L")

elif mode == "Volume (gallons)":
    target_volume = st.number_input("Enter target volume (gallons):", min_value=0.0, max_value=max_volume, step=1.0)
    height_in_result = float(height_interp(target_volume))
    st.subheader("📊 Results")
    st.write(f"**Required Height:** {height_in_result:.2f} in / {height_in_result * 2.54:.2f} cm")

elif mode == "Volume (liters)":
    target_liters = st.number_input("Enter target volume (liters):", min_value=0.0, max_value=max_volume * 3.78541, step=1.0)
    target_volume_gal = target_liters / 3.78541
    height_in_result = float(height_interp(target_volume_gal))
    st.subheader("📊 Results")
    st.write(f"**Required Height:** {height_in_result:.2f} in / {height_in_result * 2.54:.2f} cm")

st.markdown("---")
st.caption(f"Volume model based on {selected_profile} empirical chart data. Accuracy depends on fidelity of source data.")
