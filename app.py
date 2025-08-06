import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from modules.site_analysis import analyze_site
from modules.layout_engine import generate_layout
from modules.slope_handler import mask_by_slope

st.set_page_config(layout="wide")
st.title("TestFit-like Site Planner")

uploaded_file = st.file_uploader("Upload Parcel GeoJSON", type=["geojson"])
dem_file = st.file_uploader("Upload DEM (GeoTIFF)", type=["tif"])

if uploaded_file and dem_file:
    gdf = gpd.read_file(uploaded_file)
    slope_mask = mask_by_slope(dem_file, gdf)

    st.subheader("Original Parcel")
    m1 = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=17)
    folium.GeoJson(gdf).add_to(m1)
    st_folium(m1, height=400)

    st.subheader("Slope-Constrained Layout")
    layout = generate_layout(gdf, slope_mask)
    m2 = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=17)
    folium.GeoJson(layout).add_to(m2)
    st_folium(m2, height=400)
