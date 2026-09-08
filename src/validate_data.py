from pathlib import Path
import logging
import pandas as pd

from logging_config import configure_logging

logger = logging.getLogger("validate_data")

REQUIRED_COLUMNS = {"name", "address", "latitude", "longitude"}

def load_restaurants_geocoded(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Hittar inte datafilen: {path}") from error 
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"Datafilen är tom: {path}") from error 

def validate_restaurants_geocoded(data: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        errors.append("Saknade kolumner: " + ", ".join(sorted(missing_columns)))

    if data.empty:
        errors.append("Din datafil innehåller inga rader.")

    if missing_columns:
        return errors 

    if data["name"].isna().any():
        errors.append("Kolumnen name saknar vissa namn.")

    if data["address"].isna().any():
        errors.append("Kolumnen address saknar vissa adress.")

    for column in ["latitude", "longitude"]:
        try:
            pd.to_numeric(data[column], errors="raise")
        except (ValueError, TypeError):
            errors.append(f"Kolumnen {column} måste innehålla tal.")

    if not data["latitude"].between(-90, 90).all():
        errors.append("Latitude måste ligga mellan -90 och 90.")

    if not data["longitude"].between(-180, 180).all():
            errors.append("Longitude måste ligga mellan -180 och 180.")

    return errors



def main() -> int:
    input_path = Path("data/processed/restaurants_geocoded.csv")

    try:
        restaurants = load_restaurants_geocoded(input_path)
        validation_errors = validate_restaurants_geocoded(restaurants)

        if validation_errors:
            for message in validation_errors:
                logger.error(message)
            return 1
        
        logger.info("Valideringen lyckades.")

        return 0
    
    except (FileNotFoundError, ValueError) as error:
        logger.error("Kunde inte skapa rapporten: %s", error)
        return 1
    except Exception:
        logger.exception("Ett oväntat fel stoppade programmet.")
        raise


if __name__ == "__main__":
    configure_logging()
    raise SystemExit(main())