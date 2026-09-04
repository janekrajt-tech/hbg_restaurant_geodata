import pandas as pd

# Läs in den geokodade datan
df = pd.read_csv("data/processed/restaurants_geocoded.csv")


successful = df["latitude"].notna().sum()
failed = df["latitude"].isna().sum()

print("Antal restauranger totalt:", len(df))
print("Antal med koordinater:", successful)
print("Antal utan koordinater:", failed)

print("\nRestauranger utan koordinater:")
print(df[df["latitude"].isna()][["name", "address"]])