import pandas as pd

file_path = "data/processed/restaurants_geocoded.csv"
df = pd.read_csv(file_path)

manual_coordinates = {
    "Chili Mexican Grill": (56.0444, 12.6929),
    "Grekiska Kolgrillen": (56.0921, 12.7568),
    "Grytan Restaurang - Rya golfklubb": (55.9760, 12.7565),
    "Icha Mochi": (56.0558, 12.6967),
    "Omakaze Sushi": (55.9663, 12.7822),
    "Parapeten": (56.0446, 12.6863),
    "Pålsjöpaviljongen": (56.069861, 12.685528),
    "Restaurangskolan": (56.0446, 12.6863),
    "Rydebäcks Pizzeria": (55.9663, 12.7750),
    "Sillen & Makrillen": (56.0557, 12.6827),
    "Small Britain": (56.0904, 12.8298),
    "The Tivoli": (56.04534, 12.69066),
    "Vasatorp Golfrestaurang": (56.0580, 12.7885),
    "Villa Thalassa": (56.0709, 12.6744),
    "M/S Tilda": (56.04442, 12.69293),
    "På Piren": (55.99517, 12.74547),
}

# Lägg in koordinaterna
for name, (lat, lon) in manual_coordinates.items():
    mask = df["name"] == name

    df.loc[mask, "latitude"] = lat
    df.loc[mask, "longitude"] = lon

# Spara filen
df.to_csv(file_path, index=False)

print("Manuella koordinater har lagts till!")

# Kontrollera hur många som fortfarande saknas
missing = df["latitude"].isna().sum()

print("Antal restauranger utan koordinater:", missing)

print("\nFortfarande saknade:")
print(
    df[df["latitude"].isna()][["name", "address"]]
)