# Datenbank & Datenquellen

## MySQL-Datenbank

Das Originalmodell nutzt zwei MySQL-Datenbanken auf `134.147.42.33`:

### `globewq_wq_load` – Länderdaten

| Tabelle | Inhalt | Schlüssel |
|---------|--------|-----------|
| `country_input` | Bevölkerung, Kanalanschluss, Return Flows, Sanitär-Statistiken | IDScen, time, country_id |
| `country_parameter_input` | Emissionsfaktor, Konzentrationen (ef, conc_man_*, conc_urb) | parameter_id, time, country_id |
| `parameter_input` | Entfernungsraten (rem_prim/sec/tert/untr/quat), treat_failure | IDScen, parameter_id |
| `livestock_excretion_rate` | Exkretionsraten für 12 Viehkategorien | parameter_id, country_id |

### `globewq_wq_load_eu` – Zelldaten (Europa)

| Tabelle | Inhalt | Schlüssel |
|---------|--------|-----------|
| `cell_input` | pop_urb, pop_rur, pop_tot, rtf_man, rtf_dom, rtf_irr, gdp, salinity, humidity, lu | IDScen, time, cell |

---

## CSV-Alternative (empfohlen)

Da der MySQL-Server nicht immer erreichbar ist, können alle Länderdaten auch aus CSV-Dateien geladen werden. Dazu `data_source = 'Excel'` in `Paths_and_params.py` setzen.

### Zelldaten

Bereits als CSV vorhanden in `data/Europe_Cell_Input_Files/`:

```
europe_cell_input_1990.csv
europe_cell_input_1991.csv
...
europe_cell_input_2016.csv
```

**Spalten:**

| Spalte | Typ | Einheit | Beschreibung |
|--------|-----|---------|-------------|
| `cell` | int | – | Zell-ID (1-basiert, nicht GCRC) |
| `pop_urb` | float | Einwohner | Urbane Bevölkerung |
| `pop_rur` | float | Einwohner | Rurale Bevölkerung |
| `pop_tot` | float | Einwohner | Gesamtbevölkerung |
| `rtf_man` | float | m³/a | Industrieller Return Flow |
| `rtf_dom` | float | m³/a | Häuslicher Return Flow |
| `rtf_irr` | float | m³/a | Bewässerungs-Return Flow |
| `gdp` | float | $/cap/a | BIP pro Kopf |
| `salinity` | float | – | Salinität |
| `humidity` | float | – | Feuchtigkeit |
| `lu` | int | – | Landnutzungsklasse |

Zukunftsszenarien liegen in Unterordnern `SSP1/`, `SSP2/`, `SSP5/` mit Dekaden-CSVs (2010, 2020, ..., 2100).

### Länderdaten (müssen bereitgestellt werden)

Wenn die MySQL-Datenbank nicht erreichbar ist, müssen die Länderdaten als CSV-Dateien bereitgestellt werden. Folgende Datensätze werden benötigt:

#### `country_data.csv` – Bevölkerung & Sanitär-Infrastruktur

| Spalte | Typ | Einheit | DB-Quelle |
|--------|-----|---------|-----------|
| `country_id` | int | ISO 3166 | country_input |
| `year` | int | – | country_input.time |
| `IDScen` | int | – | country_input.IDScen |
| `pop_tot` | float | Einwohner | country_input |
| `pop_urb` | float | Einwohner | country_input |
| `pop_rur` | float | Einwohner | country_input |
| `con_prim` | float | Anteil [0–1] | Primärbehandlung |
| `con_sec` | float | Anteil [0–1] | Sekundärbehandlung |
| `con_tert` | float | Anteil [0–1] | Tertiärbehandlung |
| `con_untr` | float | Anteil [0–1] | Unbehandelt |
| `con_quat` | float | Anteil [0–1] | Quartärbehandlung |
| `stp_failure` | float | Anteil [0–1] | Kläranlagen-Ausfallrate |
| `UrbSewerConn` | float | Anteil [0–1] | Urbaner Kanalanschluss |
| `RurSewerConn` | float | Anteil [0–1] | Ruraler Kanalanschluss |
| `SPO_treat` | float | Anteil [0–1] | Behandlungsanteil Streusiedlungen |
| `to_treat_and_unknown` | float | Anteil [0–1] | Septic Tanks |
| `to_hanging_t` | float | Anteil [0–1] | Hängelatrinen |
| `to_open_def` | float | Anteil [0–1] | Offene Defäkation |
| `rtf_man` | float | m³/a | Industrieller Return Flow |

#### `emission_factors.csv` – Emissionsfaktoren

| Spalte | Typ | Einheit | DB-Quelle |
|--------|-----|---------|-----------|
| `country_id` | int | ISO 3166 | country_parameter_input |
| `parameter_id` | int | – | 60 für TP |
| `ef` | float | kg/cap/a | Emissionsfaktor |

#### `removal_rates.csv` – Entfernungsraten

| Spalte | Typ | Einheit | DB-Quelle |
|--------|-----|---------|-----------|
| `parameter_id` | int | – | parameter_input |
| `IDScen` | int | – | parameter_input |
| `rem_prim` | float | Anteil [0–1] | Primär |
| `rem_sec` | float | Anteil [0–1] | Sekundär |
| `rem_tert` | float | Anteil [0–1] | Tertiär |
| `rem_untr` | float | Anteil [0–1] | Unbehandelt |
| `rem_quat` | float | Anteil [0–1] | Quartär |
| `treat_failure` | float | Anteil [0–1] | Ausfallrate |

#### `concentrations.csv` – Konzentrationen in Return Flows

| Spalte | Typ | Einheit | DB-Quelle |
|--------|-----|---------|-----------|
| `country_id` | int | ISO 3166 | country_parameter_input |
| `parameter_id` | int | – | 60 für TP |
| `conc_man_nd` | float | mg/l | Industrie-Konzentration |
| `conc_urb` | float | mg/l | Urbane Event Mean Concentration |

#### `livestock_excretion.csv` – Vieh-Exkretionsraten

| Spalte | Typ | Einheit | DB-Quelle |
|--------|-----|---------|-----------|
| `country_id` | int | ISO 3166 | livestock_excretion_rate |
| `parameter_id` | int | – | 60 für TP |
| `cattle_dairy` | float | t/Tier/a | Milchkühe |
| `cattle_other` | float | t/Tier/a | Sonstige Rinder |
| `buffalo` | float | t/Tier/a | Büffel |
| `sheep` | float | t/Tier/a | Schafe |
| `goats` | float | t/Tier/a | Ziegen |
| `pigs` | float | t/Tier/a | Schweine |
| `poultry_layers` | float | t/Tier/a | Legehennen |
| `poultry_broiler` | float | t/Tier/a | Masthähnchen |
| `horses` | float | t/Tier/a | Pferde |
| `asses` | float | t/Tier/a | Esel |
| `mules` | float | t/Tier/a | Maultiere |
| `camels` | float | t/Tier/a | Kamele |

---

## GCRC-Konvertierung

Die Datenbank-Funktion `Cell_ID_To_GCRC()` konvertiert fortlaufende Zell-IDs in GCRC-Nummern. Ohne DB-Zugang kann die Konvertierung direkt aus der UNF-Datei `GCRC.UNF4` gelesen werden:

```python
from BinaryFileHandler import ReadBin

ng_europe = 180721
gcrc_values = ReadBin("data/Europe_Input_UNF_Files/OTHER_UNF_FILES/GCRC.UNF4", ng_europe)
# gcrc_values[i] = GCRC-Nummer der Zelle mit Index i (0-basiert)
# Zell-ID = i + 1 (1-basiert)
```
