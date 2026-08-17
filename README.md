# Digitalisierung, KI & Gesundheit · Rechercheportal

Ein Rechercheportal zum Themenfeld **Digitalisierung, Künstliche Intelligenz und Gesundheit**:
gebündelte Live-Suchen über medizinische Fachdatenbanken, die Informatik-Literatur, Modell- und
Standardverzeichnisse sowie Regulierung und Institutionen, dazu ein rechtes Frame mit den
**neuesten Studien** samt **deutscher Zusammenfassung**.

Schwesterportale: [Knowledge-Hub Versorgungsforschung](https://wissen.m-vf.de/) und
[Hitze, Klima & Gesundheit](https://klima.m-vf.de/) — gleicher Aufbau, gleiche Technik,
anderes Thema.

Die Seite ist eine einzelne, eigenständige `index.html` (kein Build, keine Abhängigkeiten) und wird
über **GitHub Pages** ausgeliefert.

## Live

```
https://ki.m-vf.de/
```

## Was drin ist

| | |
|---|---|
| Datenbanken | 105 in 10 Rubriken |
| davon Live-Suche | 49 (URL-Suche mit `%s`) |
| Portal-Links | 50 (kein verlinkbares Trefferziel) |
| Lizenzpflichtig | 6 |
| Suchglossar | 250 Fachbegriffe deutsch → englisch |
| Studienauswahl | täglich 6 Uhr aus PubMed, KI-kuratiert |

Zwei Rubriken sind die inhaltliche Besonderheit gegenüber den Schwesterportalen:
**Informatik & KI-Forschung** (Konferenzen und Preprints statt Zeitschriften) und
**KI-Modelle, Daten & Standards** (Modelle, Datensätze und Spezifikationen statt Publikationen).
Beide tragen deshalb einen eigenen Hinweis über den Kacheln.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | die gesamte Anwendung (CSS + HTML + JS inline) |
| `ueber.html` | Hintergrundseite zum Portal |
| `newsletter.html` | Anmeldung, sendet direkt an Mailchimp |
| `studien-archiv.json` | vollständige Historie aller gezeigten Studien |
| `studien-feed.xml` | RSS 2.0 für Mailchimps RSS-to-Email |
| `download/` | Word- und Excel-Fassungen (aktuell + Archiv) |
| `scripts/update_studies.py` | PubMed → Claude-API → Marker-Block in `index.html` |
| `scripts/build_newsletter.py` | erzeugt Feed und Download-Dateien aus dem Archiv |
| `scripts/mailchimp_entwurf.py` | legt den Kampagnen-Entwurf zur Freigabe an |
| `.github/workflows/update-studies.yml` | tägliche Automatik, 04:00 UTC |

## Lokal ansehen

`index.html` im Browser öffnen — kein Server nötig. Einzige Ausnahme: Der Ordner
„Ältere Suchergebnisse" lädt `studien-archiv.json` per `fetch` nach und bleibt bei einem
`file://`-Aufruf leer.

## Einrichtung

1. Repository auf GitHub anlegen und pushen.
2. **Settings → Pages** → Source: `main`, Ordner `/`.
3. Die Datei `CNAME` im Wurzelverzeichnis setzt die Domain `ki.m-vf.de`; beim DNS-Anbieter
   einen CNAME-Eintrag `ki` → `mvf-portal.github.io` anlegen.
4. **Settings → Secrets → Actions**: `KIHUB` hinterlegen (Claude-API für die Studienauswahl),
   optional `KIHUBMC` für den Mailchimp-Entwurf. Die beiden Namen unterscheiden sich nur
   durch das Kürzel `MC` — nicht verwechseln.
5. In `scripts/mailchimp_entwurf.py` die `TAG_ID` des Tags „Studien-Newsletter KI" eintragen
   und in `newsletter.html` dieselbe Nummer bei `tagStudien`. Ohne sie läuft der Versand über
   die Gruppe `group[16137][2048]` — das genügt, ist aber weniger fein steuerbar.
