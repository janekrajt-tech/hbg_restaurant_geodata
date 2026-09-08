import pandas as pd
from src.validate_data import validate_restaurants_geocoded

def test_missing_column() -> None:
    data = pd.DataFrame({
        "name": ["Testrestaurang"],
        "address": ["Testagatan 12"],
        "latitude":[56.55],
        #"longitude" saknas med flit
})

    errors = validate_restaurants_geocoded(data)
    assert any("longitude" in error for error in errors)

def test_invalid_latitude() -> None:
    data = pd.DataFrame({
        "name": ["Testrestaurang"],
                "address": ["Testagatan 12"],
                "latitude":[200.0],
                "longitude":[35.12]
    })
    errors = validate_restaurants_geocoded(data)
    assert any("Latitude" in error for error in errors)



def test_misssing_name() -> None:
    data = pd.DataFrame({
        "name": [None],
        "address": ["Testagatan 12"],
        "latitude":[55.0],
        "longitude":[35.12]
    })
    errors = validate_restaurants_geocoded(data)
    assert any("name" in error for error in errors)