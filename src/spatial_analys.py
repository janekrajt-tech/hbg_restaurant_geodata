import geopandas as gpd
import numpy as np
from shapely.geometry import box

gdf = gpd.read_file(
    "data/processed/restaurants.geojson"
)

gdf = gdf.to_crs("EPSG:3006")

print("Koordinatsystem:", gdf.crs)

minx, miny, maxx, maxy = gdf.total_bounds

# Storlek på varje ruta i meter
cell_size = 500

# Skapa koordinater för rutnätet
x_coords = np.arange(minx, maxx + cell_size, cell_size)
y_coords = np.arange(miny, maxy + cell_size, cell_size)

# Skapa polygoner för rutorna
grid_cells = []

for x in x_coords[:-1]:
    for y in y_coords[:-1]:
        grid_cells.append(
            box(
                x,
                y,
                x + cell_size,
                y + cell_size
            )
        )

# Skapa GeoDataFrame av rutnätet
grid = gpd.GeoDataFrame(
    {"geometry": grid_cells},
    crs=gdf.crs
)

print("Antal rutor:", len(grid))

# Spatial join
joined = gpd.sjoin(
    gdf,
    grid,
    predicate="within"
)

print("\nSpatial join klar!")
print(joined.head())

# Räkna antal restauranger per ruta
restaurant_counts = (
    joined.groupby("index_right")
    .size()
    .reset_index(name="restaurant_count")
)

# Lägg tillbaka antalet på rutnätet
grid = grid.join(
    restaurant_counts.set_index("index_right")
)

# Rutor utan restauranger får värdet 0
grid["restaurant_count"] = (
    grid["restaurant_count"]
    .fillna(0)
    .astype(int)
)

print("\nRestauranger per ruta:")
print(
    grid["restaurant_count"].describe()
)
# Spara rutnätet med restaurangantal
grid.to_file(
    "data/processed/restaurant_density.geojson",
    driver="GeoJSON"
)

print("\nTäthetsdata har sparats!")