# Geografisk analys av restauranger i Helsingborg

# Introduktion
Projektet hämtar data från Helsingborgs stad registret med alla restauranger i Helsingborg och skapar en interaktiv karta med alla restauranger och deras namn och adresser. Projektets syfte är att undersöka geografiska mönster, eventuell koncentration och skillnader mellan olika områden. För att genmföra projektet använder jag mig av teknikerna såsom:
- Python
- Geokodning av adresser med hjälp av Nominatim
- GeoPandas
- Folium 
- Geopy/Nominatim
- Shapely
- Spatial analys

# Hur körs projektet?
1. Ladda ner projektet
2. pip install -r requirements.txt
3. Aktivera venv.
4. Köra:  python main.py
5. Köra testerna:  python -m pytest

# Datakällan 
https://tillstandsenheten.helsingborg.se/alktwebbforms/Restaurants?Restaurangnamn=&Owner=&OrgNo=&Address=&District=&Restaurangnummer=&Gardsforsaljning=false 

# Genomförande

Projektet är uppbyggt som ett dataflöde där restaurangdata hämtas, bearbetas och analyseras geografiskt.

### 1. Hämtning av data

Restaurangdata hämtas från Helsingborgs stads restaurangregister med hjälp av Pandas. De relevanta kolumnerna är restaurangens namn, adress och serveringstider.

### 2. Geokodning

Eftersom restaurangregistret innehåller adresser men inte geografiska koordinater används Nominatim för att geokoda adresserna. Adresserna omvandlas till latitude och longitude som sedan kan användas för geografisk analys.

### 3. Validering

Efter geokodningen valideras datan för att kontrollera att nödvändiga kolumner finns och att koordinaterna innehåller giltiga värden. Projektet innehåller även automatiserade tester för valideringen.

### 4. Skapande av geografisk data

Med GeoPandas omvandlas restaurangdatan till en GeoDataFrame. Varje restaurang representeras som en geografisk punkt baserat på dess latitude och longitude. Datan sparas även som en GeoJSON-fil.

### 5. Spatial analys

För att undersöka hur restaurangerna är geografiskt fördelade delas området in i rutor på 500 × 500 meter. Med hjälp av en spatial join räknas antalet restauranger i varje ruta. Detta används för att identifiera områden där restaurangerna är mer eller mindre koncentrerade.

### 6 Tekniska val

## Varför EPSG:3006?
EPSG:3006 används eftersom koordinaterna då anges i meter. Det gör det möjligt att skapa ett rutnät där varje ruta är 500 × 500 meter.
Restaurangernas ursprungliga koordinater anges i EPSG:4326, där positionerna representeras med latitud och longitud. För den spatiala analysen används istället EPSG:3006 eftersom koordinaterna då anges i meter. Det gör det möjligt att skapa ett rutnät med en bestämd fysisk storlek, exempelvis 500 × 500 meter.

## Varför 500 × 500 meter?
Rutstorleken valdes för att kunna jämföra restaurangtätheten mellan olika områden. Mindre rutor hade gett mer detaljer medan större rutor hade gett en mer övergripande analys.

## Varför Nominatim?
Nominatim användes för att omvandla restaurangernas adresser till geografiska koordinater som sedan kunde användas i den spatiala analysen.

### 7. Visualisering

Folium används för att skapa interaktiva kartor. Den första kartan visar restaurangernas geografiska positioner och information om restaurangerna. En andra karta visar restaurangtätheten i de olika rutorna med hjälp av färgskalor.

Resultaten sparas som HTML-filer och kan öppnas direkt i en webbläsare.
