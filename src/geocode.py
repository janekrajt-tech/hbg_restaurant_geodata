import pandas as pd
from geopy.geocoders import Nominatim

df = pd.read_csv("data/processed/restaurants_clean.csv")


geolocator = Nominatim(user_agent="hbg_restaurant_geodata")

address = df.loc[0, "address"]

location = geolocator.geocode(
    f"{address}, Helsingborg, Sweden"
)

print("Restaurang:", df.loc[0, "name"])
print("Adress:", address)

if location:
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
else:
    print("Ingen position hittades.")