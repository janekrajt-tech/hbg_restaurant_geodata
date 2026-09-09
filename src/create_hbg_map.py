import geopandas as gpd
import folium 



### Skapar färsta karta centrerad på Helsingborg
def create_hbg_map(gdf):
    m = folium.Map(
        location= [56.0465, 12.6945],
        zoom_start=13
    )

    for _, row in gdf.iterrows():

        folium.Marker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            popup=f"""
            <b>{row['name']}</b><br>
            {row['address']}
            """
        ).add_to(m)


    m.save(
        "data/processed/restaurants_map.html"
    )

    print("Kartan har sparats")

    print(
        "Sparad som: "
        "data/processed/restaurants_map.html"
    )

    mean_lat = gdf["latitude"].mean()
    mean_lon = gdf["longitude"].mean()

    print("Genomsnittlig latitude:", mean_lat)
    print("Genomsnittlig longitude:", mean_lon)
    return m 