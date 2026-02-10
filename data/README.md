# Data Directory

Dieses Verzeichnis enthaelt die Input-Daten fuer WorldQual Lite.

Die Daten sind **nicht im Git-Repository** enthalten (zu gross). Sie muessen manuell von der externen SSD oder einem anderen Speicherort hierher kopiert oder verlinkt werden.

## Welche Daten brauche ich?

Nicht alle Ordner werden fuer jeden Lauf benoetigt. Die folgende Tabelle zeigt, was je nach Konfiguration noetig ist.

### Immer benoetigt

| Ordner | Inhalt | Bemerkung |
|--------|--------|-----------|
| `Europe_Input_UNF_Files/OTHER_UNF_FILES/` | Statische Raster (GAREA, GC, GR, GCRC, Erosion, Deposition, Verwitterung) | Pflicht fuer jeden Run |
| `Europe_Input_UNF_Files/G_LIVESTOCK_NR/` | Viehdichte (12 Kategorien x 12 Monate) | Pflicht fuer jeden Run |
| `Europe_Cell_Input_Files/` | Zelldaten-CSVs (Bevoelkerung, Return Flows, GDP etc.) | Nur die Jahres-CSVs im Wurzelordner |

### Nur bei run_type = 'Historical'

| Ordner | Inhalt |
|--------|--------|
| `Europe_Input_UNF_Files/G_SURFACE_RUNOFF/` | Oberflaechenabfluss (monatlich, 1980-2020) |
| `Europe_Input_UNF_Files/G_URBAN_RUNOFF/` | Urbaner Abfluss (monatlich, 1980-2020) |
| `Europe_Input_UNF_Files/G_CORR_FACT_RTF/` | Return-Flow-Korrekturfaktoren (monatlich, 1990-2016) |
| `Europe_Input_UNF_Files/P_RATE_TON_KM2/` | P-Duengungsraten (jaehrlich, 1990-2016) |
| `Europe_Input_UNF_Files/CROPLAND_CORR_KM2/` | Ackerflaechen (jaehrlich, 1990-2016) |

### Nur bei run_type = 'Future'

| Ordner | Inhalt |
|--------|--------|
| `Future_UNF_files/Hydrology/{cont}/{rcp}_{GCM}/` | Abfluss-Daten fuer das gewaehlte RCP/GCM |
| `Future_UNF_files/CROPLAND_AREA_KM2/{SSP}/{cont}/` | Ackerflaechen fuer den gewaehlten SSP |
| `Future_UNF_files/P_RATE_TON_KM2/{SSP}/{cont}/` | P-Duengungsraten fuer den gewaehlten SSP |
| `Future_UNF_files/LIVESTOCK_NR/{SSP}/{cont}/` | Viehdichte fuer den gewaehlten SSP |
| `Future_UNF_files/correction_factors/{rcp}_{SSP}/{cont}/{GCM}/` | Korrekturfaktoren fuer die gewaehlte Kombination |
| `Europe_Cell_Input_Files/{SSP}/` | Zelldaten-CSVs fuer den gewaehlten SSP (Dekaden) |

### Optional

| Ordner | Inhalt | Wann benoetigt |
|--------|--------|---------------|
| `WG_mothers/` | WaterGAP-Muttergitter (Shapefiles) | Nur fuer BasinDelineation.py (Shapefile-Overlay-Methode). Nicht noetig wenn die Zellenliste bereits existiert. |

---

## Einrichtung

### Option A: Symlink zur SSD (empfohlen)

Erstellt Verknuepfungen zu den Daten auf der externen SSD, ohne sie zu kopieren:

```bash
cd data

# Historische UNF-Daten
ln -sf /Volumes/Extreme\ SSD/WorldQual_lite/Europe_Input_UNF_Files/* Europe_Input_UNF_Files/

# Zelldaten
ln -sf /Volumes/Extreme\ SSD/WorldQual_lite/Europe_Cell_Input_Files/* Europe_Cell_Input_Files/

# Future-Daten (nur wenn benoetigt)
ln -sf /Volumes/Extreme\ SSD/WorldQual_lite/Future_UNF_files/* Future_UNF_files/

# Shapefiles (nur wenn benoetigt)
ln -sf /Volumes/Extreme\ SSD/WorldQual_lite/WG_mothers/* WG_mothers/
```

### Option B: Daten kopieren

```bash
cp -r /Volumes/Extreme\ SSD/WorldQual_lite/Europe_Input_UNF_Files/* data/Europe_Input_UNF_Files/
cp -r /Volumes/Extreme\ SSD/WorldQual_lite/Europe_Cell_Input_Files/* data/Europe_Cell_Input_Files/
# etc.
```

### Pruefung

Nach dem Einrichten sollten z.B. folgende Dateien existieren:

```
data/Europe_Input_UNF_Files/OTHER_UNF_FILES/GAREA.UNF0
data/Europe_Input_UNF_Files/G_SURFACE_RUNOFF/G_SURFACE_RUNOFF_2010.12.UNF0
data/Europe_Cell_Input_Files/europe_cell_input_2010.csv
```
