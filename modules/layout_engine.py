import geopandas as gpd
from shapely.geometry import box
import numpy as np

def generate_layout(parcel_gdf, slope_mask):
    bounds = parcel_gdf.total_bounds
    units = []
    spacing = 18  # meters (about 60 ft)

    xmin, ymin, xmax, ymax = bounds
    for x in np.arange(xmin, xmax, spacing):
        for y in np.arange(ymin, ymax, spacing):
            unit = box(x, y, x + spacing * 0.8, y + spacing * 0.6)
            if slope_mask.contains(unit.centroid).any():
                units.append(unit)
    return gpd.GeoDataFrame(geometry=units, crs=parcel_gdf.crs)
