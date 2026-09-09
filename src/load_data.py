import pandas as pd
def load_data():
    url = "https://tillstandsenheten.helsingborg.se/alktwebbforms/Restaurants"

    tables = pd.read_html(url)

    df = tables[0]

    df = df[["Namn", "Postadress", "Serveringstider"]]

    df = df.rename(columns={
    "Namn": "name",
    "Postadress": "address",
    "Serveringstider": "serving_hours"
        })

    print("\nAntal restauranger:")
    print(len(df))

    print("\nKolumner:")
    print(df.columns.tolist())

    print("\nDatatyper:")
    print(df.dtypes)

    print("\nSaknade värden:")
    print(df.isna().sum())

    print(df.head())

    df.to_csv("data/processed/restaurants_clean.csv", index=False)

    print("Bearbetad data har sparats")

    return df 