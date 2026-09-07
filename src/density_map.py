import geopandas as gpd
import folium

# Läs in rutnätet med restaurangantal
grid = gpd.read_file(
    "data/processed/restaurant_density.geojson"
)

# Skapa ett unikt ID för varje ruta
grid["cell_id"] = range(len(grid))

# Folium använder latitud/longitud
grid = grid.to_crs("EPSG:4326")

# Skapa karta över Helsingborg
m = folium.Map(
    location=[56.0465, 12.6945],
    zoom_start=12
)

# Lägg till rutorna på kartan
folium.Choropleth(
    geo_data=grid,
    data=grid,
    columns=["cell_id", "restaurant_count"],
    key_on="feature.properties.cell_id",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Antal restauranger"
).add_to(m)

# Spara kartan
m.save(
    "data/processed/restaurant_density_map.html"
)

print("Täthetskartan har skapats!")
print(
    "Sparad som: "
    "data/processed/restaurant_density_map.html"
)