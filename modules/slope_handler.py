import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import shapes
from shapely.geometry import shape

def mask_by_slope(dem_file, parcel_gdf, max_slope_deg=15):
    with rasterio.open(dem_file) as src:
        elevation = src.read(1)
        transform = src.transform

        gy, gx = np.gradient(elevation)
        slope = np.degrees(np.arctan(np.sqrt(gx**2 + gy**2)))

        slope_mask = slope <= max_slope_deg
        mask_shapes = shapes(slope_mask.astype(np.uint8), transform=transform)
        polygons = [shape(geom) for geom, val in mask_shapes if val == 1]

        return gpd.GeoSeries(polygons, crs=src.crs).to_crs(parcel_gdf.crs)
