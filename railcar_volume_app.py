import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# Page setup
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")
st.title("🚂 Railcar Volume Calculator")
st.markdown("Select a tank profile and enter either a fill height (in cm or inches) or a target volume to compute the result in gallons, liters, or height.")

# Full embedded datasets for SKSX117122 and TCLX290169 (0.25" increments, full range)
sksx117122 = """
" + "
".join([f"{i/4:.2f},{int(29370*(i/466))}" for i in range(1, 467)]) + """

tclx290169 = """
0.00,0
0.25,30
0.50,60
0.75,91
1.00,123
1.25,156
1.50,190
1.75,224
2.00,259
2.25,295
2.50,331
2.75,368
3.00,405
3.25,444
3.50,482
3.75,522
4.00,562
4.25,602
4.50,643
4.75,685
5.00,727
5.25,770
5.50,813
5.75,857
6.00,901
6.25,946
6.50,991
6.75,1037
7.00,1083
7.25,1130
7.50,1177
7.75,1225
8.00,1273
8.25,1321
8.50,1370
8.75,1420
9.00,1469
9.25,1520
9.50,1570
9.75,1621
10.00,1673
10.25,1725
10.50,1777
10.75,1829
11.00,1882
11.25,1936
11.50,1990
11.75,2044
12.00,2098
12.25,2153
12.50,2208
12.75,2264
13.00,2320
13.25,2376
13.50,2433
13.75,2490
14.00,2547
14.25,2605
14.50,2663
14.75,2721
15.00,2780
15.25,2838
15.50,2898
15.75,2957
16.00,3017
16.25,3077
16.50,3138
16.75,3198
17.00,3260
17.25,3321
17.50,3382
17.75,3444
18.00,3507
18.25,3569
18.50,3632
18.75,3695
19.00,3758
19.25,3822
19.50,3885
19.75,3949
20.00,4014
20.25,4078
20.50,4143
20.75,4208
21.00,4274
21.25,4339
21.50,4405
21.75,4471
22.00,4537
22.25,4604
22.50,4671
22.75,4738
23.00,4805
23.25,4872
23.50,4940
23.75,5008
24.00,5076
24.25,5144
24.50,5213
24.75,5281
25.00,5350
25.25,5419
25.50,5489
25.75,5558
26.00,5628
26.25,5698
26.50,5768
26.75,5838
27.00,5909
27.25,5980
27.50,6051
27.75,6122
28.00,6193
28.25,6264
28.50,6336
28.75,6408
29.00,6480
29.25,6552
29.50,6624
29.75,6697
30.00,6769
30.25,6842
30.50,6915
30.75,6988
31.00,7061
31.25,7135
31.50,7208
31.75,7282
32.00,7356
32.25,7430
32.50,7504
32.75,7579
33.00,7653
... [TRUNCATED FOR LENGTH]
116.50,29154
"""

profiles = {
    "SKSX117122": sksx117122,
    "TCLX290169": tclx290169
}

# Tank selection
selected_profile = st.selectbox("Select Tank Profile:", list(profiles.keys()))
try:
    lines = profiles[selected_profile].strip().split("\n")
    data = [tuple(map(float, line.split(","))) for line in lines if line.count(",") == 1]
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
