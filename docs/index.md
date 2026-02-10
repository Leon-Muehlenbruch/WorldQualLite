# WorldQual Lite – Vereinfachtes TP-Frachtmodell

**Dokumentations-Übersicht:** [Home](index.md) | [Schnellreferenz](user/schnellreferenz.md) | [Detaillierte Anleitung](user/anleitung.md) | [Projektstruktur](user/projektstruktur.md)

## Was ist WorldQual Lite?

WorldQual Lite ist eine vereinfachte Python-Implementierung des [WorldQual-Wasserqualitätsmodells](https://leon-muehlenbruch.github.io/WorldQual/). Es berechnet **monatliche und jährliche Gesamtphosphor-Frachten (TP)** auf Einzugsgebietsebene aus verschiedenen Punkt- und diffusen Quellen.

### Einfach erklärt

WorldQual Lite beantwortet die Frage: **Wie viel Phosphor gelangt pro Jahr in ein Gewässer – und woher kommt er?**

Das Modell berechnet TP-Einträge aus 8 Quellen:

| Quelle | Beschreibung | Typ |
|--------|-------------|-----|
| **Häuslich (angeschlossen)** | Abwasser über Kläranlagen | Punktquelle |
| **Streusiedlungen** | Nicht an Kanalisation angeschlossen | Punktquelle |
| **Industrie** | Manufacturing-Abwässer | Punktquelle |
| **Anorganischer Dünger** | Mineraldünger auf Ackerflächen | Diffus |
| **Viehwirtschaft** | Tierexkremente | Diffus |
| **Atmosphärische Deposition** | P-Eintrag über Niederschlag | Diffus |
| **Chemische Verwitterung** | Natürlicher P-Eintrag aus Gestein | Diffus |
| **Urbaner Oberflächenabfluss** | Abfluss von versiegelten Flächen | Diffus |

### Unterschied zur Vollversion

WorldQual Lite ist bewusst reduziert gegenüber dem [vollständigen WorldQual-Modell](https://leon-muehlenbruch.github.io/WorldQual/):

| Eigenschaft | WorldQual (Voll) | WorldQual Lite |
|------------|-----------------|----------------|
| **Sprache** | C++ | Python |
| **Parameter** | BOD, TDS, FC, TN, TP, Pestizide | Nur TP |
| **Instream-Routing** | Vollständiges Fluss-Routing mit Abbau | Kein Routing, nur Frachtsummierung |
| **Räumlicher Umfang** | Kompletter Kontinent | Einzelnes Einzugsgebiet |
| **Retention** | Physikbasiert (Seen, Flussabschnitte) | Vereinfacht (Vollenweider, HL-basiert) |
| **Datenbank** | MySQL (Pflicht) | MySQL oder CSV-Dateien |
| **Industriesektoren** | 7 Sektoren detailliert | Aggregiert (1 Konzentration) |
| **Bergbau** | 5 Ressourcentypen | Nicht enthalten |
| **Pestizide** | Vollständiges Modul | Nicht enthalten |
| **Temperaturabhängigkeit** | Ja (Abbauraten) | Nein |

### Typische Anwendungen

- **Einzugsgebiets-Analyse**: TP-Frachten für ein spezifisches Einzugsgebiet berechnen
- **Quellenaufteilung**: Identifizieren der dominanten P-Quellen (Source Apportionment)
- **Szenarienvergleich**: Historisch (1990–2016) vs. Zukunft (SSP1/2/5 × RCP × GCM)
- **Kalibrierung**: Modellparameter gegen Messdaten optimieren (RMSE, R²)

---

## Schnellstart

### Voraussetzungen

- Python 3.8+
- Pakete: `pip install -r requirements.txt`
- Input-Daten (UNF-Dateien und Cell-Input-CSVs)
- Entweder MySQL-Datenbankzugang **oder** vorab exportierte CSV-Dateien für Länderdaten

### In 4 Schritten zur ersten Simulation

```bash
# 1. Repository klonen
git clone https://github.com/Leon-Muehlenbruch/WorldQual-lite.git
cd WorldQual-lite

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Konfiguration anpassen
#    → src/Paths_and_params.py editieren (Pfade, Parameter, Zeitraum)

# 4. Modell ausführen
cd src
python WorldQual_Lite_TP.py
```

Detaillierte Anleitung: [Benutzer-Dokumentation → Anleitung](user/anleitung.md)

---

## Weitere Hilfe

**Für Nutzer:**

- [Detaillierte Anleitung](user/anleitung.md) – Schritt-für-Schritt von Installation bis Ergebnis
- [Schnellreferenz](user/schnellreferenz.md) – Parameter, Kalibrierungswerte, wichtige IDs
- [Projektstruktur](user/projektstruktur.md) – Verzeichnisse, Dateien, Datenformate

**Für Entwickler:**

- [Architektur](technical/ARCHITECTURE.md) – Module, Datenfluss, Berechnungslogik
- [API-Referenz](technical/API.md) – Alle Funktionen und ihre Parameter
- [Datenbank & Datenquellen](technical/DATA_SOURCES.md) – DB-Tabellen und CSV-Alternativen
- [Input-Daten Checkliste](technical/DATA_REQUIREMENTS.md) – Was wird gebraucht, was ist vorhanden

**Verwandtes Projekt:**

- [WorldQual (Vollversion)](https://leon-muehlenbruch.github.io/WorldQual/) – Vollständiges C++ Instream-Modell

---

**Ursprünglicher Autor:** Ammanuel Tilahun  
**Dokumentation & Aufbereitung:** Leon Mühlenbruch  
**Letzte Aktualisierung:** Februar 2026
