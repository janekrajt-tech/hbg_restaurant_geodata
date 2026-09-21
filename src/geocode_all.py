import pandas as pd
import time
import logging
from geopy.geocoders import Nominatim



def geocode_all(df):

    if "latitude" not in df.columns:
        df["latitude"] = None

    if "longitude" not in df.columns:
        df["longitude"] = None

    # Skapa loggfil
    logging.basicConfig(
        filename="logs/geocoding.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
        )

    missing = df["latitude"].isna() | df["longitude"].isna()
# Skapa geocoder
    geolocator = Nominatim(
        user_agent="hbg_restaurant_geodata"
)



    logging.info("Startar geokodning av %s restauranger",
                missing.sum())


# Geokoda varje adress
    for i, row in df[missing].iterrows():

        address = f"{row['address']}, Helsingborg, Sweden"

        try:
            location = geolocator.geocode(address)

            if location:
                df.loc[i, "latitude"] = location.latitude
                df.loc[i, "longitude"] = location.longitude

                logging.info(
                    "Lyckades: %s - %s",
                    row["name"],
                    address
                )

                print(f"{i + 1}/{len(df)}: {row['name']} ✓")

            else:
                logging.warning(
                    "Ingen position hittades: %s - %s",
                    row["name"],
                    address
                )

                print(
                f"{i + 1}/{len(df)}: "
                f"{row['name']} - hittades inte"
            )


        except Exception as e:
            logging.error(
                "Fel vid geokodning: %s - %s - %s",
                row["name"],
                address,
                e
            )
            print(f"{i + 1}/{len(df)}: FEL - {e}")

# Vänta mellan förfrågningarna
        time.sleep(1.1)

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
    return df 