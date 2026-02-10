# Input-Daten Checkliste

Uebersicht aller benoetigten Input-Daten mit Verfuegbarkeitsstatus.

## Legende

| Symbol | Bedeutung |
|--------|-----------|
| Vorhanden | Auf SSD verfuegbar |
| Teilweise | Vorhanden, aber nur bestimmte Szenarien |
| Fehlend | Nicht verfuegbar, muss beschafft werden |

---

## UNF-Rasterdaten (Historisch)

| Datensatz | Ordner | Zeitraum | Status |
|-----------|--------|----------|--------|
| Oberflaechenabfluss | `G_SURFACE_RUNOFF/` | 1980-2020 + MEAN | Vorhanden |
| Urbaner Abfluss | `G_URBAN_RUNOFF/` | 1980-2020 | Vorhanden |
| Viehdichte (12 Kat. x 12 Mon.) | `G_LIVESTOCK_NR/` | 1980-2020 | Vorhanden |
| Return-Flow-Korrekturfaktoren | `G_CORR_FACT_RTF/` | 1990-2016 | Vorhanden |
| P-Duengungsraten | `P_RATE_TON_KM2/` | 1990-2016 | Vorhanden |
| Ackerflaechen | `CROPLAND_CORR_KM2/` | 1990-2016 | Vorhanden |

## Statische UNF-Dateien

| Datei | Format | Inhalt | Status |
|-------|--------|--------|--------|
| `GAREA.UNF0` | Float | Zellflaeche [km2] | Vorhanden |
| `GBUILTUP.UNF0` | Float | Versiegelungsgrad | Vorhanden |
| `GC.UNF2` | Short | Spalten-Koordinate | Vorhanden |
| `GR.UNF2` | Short | Zeilen-Koordinate | Vorhanden |
| `GCRC.UNF4` | Integer | Zell-ID (GCRC) | Vorhanden |
| `G_OUTFLC.UNF4` | Integer | Routing (naechste Unterstrom-Zelle) | Vorhanden |
| `G_LAND_AREA.UNF1` | Byte | Landflaechenanteil | Vorhanden |
| `G_SOILEROS.UNF0` | Float | Bodenerosionsrate | Vorhanden |
| `G_PATMDEPOS.UNF0` | Float | Atmosphaerische P-Deposition | Vorhanden |
| `G_PWEATHERING.UNF0` | Float | Chemische P-Verwitterung | Vorhanden |
| `GFREQW.UNF1` | Byte | Wasserflaechenanteil | Vorhanden |
| `GLCC2000.UNF2` | Short | Landbedeckungsklasse | Vorhanden |

## UNF-Rasterdaten (Zukunft)

| Datensatz | Pfad-Muster | Verfuegbare Szenarien | Status |
|-----------|------------|---------------------|--------|
| Hydrologie (Abfluss) | `Hydrology/eu/{rcp}_{GCM}/` | rcp6p0 x MIROC5 | Teilweise (nur 1 RCP) |
| Ackerflaechen | `CROPLAND_AREA_KM2/{SSP}/eu/` | SSP2 | Teilweise (nur SSP2) |
| P-Duengungsraten | `P_RATE_TON_KM2/{SSP}/eu/` | SSP2 | Teilweise (nur SSP2) |
| Viehdichte | `LIVESTOCK_NR/{SSP}/eu/` | SSP2 | Teilweise (nur SSP2) |
| Korrekturfaktoren | `correction_factors/{rcp}_{SSP}/eu/{GCM}/` | rcp6p0_SSP2 x MIROC5 | Teilweise |

!!! warning "Eingeschraenkte Zukunftsszenarien"
    Auf der SSD liegt nur die Kombination **SSP2 x rcp6p0 x MIROC5** vollstaendig vor. Andere SSP/RCP/GCM-Kombinationen muessen ggf. nachgeliefert werden.

## Zelldaten (CSV)

| Datensatz | Ordner | Zeitraum | Status |
|-----------|--------|----------|--------|
| Historische Zell-Inputs | `Europe_Cell_Input_Files/` | 1990-2016 (jaehrlich) | Vorhanden |
| SSP1-Zell-Inputs | `Europe_Cell_Input_Files/SSP1/` | 2010-2100 (Dekaden) | Vorhanden |
| SSP2-Zell-Inputs | `Europe_Cell_Input_Files/SSP2/` | 2010-2100 (Dekaden) | Vorhanden |
| SSP5-Zell-Inputs | `Europe_Cell_Input_Files/SSP5/` | 2010-2100 (Dekaden) | Vorhanden |

## Laenderdaten (aus Datenbank)

Diese Daten kommen normalerweise aus der MySQL-Datenbank. Ohne DB-Zugang muessen sie als CSV bereitgestellt werden.

| Datensatz | DB-Funktion | Fuer welche Quelle | Status |
|-----------|------------|-------------------|--------|
| Bevoelkerung (Land) | `CountryPopulation()` | Haeuslich | Fehlend |
| Emissionsfaktor | `CountryEmmisionFactor()` | Haeuslich, Streusiedlung | Fehlend |
| Klaeranlagen-Anschluss | `CountryConnectionToTreatment()` | Haeuslich | Fehlend |
| Entfernungsraten | `RemovalRate()` | Haeuslich, Industrie | Fehlend |
| Return Flows (Land) | `CountryReturnFlows()` | Industrie | Fehlend |
| Konzentrationen | `CountryConcInReturnFlows()` | Industrie, Urban | Fehlend |
| Vieh-Exkretionsraten | `LivestockExcretionRate()` | Viehwirtschaft | Fehlend |
| GCRC-Konvertierung | `Cell_ID_To_GCRC()` | Alle | Teilweise (aus UNF ableitbar) |
| FAO-Region | `IDFaoReg_from_Country_Id()` | Streusiedlung | Fehlend |

!!! danger "Kritisch: Laenderdaten fehlen"
    Die MySQL-Datenbank (`134.147.42.33`) ist nicht erreichbar. Fuer einen Modelllauf muessen die Laenderdaten als CSV-Dateien exportiert und bereitgestellt werden. Siehe [Datenquellen - CSV-Alternative](DATA_SOURCES.md#csv-alternative-empfohlen) fuer das benoetigte Format.

## Einzugsgebietsdefinition

| Datensatz | Beschreibung | Status |
|-----------|-------------|--------|
| Basin-Zellenliste (Moehne) | CSV mit Zell-IDs im Einzugsgebiet | Fehlend |
| WG-Muttergitter (Shapefiles) | `WG_mothers/mother_eu.shp` etc. | Vorhanden |
| Routing-Datei | `G_OUTFLC.UNF4` | Vorhanden |

!!! info "Zellenliste generierbar"
    Die Zellenliste kann mit `BasinDelineation.py` aus dem Routing-Netzwerk oder per Shapefile-Overlay erzeugt werden.

## Validierungsdaten

| Datensatz | Beschreibung | Status |
|-----------|-------------|--------|
| Messdaten Moehne (2002-2016) | TP-Jahresfrachten am Auslass | Fehlend |

!!! note "Optional"
    Messdaten werden nur fuer die RMSE-Validierung benoetigt. Das Modell laeuft auch ohne.

---

## Zusammenfassung

| Kategorie | Dateien gesamt | Vorhanden | Fehlend |
|-----------|---------------|-----------|---------|
| UNF-Rasterdaten (historisch) | ~6 Ordner | Alle | - |
| UNF statische Dateien | 12 Dateien | Alle | - |
| UNF-Zukunftsdaten | ~5 Ordner | Nur SSP2/rcp6p0 | Andere Kombinationen |
| Zelldaten (CSV) | ~30 Dateien | Alle | - |
| Laenderdaten (DB) | ~8 Abfragen | Keine | **Alles** |
| Einzugsgebiet | 1 CSV | Keine | Generierbar |
| Validierung | 1 Excel | Keine | Optional |

**Fazit:** Die aufwaendigen Rasterdaten sind vollstaendig vorhanden. Blocker ist die fehlende Laenderdaten-CSV (ca. 20-30 Werte pro Land und Jahr), die aus der Datenbank exportiert werden muss.
