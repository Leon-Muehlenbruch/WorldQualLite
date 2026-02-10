# Schnellreferenz

## Kalibrierungsparameter (Moehne-Einzugsgebiet)

| Parameter | Wert | Beschreibung |
|-----------|------|-------------|
| `Lmax_calib` | 6.34e-02 | Max. gelöster P-Auslaugungsanteil |
| `a_calib` | 900 | Abfluss-DP-Beziehung |
| `b_calib` | -2 | Abfluss-DP-Exponent |
| `c_calib` | 1e-12 | PP-Erosions-Koeffizient |
| `sc_corr_calib` | 1 | Streusiedlungs-Korrekturfaktor |
| `bg_corr_calib` | 1 | Hintergrund-Korrekturfaktor |
| `Point_load_corr` | 1 | Punktquellen-Korrekturfaktor |

## Kontinent-Codes

| Index | Kürzel | Kontinent | ng (Zellen) | Zeilen × Spalten |
|-------|--------|-----------|-------------|-----------------|
| 0 | eu | Europa | 180.721 | 641 × 1000 |
| 1 | af | Afrika | 371.410 | 1090 × 1237 |
| 2 | as | Asien | 841.703 | 1258 × 4320 |
| 3 | au | Australien | 109.084 | 740 × 4309 |
| 4 | na | Nordamerika | 461.694 | 915 × 1519 |
| 5 | sa | Südamerika | 226.852 | 824 × 1356 |

## Wichtige IDs

| ID | Wert | Bedeutung |
|----|------|-----------|
| `parameter_id` | 60 | Gesamtphosphor (TP) |
| `country_id` | 276 | Deutschland (ISO 3166) |
| `IDScen` | 27 | Standard-Szenario |
| `IDReg` | 1 | Europa |

## Szenario-Kombinationen (Future)

| SSP | RCP | Beschreibung |
|-----|-----|-------------|
| SSP1 | rcp2p6 | Nachhaltigkeit, niedrige Emissionen |
| SSP2 | rcp6p0 | Mittlerer Weg |
| SSP5 | rcp8p5 | Fossile Entwicklung, hohe Emissionen |

**Verfügbare GCMs:** GFDL-ESM2M, HadGEM2-ES, IPSL-CM5a-LR, MIROC5

## UNF-Dateiformate

| Suffix | Bytes/Wert | Datentyp | Beispiel |
|--------|-----------|----------|---------|
| `.UNF0` | 4 | Float (Big-Endian) | Oberflächenabfluss, Zellflächen |
| `.UNF1` | 1 | Byte/Character | Landflächenanteil |
| `.UNF2` | 2 | Short Integer | GC/GR-Koordinaten |
| `.UNF4` | 4 | Integer | GCRC-IDs, Routing |

Monatliche Dateien haben `.12.` im Namen (z.B. `G_SURFACE_RUNOFF_2010.12.UNF0` = 12 Monate).

## TP-Quellen im Modell

| # | Funktion | Quelltyp | Beschreibung |
|---|----------|----------|-------------|
| 1 | `DomesticSewered()` | Punkt | Kläranlagen-Abwasser |
| 2 | `DomesticNonsewered()` | Punkt | Streusiedlungen (Latrinen, Septic) |
| 3 | `Manufacturing()` | Punkt | Industrieabwässer |
| 4 | `Inorganic_Fertilizer_new_method()` | Diffus | Mineraldünger-Erosion |
| 5 | `AgricultureLivestock()` | Diffus | Vieh-Exkremente |
| 6 | `BackgroundAtm()` | Diffus | Atmosphärische P-Deposition |
| 7 | `BackgroundCW()` | Diffus | Chemische Verwitterung |
| 8 | `UrbanSurfaceRunoff()` | Diffus | Versiegelter Flächenabfluss |

## Häufige Befehle

```bash
# Modell ausführen
cd src && python WorldQual_Lite_TP.py

# Einzugsgebiet definieren
python BasinDelineation.py

# Abhängigkeiten installieren
pip install -r requirements.txt
```
