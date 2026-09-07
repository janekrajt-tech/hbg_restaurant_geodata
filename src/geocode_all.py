import pandas as pd
import time
import logging
from geopy.geocoders import Nominatim

# Skapa loggfil
logging.basicConfig(
    filename="logs/geocoding.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Läs in restaurangdata
df = pd.read_csv("data/processed/restaurants_clean.csv")

# Skapa geocoder
geolocator = Nominatim(
    user_agent="hbg_restaurant_geodata"
)

# Listor för koordinater
latitudes = []
longitudes = []

logging.info("Startar geokodning av %s restauranger", len(df))

# Geokoda varje adress
for i, row in df.iterrows():

    address = f"{row['address']}, Helsingborg, Sweden"

    try:
        location = geolocator.geocode(address)

        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            logging.info(
                "Lyckades: %s - %s",
                row["name"],
                address
            )
            print(f"{i + 1}/{len(df)}: {row['name']} ✓")
        else:
            latitudes.append(None)
            longitudes.append(None)
            logging.warning(
                "Ingen position hittades: %s - %s",
                row["name"],
                address
            )
            print(f"{i + 1}/{len(df)}: {row['name']} - hittades inte")

    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        logging.error(
            "Fel vid geokodning: %s - %s - %s",
            row["name"],
            address,
            e
        )
        print(f"{i + 1}/{len(df)}: FEL - {e}")

    # Vänta mellan förfrågningarna
    time.sleep(1.1)

# Lägg till koordinater
df["latitude"] = latitudes
df["longitude"] = longitudes

# Spara resultatet
df.to_csv(
    "data/processed/restaurants_geocoded.csv",
    index=False
)

logging.info(
    "Geokodning klar. Resultat sparat till restaurants_geocoded.csv"
)

print("\nGeokodningen är klar!")
print("Sparad som: data/processed/restaurants_geocoded.csv")