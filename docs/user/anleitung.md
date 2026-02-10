# Detaillierte Anleitung

## Voraussetzungen

### Python-Umgebung

WorldQual Lite benötigt Python 3.8 oder höher. Installieren Sie die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

Benötigte Pakete: pandas, numpy, scipy, matplotlib, seaborn, geopandas, gdal, mysql-connector-python.

### Input-Daten

Das Modell benötigt zwei Kategorien von Input-Daten:

1. **Rasterdaten** (UNF-Binärdateien) – räumlich aufgelöste Daten auf 5-arcmin-Gitter
2. **Tabellarische Daten** – Länder- und Zellparameter aus MySQL-Datenbank oder CSV-Dateien

Details zu allen benötigten Dateien: [Input-Daten Checkliste](../technical/DATA_REQUIREMENTS.md)

---

## Schritt 1: Einzugsgebiet definieren

Bevor das Modell laufen kann, muss definiert werden, welche Rasterzellen zum Einzugsgebiet gehören. Dafür gibt es zwei Wege:

### Option A: BasinDelineation.py verwenden

Das Skript `BasinDelineation.py` identifiziert alle Rasterzellen innerhalb eines Einzugsgebiets. Es bietet zwei Methoden:

**Methode 1 – Routing-basiert:** Ausgehend von einer Auslass-Zelle (`MostDownstreamCell`) werden über die Routing-Datei (`G_OUTFLC.UNF4`) alle Oberstrom-Zellen identifiziert.

```python
# In BasinDelineation.py anpassen:
MostDownstreamCell = [82130, 82129, 82128]  # Auslass-Zell-IDs
outflowpath = "data/Europe_Input_UNF_Files/OTHER_UNF_FILES/G_OUTFLC.UNF4"
```

**Methode 2 – Shapefile-Overlay:** Ein Einzugsgebiets-Shapefile wird mit dem WaterGAP-Muttergitter (`mother_eu.shp`) verschnitten. Ergebnis: Liste der Zell-IDs mit Flächenanteil im Einzugsgebiet.

### Option B: Vorhandene Zellenliste verwenden

Falls bereits eine CSV-Datei mit Zell-IDs existiert, kann diese direkt in `Paths_and_params.py` referenziert werden:

```python
Basin_cells_list_csv_path = "data/List_of_cells_in_Moehne_basin.csv"
```

!!! info "Format der Zellenliste"
    Die CSV-Datei muss eine Spalte `Cell_ID` enthalten mit den GCRC-Nummern der Zellen im Einzugsgebiet. Optional: Spalte `Portion of Cell in Basin (%)` für Flächenanteile.

---

## Schritt 2: Konfiguration

Alle Einstellungen werden in `src/Paths_and_params.py` vorgenommen.

### Lauftyp und Szenario

```python
run_type = 'Historical'   # 'Historical' oder 'Future'
Scenario = 'SSP2'         # 'SSP1', 'SSP2', 'SSP5' (nur bei Future)
rcp = 'rcp6p0'            # 'rcp2p6', 'rcp6p0', 'rcp8p5' (nur bei Future)
GCM = 'MIROC5'            # GCM-Modell (nur bei Future)
data_source = 'Excel'     # 'Excel' (CSV-Dateien) oder 'DB' (MySQL)
```

### Zeitraum

```python
initial_year = 1990              # Startjahr
final_year_included = 2016       # Endjahr (einschließlich)
time_step = 1                    # Zeitschritt in Jahren (1 für historisch, 10 für Future)
```

### Räumliche Parameter

```python
country_id = 276          # ISO-Ländercode (276 = Deutschland)
IDScen = 27               # Szenario-ID in der Datenbank
IDReg = 1                 # Kontinent (1=EU, 2=AF, 3=AS, 4=AU, 5=NA, 6=SA)
parameter_id = 60         # Phosphor
continent_index = 0       # Index in der Kontinent-Liste (0 = Europa)
```

### Kalibrierungsparameter

```python
Lmax_calib = 6.34e-02     # Max. DP-Auslaugungsfraktion
a_calib = 900             # Beziehung Abfluss-DP-Auslaugung
b_calib = -2              # Beziehung Abfluss-DP-Auslaugung
c_calib = 1e-12           # PP mit erodiertem Sediment
sc_corr_calib = 1         # Korrekturfaktor Streusiedlungen
bg_corr_calib = 1         # Korrekturfaktor Hintergrund
Point_load_corr = 1       # Korrekturfaktor Punktquellen
```

### Dateipfade

```python
# Relative Pfade zu den Datenverzeichnissen
Surface_Runoff_folder = "data/Europe_Input_UNF_Files/G_SURFACE_RUNOFF"
Urban_Runoff_folder = "data/Europe_Input_UNF_Files/G_URBAN_RUNOFF"
Livestock_Density_folder = "data/Europe_Input_UNF_Files/G_LIVESTOCK_NR"
# ... weitere Pfade siehe Paths_and_params.py
```

---

## Schritt 3: Modell ausführen

```bash
cd src
python WorldQual_Lite_TP.py
```

Das Modell durchläuft für jedes Jahr im definierten Zeitraum folgende Schritte:

1. **UNF-Daten laden** – Oberflächenabfluss, urbaner Abfluss, Viehdichte, Korrekturfaktoren, P-Raten, Ackerflächen
2. **Länder-/Zellparameter holen** – Bevölkerung, Kläranlagen-Anschlussraten, Emissionsfaktoren (aus DB oder CSV)
3. **8 Frachtkomponenten berechnen** – für jede Zelle und jeden Monat
4. **Erosions- und Retentionsfaktoren anwenden** – Fink-Erosionsmodell, Vollenweider-Retention
5. **Aggregieren** – Summierung auf Einzugsgebietsebene
6. **Output** – Monatliche/jährliche Frachten als CSV, Stacked-Bar-Plot

### Output

Das Modell erzeugt:

- **CSV-Datei** mit monatlichen und jährlichen TP-Frachten, aufgeteilt nach den 8 Quellen
- **Stacked-Bar-Plot** der jährlichen Frachten
- **RMSE und R²** gegen Messdaten (falls vorhanden)

---

## Schritt 4: Validierung

Falls Messdaten verfügbar sind, berechnet das Modell automatisch:

- **RMSE** (Root Mean Square Error) zwischen simulierten und gemessenen Jahresfrachten
- **R²** (Bestimmtheitsmaß)

Die Messdaten werden als Excel-Datei erwartet. Pfad konfigurierbar im Hauptskript.

---

## Fehlerbehebung

### MySQL-Verbindung schlägt fehl

Wenn `data_source = 'DB'` und die Datenbank nicht erreichbar ist:

1. Auf `data_source = 'Excel'` umstellen
2. Vorab exportierte CSV-Dateien in `data/Europe_Cell_Input_Files/` bereitstellen
3. Länderdaten als separate CSVs bereitstellen (siehe [Datenquellen](../technical/DATA_SOURCES.md))

### UNF-Dateien nicht gefunden

Pfade in `Paths_and_params.py` prüfen. Alle UNF-Pfade sind relativ zum Arbeitsverzeichnis. Stellen Sie sicher, dass das `data/`-Verzeichnis korrekt verlinkt oder befüllt ist.

### Basin-Zellenliste fehlt

Entweder `BasinDelineation.py` ausführen (benötigt G_OUTFLC.UNF4 und ggf. Shapefile) oder eine eigene CSV mit Zell-IDs erstellen.
