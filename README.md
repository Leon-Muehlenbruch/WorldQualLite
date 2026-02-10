# WorldQual Lite

Vereinfachtes Python-Modell zur Berechnung von **Gesamtphosphor-Frachten (TP)** auf Einzugsgebietsebene. Basiert auf dem [WorldQual-Wasserqualitätsmodell](https://leon-muehlenbruch.github.io/WorldQual/).

## Dokumentation

**[→ leon-muehlenbruch.github.io/WorldQual-lite](https://leon-muehlenbruch.github.io/WorldQual-lite/)**

## Überblick

WorldQual Lite berechnet monatliche und jährliche TP-Einträge aus 8 Quellen:

- Häusliches Abwasser (angeschlossen & Streusiedlungen)
- Industrie
- Anorganischer Dünger
- Viehwirtschaft
- Atmosphärische Deposition
- Chemische Verwitterung
- Urbaner Oberflächenabfluss

### Unterschied zur Vollversion

| | WorldQual | WorldQual Lite |
|--|----------|----------------|
| Sprache | C++ | Python |
| Parameter | 6 (BOD, TDS, FC, TN, TP, Pestizide) | Nur TP |
| Routing | Vollständiges Instream-Routing | Keine (Frachtsummierung) |
| Umfang | Kontinent | Einzelnes Einzugsgebiet |

## Schnellstart

```bash
# Klonen
git clone https://github.com/Leon-Muehlenbruch/WorldQual-lite.git
cd WorldQual-lite

# Abhängigkeiten
pip install -r requirements.txt

# Konfiguration anpassen
#   → src/Paths_and_params.py (Pfade, Zeitraum, Szenario)

# Ausführen
cd src && python WorldQual_Lite_TP.py
```

## Projektstruktur

```
WorldQual-lite/
├── src/                    # Python-Quellcode
│   ├── WorldQual_Lite_TP.py
│   ├── Paths_and_params.py
│   ├── InputDataFetchFunctions.py
│   ├── BinaryFileHandler.py
│   └── BasinDelineation.py
├── data/                   # Input-Daten (nicht in Git)
│   ├── Europe_Input_UNF_Files/
│   ├── Europe_Cell_Input_Files/
│   └── Future_UNF_files/
├── docs/                   # MkDocs-Dokumentation
├── mkdocs.yml
└── requirements.txt
```

## Autor

- **Originalmodell:** Ammanuel Tilahun
- **Dokumentation & Aufbereitung:** Leon Mühlenbruch

## Verwandtes Projekt

- [WorldQual (Vollversion)](https://leon-muehlenbruch.github.io/WorldQual/) – C++ Instream-Modell mit vollständigem Routing
