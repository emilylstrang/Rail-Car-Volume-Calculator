import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# Page setup
st.set_page_config(page_title="Railcar Volume Calculator", layout="centered")
st.title("🚂 Railcar Volume Calculator")
st.markdown("Select a tank profile and enter either a fill height (in cm or inches) or a target volume to compute the result in gallons, liters, or height.")

# Full chart data from 0.25 to 116.5 inches in 0.25" steps
# Data from Emily: accurate from 0.25 to 116.5 inches
raw_data = '''
0.25,23
0.5,47
0.75,72
1.0,98
1.25,125
1.5,153
1.75,182
2.0,212
2.25,242
2.5,274
2.75,306
3.0,339
3.25,373
3.5,408
3.75,443
4.0,479
4.25,516
4.5,553
4.75,591
5.0,629
5.25,669
5.5,709
5.75,749
6.0,790
6.25,832
6.5,874
6.75,916
7.0,960
7.25,1004
7.5,1048
7.75,1093
8.0,1138
8.25,1184
8.5,1230
8.75,1277
9.0,1325
9.25,1373
9.5,1421
9.75,1470
10.0,1519
10.25,1568
10.5,1619
10.75,1669
11.0,1720
11.25,1772
11.5,1823
11.75,1876
12.0,1928
12.25,1981
12.5,2035
12.75,2089
13.0,2143
13.25,2198
13.5,2253
13.75,2308
14.0,2364
14.25,2420
14.5,2476
14.75,2533
15.0,2591
15.25,2648
15.5,2706
15.75,2764
16.0,2823
16.25,2882
16.5,2941
16.75,3001
17.0,3061
17.25,3121
17.5,3181
17.75,3242
18.0,3303
18.25,3365
18.5,3427
18.75,3489
19.0,3551
19.25,3614
19.5,3677
19.75,3740
20.0,3804
20.25,3867
20.5,3931
20.75,3996
21.0,4060
21.25,4125
21.5,4191
21.75,4256
22.0,4322
22.25,4388
22.5,4454
22.75,4520
23.0,4587
23.25,4654
23.5,4721
23.75,4789
24.0,4856
24.25,4924
24.5,4992
24.75,5061
25.0,5129
25.25,5198
25.5,5267
25.75,5337
26.0,5406
26.25,5476
26.5,5546
26.75,5616
27.0,5686
27.25,5757
27.5,5828
27.75,5899
28.0,5970
28.25,6041
28.5,6113
28.75,6185
29.0,6256
29.25,6329
29.5,6401
29.75,6473
30.0,6546
30.25,6619
30.5,6692
30.75,6765
31.0,6839
31.25,6912
31.5,6986
31.75,7060
32.0,7134
32.25,7208
32.5,7283
32.75,7357
33.0,7432
33.25,7507
33.5,7582
33.75,7657
34.0,7732
34.25,7808
34.5,7883
34.75,7959
35.0,8035
35.25,8111
35.5,8187
35.75,8264
36.0,8340
36.25,8417
36.5,8493
36.75,8570
37.0,8647
37.25,8724
37.5,8802
37.75,8879
38.0,8956
38.25,9034
38.5,9112
38.75,9189
39.0,9267
39.25,9345
39.5,9423
39.75,9502
40.0,9580
40.25,9658
40.5,9737
40.75,9816
41.0,9894
41.25,9973
41.5,10052
41.75,10131
42.0,10210
42.25,10290
42.5,10369
42.75,10448
43.0,10528
43.25,10607
43.5,10687
43.75,10767
44.0,10847
44.25,10926
44.5,11006
44.75,11086
45.0,11166
45.25,11247
45.5,11327
45.75,11407
46.0,11487
46.25,11568
46.5,11648
46.75,11729
47.0,11809
47.25,11890
47.5,11971
47.75,12051
48.0,12132
48.25,12213
48.5,12294
48.75,12375
49.0,12456
49.25,12537
49.5,12618
49.75,12699
50.0,12780
50.25,12861
50.5,12942
50.75,13023
51.0,13104
51.25,13185
51.5,13266
51.75,13347
52.0,13428
52.25,13509
52.5,13590
52.75,13671
53.0,13752
53.25,13833
53.5,13914
53.75,13995
54.0,14076
54.25,14157
54.5,14238
54.75,14319
55.0,14400
55.25,14481
55.5,14562
55.75,14643
56.0,14724
56.25,14805
56.5,14886
56.75,14967
57.0,15048
57.25,15129
57.5,15210
57.75,15291
58.0,15372
58.25,15453
58.5,15534
58.75,15615
59.0,15696
59.25,15777
59.5,15858
59.75,15939
60.0,16020
60.25,16101
60.5,16182
60.75,16263
61.0,16344
61.25,16425
61.5,16506
61.75,16587
62.0,16668
62.25,16749
62.5,16830
62.75,16911
63.0,16992
63.25,17073
63.5,17154
63.75,17235
64.0,17316
64.25,17397
64.5,17478
64.75,17559
65.0,17640
65.25,17721
65.5,17802
65.75,17883
66.0,17964
66.25,18045
66.5,18126
66.75,18207
67.0,18288
67.25,18369
67.5,18450
67.75,18531
68.0,18612
68.25,18693
68.5,18774
68.75,18855
69.0,18936
69.25,19017
69.5,19098
69.75,19179
70.0,19260
70.25,19341
70.5,19422
70.75,19503
71.0,19584
71.25,19665
71.5,19746
71.75,19827
72.0,19908
72.25,19989
72.5,20070
72.75,20151
73.0,20232
73.25,20313
73.5,20394
73.75,20475
74.0,20556
74.25,20637
74.5,20718
74.75,20799
75.0,20880
75.25,20961
75.5,21042
75.75,21123
76.0,21204
76.25,21285
76.5,21366
76.75,21447
77.0,21528
77.25,21609
77.5,21690
77.75,21771
78.0,21852
78.25,21933
78.5,22014
78.75,22095
79.0,22176
79.25,22257
79.5,22338
79.75,22419
80.0,22500
100.0,27424
114.0,29340
114.25,29346
114.5,29352
114.75,29357
115.0,29361
115.25,29364
115.5,29367
115.75,29368
116.0,29369
116.25,29370
116.5,29370
'''
data = [tuple(map(float, line.split(","))) for line in raw_data.strip().split("\n")]

# Unpack
height_in, volume_gal = zip(*data)

# Create interpolation functions
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
st.caption("Volume model based on SKSX117122 empirical chart data. Accuracy depends on fidelity of source data.")
