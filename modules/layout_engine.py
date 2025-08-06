import geopandas as gpd
from shapely.geometry import box, Point
import numpy as np

def generate_layout(parcel_gdf, slope_mask):
    bounds = parcel_gdf.total_bounds
    xmin, ymin, xmax, ymax = bounds
    spacing = 18  # meters (approx 60ft)

    print("Parcel bounds:", bounds)
    print("Slope mask geometries:", len(slope_mask))

    units = []
    for x in np.arange(xmin, xmax, spacing):
        for y in np.arange(ymin, ymax, spacing):
            unit = box(x, y, x + spacing * 0.8, y + spacing * 0.6)
            unit_center = Point(unit.centroid)

            # Check if inside parcel and in slope mask
            if parcel_gdf.contains(unit_center).any() and slope_mask.contains(unit_center).any():
                units.append(unit)

    print(f"Generated {len(units)} units")
    return gpd.GeoDataFrame(geometry=units, crs=parcel_gdf.crs)
