# Projektstruktur

```
WorldQual-lite/
├── docs/                          # MkDocs-Dokumentation
│   ├── index.md                   # Startseite
│   ├── user/                      # Benutzer-Dokumentation
│   │   ├── anleitung.md
│   │   ├── schnellreferenz.md
│   │   └── projektstruktur.md
│   └── technical/                 # Entwickler-Dokumentation
│       ├── ARCHITECTURE.md
│       ├── API.md
│       ├── DATA_SOURCES.md
│       └── DATA_REQUIREMENTS.md
├── src/                           # Python-Quellcode
│   ├── WorldQual_Lite_TP.py       # Hauptmodul
│   ├── Paths_and_params.py        # Konfiguration
│   ├── InputDataFetchFunctions.py # Datenbankzugriff
│   ├── BinaryFileHandler.py       # UNF-Datei-Handler
│   └── BasinDelineation.py        # Einzugsgebiets-Definition
├── data/                          # Input-Daten (nicht in Git)
│   ├── Europe_Input_UNF_Files/    # Historische UNF-Rasterdaten
│   │   ├── G_SURFACE_RUNOFF/
│   │   ├── G_URBAN_RUNOFF/
│   │   ├── G_LIVESTOCK_NR/
│   │   ├── G_CORR_FACT_RTF/
│   │   ├── P_RATE_TON_KM2/
│   │   ├── CROPLAND_CORR_KM2/
│   │   └── OTHER_UNF_FILES/
│   ├── Future_UNF_files/           # Zukunfts-UNF-Daten
│   │   ├── Hydrology/{cont}/{rcp}_{GCM}/
│   │   ├── CROPLAND_AREA_KM2/{SSP}/{cont}/
│   │   ├── LIVESTOCK_NR/{SSP}/{cont}/
│   │   ├── P_RATE_TON_KM2/{SSP}/{cont}/
│   │   └── correction_factors/{rcp}_{SSP}/{cont}/{GCM}/
│   ├── Europe_Cell_Input_Files/    # Zell-Input CSVs
│   │   ├── europe_cell_input_1990.csv ... 2016.csv
│   │   └── SSP1/ SSP2/ SSP5/
│   └── WG_mothers/                 # WaterGAP-Muttergitter (Shapefiles)
├── mkdocs.yml                     # MkDocs-Konfiguration
├── requirements.txt               # Python-Abhängigkeiten
├── .gitignore
└── README.md
```

## Verzeichnisse im Detail

### `src/` – Python-Quellcode

| Datei | Zeilen | Funktion |
|-------|--------|----------|
| `WorldQual_Lite_TP.py` | ~850 | Hauptmodul: Berechnet alle 8 TP-Frachtkomponenten, Erosion, Retention, Validierung |
| `Paths_and_params.py` | ~90 | Konfiguration: Pfade, Szenarien, Kalibrierungsparameter |
| `InputDataFetchFunctions.py` | ~340 | Datenzugriff: MySQL-Abfragen für Länder- und Zellparameter |
| `BinaryFileHandler.py` | ~155 | UNF-Handler: Liest/schreibt Binärdateien, konvertiert zu NumPy/GeoTIFF |
| `BasinDelineation.py` | ~170 | Einzugsgebiet: Zell-Identifikation über Routing oder Shapefile-Overlay |

### `data/Europe_Input_UNF_Files/` – Historische Rasterdaten

| Unterordner | Inhalt | Zeitraum | Auflösung |
|------------|--------|----------|-----------|
| `G_SURFACE_RUNOFF/` | Oberflächenabfluss [mm/Monat] | 1980–2016 + MEAN | Monatlich |
| `G_URBAN_RUNOFF/` | Urbaner Abfluss [mm/Monat] | 1980–2020 | Monatlich |
| `G_LIVESTOCK_NR/` | Viehdichte [Tiere/Zelle] | 1980–2020 | Monatlich × 12 Kategorien |
| `G_CORR_FACT_RTF/` | Return-Flow-Korrekturfaktoren | 1990–2016 | Monatlich |
| `P_RATE_TON_KM2/` | P-Düngungsraten [t/km²] | 1990–2016 | Jährlich |
| `CROPLAND_CORR_KM2/` | Ackerflächen [km²] | 1990–2016 | Jährlich |
| `OTHER_UNF_FILES/` | Statische Raster (Zellfläche, GCRC, Routing, Erosion, etc.) | Konstant | – |

### `data/Europe_Cell_Input_Files/` – Tabellarische Zelldaten

CSV-Dateien mit Spalten: `cell, pop_urb, pop_rur, pop_tot, rtf_man, rtf_dom, rtf_irr, gdp, salinity, humidity, lu`

- Historisch: `europe_cell_input_1990.csv` bis `europe_cell_input_2016.csv`
- Zukunft: `SSP1/`, `SSP2/`, `SSP5/` mit Dekaden-CSVs

### `data/OTHER_UNF_FILES/` – Statische Dateien

| Datei | Format | Inhalt |
|-------|--------|--------|
| `GAREA.UNF0` | Float | Zellfläche [km²] |
| `GC.UNF2` | Short | Spalten-Koordinate im Raster |
| `GR.UNF2` | Short | Zeilen-Koordinate im Raster |
| `GCRC.UNF4` | Integer | Zell-ID (GCRC-Nummer) |
| `G_OUTFLC.UNF4` | Integer | Routing: nächste Unterstrom-Zelle |
| `GBUILTUP.UNF0` | Float | Versiegelungsgrad [-] |
| `G_SOILEROS.UNF0` | Float | Bodenerosionsrate [kg/km²/a] |
| `G_PATMDEPOS.UNF0` | Float | Atmosphärische P-Deposition [kg/km²/a] |
| `G_PWEATHERING.UNF0` | Float | Chemische P-Verwitterung [kg/km²/a] |
| `GFREQW.UNF1` | Byte | Wasserflächenanteil [%] |
| `G_LAND_AREA.UNF1` | Byte | Landflächenanteil [%] |
