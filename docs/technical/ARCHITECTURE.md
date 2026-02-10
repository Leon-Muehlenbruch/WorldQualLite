# Architektur

## Modulübersicht

```
Paths_and_params.py          ← Konfiguration (Pfade, Szenarien, Kalibrierung)
        │
        ▼
WorldQual_Lite_TP.py         ← Hauptmodul (Frachtberechnung)
        │
        ├── BinaryFileHandler.py    ← UNF-Datei I/O
        │
        └── InputDataFetchFunctions.py  ← DB/CSV-Datenzugriff
                │
                └── MySQL oder CSV-Dateien

BasinDelineation.py          ← Einzugsgebiets-Definition (eigenständig)
```

## Datenfluss

```
[UNF-Dateien]──────────────┐
  Oberflächenabfluss        │
  Urbaner Abfluss           │    ┌─────────────────────┐
  Viehdichte                ├───►│                     │
  Korrekturfaktoren         │    │  WorldQual_Lite_TP  │
  P-Raten, Cropland         │    │                     │
  Zellfläche, Erosion, ...  │    │  Für jede Zelle:    │
                            │    │  ├─ DomesticSewered │──► CSV
[DB/CSV]────────────────────┤    │  ├─ Manufacturing   │    (monatl./jährl.
  Bevölkerung               │    │  ├─ Fertilizer      │     Frachten)
  Emissionsfaktoren         ├───►│  ├─ Livestock       │
  Kläranlagen-Raten         │    │  ├─ Scattered       │──► Plot
  Entfernungsraten          │    │  ├─ Atm. Deposition │    (Stacked Bar)
  Konzentration Industrie   │    │  ├─ Chem. Weather.  │
  Vieh-Exkretionsraten      │    │  └─ Urban Runoff    │──► RMSE, R²
                            │    │                     │
[Basin-Zellenliste]─────────┘    └─────────────────────┘
```

## Berechnungslogik

### Hauptschleife

Das Modell iteriert über Jahre. Pro Jahr:

1. **Datenladen**: UNF-Dateien für das aktuelle Jahr lesen (Abfluss, Vieh, Korrekturfaktoren, etc.)
2. **Zellschleife**: Für jede Zelle im Einzugsgebiet und jeden Monat:
    - 8 Frachtkomponenten berechnen
    - Erosionsanteil anwenden (`Cell_Yearly_ErodedPortion`)
    - Auf Einzugsgebiet aufsummieren
3. **Retention**: Auf die Gesamtfracht den Retentionsfaktor anwenden (`Load_After_Retention_factor`)
4. **Output**: CSV schreiben, Plot erzeugen

### Erosionsmodell (Fink et al.)

Diffuse Quellen (Dünger, Vieh, Deposition, Verwitterung) unterliegen einem Erosionskoeffizienten:

```
ErodedPortion = Lmax × (1 - exp(-(SR/a)^b)) + c × SoilErosion × P_input
```

Dabei ist:
- `SR` = Oberflächenabfluss [mm/a]
- `Lmax, a, b, c` = Kalibrierungsparameter
- `SoilErosion` = Bodenerosionsrate [kg/km²/a]
- `P_input` = P-Eintrag in den Boden

### Retentionsmodell (Vollenweider)

Die Fracht am Einzugsgebietsauslass wird durch Retention in Wasserkörpern reduziert:

```
Load_out = Load_in / (1 + a × HL^b)
```

Dabei ist `HL` = Hydraulic Load = Q_out / Seefläche.

### Behandlungseffizienz (Kläranlagen)

Für Punktquellen (Häuslich, Industrie):

```
Load_treated = Σ (Pop × ef × conn_level × (1 - rem_level)) × (1 - stp_failure)
```

Dabei werden 5 Behandlungsstufen unterschieden: unbehandelt, primär, sekundär, tertiär, quartär.

### Streusiedlungen

Nicht angeschlossene Bevölkerung wird in 3 Kategorien aufgeteilt:
- **Behandelt** (Septic Tanks, Klärgruben) → Bodenentfernung angewandt
- **Hängende Latrinen** → Direkter Eintrag
- **Offene Defäkation** → Diffuser Eintrag über Abfluss

## Vergleich mit WorldQual (Vollversion)

| Aspekt | Vollversion (C++) | Lite (Python) |
|--------|------------------|---------------|
| Frachtberechnung (wq_load) | Ja, identische Logik | Ja, portiert |
| Instream-Transport (worldqual) | Ja, Routing, Abbau, Seen | Nein |
| Statistik (wq_stat) | Ja, Stationsvergleich | Eingeschraenkt, nur RMSE am Auslass |
| Erosionsmodell | Ja, Fink et al. | Ja, identisch |
| Retentionsmodell | Ja, physikbasiert | Vereinfacht (Vollenweider) |
| Multi-Parameter | Ja, 6 Parameter | Nein, nur TP |
| Parallelisierung | Nein, Single-Core | Nein, Single-Core |
