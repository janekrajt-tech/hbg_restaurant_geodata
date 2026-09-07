import pandas as pd 
import geopandas as gpd

df = pd.read_csv("data/processed/restaurants_geocoded.csv")

df = df.dropna(
    subset=["latitude", "longitude"]
)

geometry = gpd.points_from_xy(
    df["longitude"],
    df["latitude"]
)

gdf = gpd.GeoDataFrame(
    df,
    geometry=geometry,
    crs="EPSG:4326"
)

print("Antal restauranger:", len(gdf))

print("\nFörsta raderna:")
print(gdf.head())

print("\nKoordinatsystem:")
print(gdf.crs)

gdf.to_file(
    "data/processed/restaurants.geojson",
    driver="GeoJSON"
)

print("\nGeoJSON har sparats")