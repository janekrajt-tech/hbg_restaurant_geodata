from src.validate_data import validate_restaurants_geocoded 
from src.load_data import load_data
from src.geocode_all import geocode_all
from src.create_geodata import create_geodata
from src.spatial_analys import spatial_analys
from src.create_hbg_map import create_hbg_map
from src.density_map import density_map
def main():
    df = load_data()
    df = geocode_all()
    errors = validate_restaurants_geocoded(df)

    if errors:
        for error in errors:
            print(f"FEL: {error}")
    else:
        print("Valideringen lyckades!")

    gdf = create_geodata(df)
    grid = spatial_analys(gdf)
    create_hbg_map(gdf)
    density_map(grid)
    
if __name__ == "__main__":
    main()