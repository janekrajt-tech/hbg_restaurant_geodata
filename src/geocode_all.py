import pandas as pd
import time
import logging
import os
from geopy.geocoders import Nominatim

# Skapa loggmapp om den inte redan finns
os.makedirs("logs", exist_ok=True)

# Skapa loggfil
logging.basicConfig(
    filename="logs/geocoding.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Om geokodad data redan finns, använd den
geocoded_file = "data/processed/restaurants_geocoded.csv"
clean_file = "data/processed/restaurants_clean.csv"

if os.path.exists(geocoded_file):
    df = pd.read_csv(geocoded_file)
    print("Använder befintlig geokodad data.")
else:
    df = pd.read_csv(clean_file)
    df["latitude"] = None
    df["longitude"] = None
    print("Ingen tidigare geokodad data hittades.")

# Skapa geocoder
geolocator = Nominatim(
    user_agent="hbg_restaurant_geodata"
)

# Hitta endast restauranger som saknar koordinater
missing = df["latitude"].isna() | df["longitude"].isna()

print(f"Totalt antal restauranger: {len(df)}")
print(f"Restauranger som behöver geokodas: {missing.sum()}")

logging.info(
    "Startar geokodning. %s restauranger saknar koordinater.",
    missing.sum()
)

# Geokoda endast saknade restauranger
for i in df[missing].index:

    name = df.loc[i, "name"]
    address = f"{df.loc[i, 'address']}, Helsingborg, Sweden"

    try:
        location = geolocator.geocode(address)

        if location:
            df.loc[i, "latitude"] = location.latitude
            df.loc[i, "longitude"] = location.longitude

            logging.info(
                "Lyckades: %s - %s",
                name,
                address
            )

            print(f"{name} ✓")

        else:
            logging.warning(
                "Ingen position hittades: %s - %s",
                name,
                address
            )

            print(f"{name} - hittades inte")

    except Exception as e:

        logging.error(
            "Fel vid geokodning: %s - %s - %s",
            name,
            address,
            e
        )

        print(f"{name} - FEL: {e}")

    # Vänta mellan API-anrop
    time.sleep(1.1)

    # Spara efter varje försök
    df.to_csv(
        geocoded_file,
        index=False
    )

# Slutlig kontroll
missing_after = df["latitude"].isna().sum()

logging.info(
    "Geokodning klar. %s restauranger saknar fortfarande koordinater.",
    missing_after
)

print("\nGeokodningen är klar!")
print(f"Restauranger utan koordinater: {missing_after}")
print(f"Data sparad i: {geocoded_file}")
print("Logg sparad i: logs/geocoding.log")