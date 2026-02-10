# API-Referenz

## WorldQual_Lite_TP.py – Hauptmodul

### Frachtberechnungs-Funktionen

#### `DomesticSewered()`
Berechnet TP-Fracht aus häuslichem Abwasser, das an Kläranlagen angeschlossen ist.

**Input:** Bevölkerung (urban/rural), Emissionsfaktor, Kanalanschlussrate, Kläranlagen-Behandlungsstufen (primär/sekundär/tertiär/quartär), Entfernungsraten, STP-Ausfallrate.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `DomesticNonsewered()`
Berechnet TP-Fracht aus Streusiedlungen (nicht an Kanalisation angeschlossen).

**Input:** Nicht-angeschlossene Bevölkerung, Emissionsfaktor, Anteile (behandelt/Hängelatrinen/offene Defäkation), Bodenentfernungsrate.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `Manufacturing()`
Berechnet TP-Fracht aus Industrieabwässern.

**Input:** Industrieller Return Flow [m³/a], Konzentration in Return Flows [mg/l], Kläranlagen-Anschlussraten, Entfernungsraten.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `Inorganic_Fertilizer_new_method()`
Berechnet TP-Fracht aus anorganischem Dünger über Erosion.

**Input:** P-Düngungsrate [t/km²], Ackerfläche [km²], Erosionskoeffizient.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `AgricultureLivestock()`
Berechnet TP-Fracht aus Viehexkrementen.

**Input:** Viehdichte (12 Kategorien × 12 Monate), Exkretionsraten, Erosionskoeffizient.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `BackgroundAtm()`
Berechnet TP-Fracht aus atmosphärischer Deposition.

**Input:** Depositionsrate [kg/km²/a], Zellfläche, Landflächenanteil.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `BackgroundCW()`
Berechnet TP-Fracht aus chemischer Verwitterung.

**Input:** Verwitterungsrate [kg/km²/a], Zellfläche, Landflächenanteil.

**Output:** Monatliche TP-Fracht [t/Monat]

#### `UrbanSurfaceRunoff()`
Berechnet TP-Fracht aus urbanem Oberflächenabfluss.

**Input:** Urbaner Abfluss [mm/Monat], Event Mean Concentration [mg/l], Zellfläche, Versiegelungsgrad.

**Output:** Monatliche TP-Fracht [t/Monat]

### Hilfsfunktionen

#### `Cell_Yearly_ErodedPortion(SR, Lmax, a, b, c, SoilErosion, P_input)`
Berechnet den Erosionsanteil nach Fink et al.

**Parameter:**

| Parameter | Typ | Einheit | Beschreibung |
|-----------|-----|---------|-------------|
| `SR` | float | mm/a | Jährlicher Oberflächenabfluss |
| `Lmax` | float | - | Max. gelöster P-Auslaugungsanteil |
| `a` | float | - | Skalierungsparameter |
| `b` | float | - | Exponent |
| `c` | float | - | PP-Koeffizient |
| `SoilErosion` | float | kg/km²/a | Bodenerosionsrate |
| `P_input` | float | t/a | P-Eintrag in den Boden |

**Return:** float – Erodierter Anteil [0–1]

#### `Load_After_Retention_factor(Load_in, HL)`
Wendet den Vollenweider-Retentionsfaktor an.

**Parameter:**

| Parameter | Typ | Einheit | Beschreibung |
|-----------|-----|---------|-------------|
| `Load_in` | float | t/a | Eingangs-Fracht |
| `HL` | float | m/a | Hydraulic Load |

**Return:** float – Fracht nach Retention [t/a]

---

## BinaryFileHandler.py – UNF-Datei-Handler

#### `ReadBin(filepath, ng, months=1)`
Liest eine UNF-Binärdatei in eine Python-Liste.

**Parameter:**

| Parameter | Typ | Beschreibung |
|-----------|-----|-------------|
| `filepath` | str | Pfad zur UNF-Datei |
| `ng` | int | Anzahl Rasterzellen im Kontinent |
| `months` | int | Anzahl Zeitschritte (1 oder 12) |

**Return:** list – Werte als flache Liste oder verschachtelte Liste [ng × months]

#### `FileToArray(data, GC, GR, nrow, ncol)`
Konvertiert eine Liste in ein 2D-NumPy-Array mit GC/GR-Koordinaten.

#### `ArrayToRaster(array, output_path, nrow, ncol, geotransform, projection)`
Exportiert ein NumPy-Array als GeoTIFF über GDAL.

#### `Path_Concatenate(folder, prefix, year, suffix)`
Baut Dateipfade für Jahresdateien zusammen (z.B. `G_SURFACE_RUNOFF_2010.12.UNF0`).

---

## InputDataFetchFunctions.py – Datenzugriff

Alle Funktionen verbinden sich zur MySQL-Datenbank über `LoadDatabase(dbname)`.

| Funktion | Datenbank | Rückgabe |
|----------|-----------|---------|
| `CountryPopulation(dbname, IDScen, time, country_id)` | globewq_wq_load | pop_tot, pop_urb, pop_rur |
| `CountryEmmisionFactor(dbname, parameter_id, time, country_id)` | globewq_wq_load | ef [kg/cap/year] |
| `CountryConnectionToTreatment(dbname, IDScen, time, country_id)` | globewq_wq_load | con_prim/sec/tert/untr/quat, stp_failure, UrbSewerConn, RurSewerConn, SPO_treat |
| `RemovalRate(dbname, parameter_id, IDScen)` | globewq_wq_load | rem_prim/sec/tert/untr/quat, treat_failure |
| `CountryReturnFlows(dbname, IDScen, time, country_id)` | globewq_wq_load | rtf_man [m³/a] |
| `CountryConcInReturnFlows(dbname, parameter_id, time, country_id)` | globewq_wq_load | conc_man_nd, conc_urb [mg/l] |
| `LivestockExcretionRate(dbname, parameter_id, country_id)` | globewq_wq_load | 12 Kategorien [t/Tier/a] |
| `Cell_ID_To_GCRC(dbname, cell_id)` | globewq_wq_load_eu | GCRC-Nummer |
| `IDFaoReg_from_Country_Id(country_id)` | globewq_wq_load | FAO-Region |

---

## BasinDelineation.py – Einzugsgebiets-Definition

#### `DelineateBasin(MostDownstreamCell, outflowpath, ng, continent_index)`
Identifiziert alle Oberstrom-Zellen durch Rückverfolgung des Routing-Netzwerks.

**Parameter:**

| Parameter | Typ | Beschreibung |
|-----------|-----|-------------|
| `MostDownstreamCell` | list[int] | GCRC-IDs der Auslass-Zelle(n) |
| `outflowpath` | str | Pfad zu G_OUTFLC.UNF4 |
| `ng` | int | Gesamtzahl Rasterzellen |
| `continent_index` | int | Index des Kontinents |

**Return:** list[int] – GCRC-IDs aller Zellen im Einzugsgebiet
