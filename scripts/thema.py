#!/usr/bin/env python3
"""Alles Themenspezifische der taeglichen Studienauswahl — und sonst nichts.

Beim Anschluss an die Vorlage am 18.08.2026 woertlich aus update_studies.py
uebernommen, damit sich an der taeglichen Auswahl nichts aendert.
`update_studies.py` ist seither in allen Portalen wortgleich und wird zentral
gepflegt; wer die Auswahl aendern will, aendert Text in DIESER Datei.
"""
from __future__ import annotations

import os

# NCBI bittet bei automatisierten Zugriffen um eine Tool-Kennung.
NCBI_TOOL = "ki-gesundheit-portal"

# Die digitale Seite UND die Versorgungsseite muessen beide vorkommen - sonst
# spuelt die Abfrage reine Informatik oder reine Klinik herein. Entscheidend ist
# hier zusaetzlich das [Majr] bzw. [Title]: Maschinelles Lernen taucht inzwischen
# in jeder zweiten Auswertung als blosses Statistikwerkzeug auf. Nur wenn die
# Technik HAUPT-Schlagwort ist oder im Titel steht, geht es wirklich um sie.
_DIGITAL = (
    '("Artificial Intelligence"[Majr] OR "Machine Learning"[Majr] '
    'OR "Deep Learning"[Majr] OR "Medical Informatics"[Majr] '
    'OR "Telemedicine"[Majr] OR "Digital Technology"[Majr] '
    'OR "Electronic Health Records"[Majr] '
    'OR "Decision Support Systems, Clinical"[Majr] '
    'OR "Mobile Applications"[Majr] OR "Natural Language Processing"[Majr] '
    'OR "Health Information Interoperability"[Majr] '
    'OR "artificial intelligence"[Title] OR "machine learning"[Title] '
    'OR "deep learning"[Title] OR "large language model*"[Title] '
    'OR "digital health"[Title] OR telemedicine[Title] OR telehealth[Title] '
    'OR "clinical decision support"[Title] OR "electronic health record*"[Title] '
    'OR chatbot*[Title] OR "digital therapeutic*"[Title] OR mHealth[Title])'
)
_VERSORGUNG = (
    '("Delivery of Health Care"[MeSH Terms] OR "Health Services"[MeSH Terms] '
    'OR "Quality of Health Care"[MeSH Terms] OR "Patient Care"[MeSH Terms] '
    'OR "Health Policy"[MeSH Terms] OR "Public Health"[MeSH Terms] '
    'OR "Patient Safety"[MeSH Terms] OR "Hospitalization"[MeSH Terms] '
    'OR "health care"[Title/Abstract] OR "health services"[Title/Abstract] '
    'OR "patient outcome*"[Title/Abstract] OR "clinical practice"[Title/Abstract] '
    'OR workflow[Title/Abstract] OR implementation[Title/Abstract] '
    'OR patients[Title/Abstract] OR clinicians[Title/Abstract])'
)
# "Humans"[MeSH] haelt Methodenarbeiten ohne Menschenbezug heraus - Bildverarbeitung
# an Phantomen, Laborautomatisierung, reine Benchmark-Studien. Gemessen am
# 17.08.2026: rund 321.000 Treffer gesamt, 37.000 mit Europa-/Deutschlandbezug.
# Das ist ein Vielfaches der Schwesterportale; Nachschub ist hier nie das Problem,
# die Trennung von Anwendung und Methodendemonstration schon.
TERM = os.environ.get(
    "SEARCH_TERM",
    f'(({_DIGITAL} AND {_VERSORGUNG}) AND "Humans"[MeSH Terms])',
)
# Zweite Abfrage, damit Arbeiten mit Deutschland- und Europabezug den
# Kandidatenpool sicher erreichen. Ueber MeSH und Autorenadresse, nicht ueber
# Journalnamen - deutschsprachige Journale liefern kaum Treffer.
TERM_DE = os.environ.get(
    "SEARCH_TERM_DE",
    f"{TERM} AND (Germany[MeSH Terms] OR Germany[Affiliation] "
    "OR Europe[MeSH Terms] OR Europe[Affiliation])",
)

# Groesse des Kandidatenpools und Reihenfolge der beiden Abfragen — beides so
# uebernommen, wie dieses Portal es bisher gehandhabt hat. EUROPA_ZUERST=False
# heisst: die allgemeine Abfrage steht vorn. Ein Sprachmodell gewichtet, was es
# zuerst liest; umzustellen ist eine redaktionelle Entscheidung.
POOL_EUROPA = 30
POOL_ALLGEMEIN = 25
EUROPA_ZUERST = True

# Wie viele Studien taeglich erscheinen. KAPPEN=False heisst: zu viele lassen
# den Lauf scheitern, statt gekuerzt zu werden.
# **Nicht ins JSON-Schema schreiben** — die Anthropic-API lehnt minItems > 1
# und maxItems ab.
ANZAHL_SOLL = 6
ANZAHL_MAX = 7
ANZAHL_MIN = 5
KAPPEN = True

# ------------------------------------------------------------------- Prompts
SYSTEM = (
    "Du bist Fachredakteur fuer Digitalisierung und Kuenstliche Intelligenz im "
    "Gesundheitswesen. Aus einer Liste von PubMed-Abstracts waehlst du die "
    "relevantesten aktuellen Studien aus und fasst sie praezise auf Deutsch "
    "zusammen. Deine Leserschaft arbeitet im deutschen Gesundheitswesen: "
    "Kliniken, Praxen, Kostentraeger, Selbstverwaltung, Gesundheitspolitik, "
    "Medizininformatik. Sie will wissen, was eine Anwendung in der Versorgung "
    "leistet - nicht, welches Modell den hoechsten AUC-Wert erreicht hat."
)

USER_TEMPLATE = """Unten stehen aktuelle PubMed-Abstracts (nach Datum sortiert).

Waehle GENAU 6 Studien aus, die (a) eine digitale Technologie oder ein
KI-Verfahren IN DER GESUNDHEITSVERSORGUNG untersuchen UND (b) im Abstract
KONKRETE quantitative Ergebnisse nennen (Prozentwerte, Sensitivitaet/Spezifitaet,
Odds/Hazard Ratios, Zeitersparnis, Fallzahlen, p-Werte). Ueberspringe Studien
ohne Abstract oder ohne konkrete Ergebnisse. Achte auf thematische Vielfalt.

THEMATISCHE RANGFOLGE - in dieser Reihenfolge bevorzugen:
  1. Anwendung in der Versorgung: KI-gestuetzte Diagnostik und Entscheidungs-
     unterstuetzung im klinischen Betrieb, Telemedizin, digitale Gesundheits-
     anwendungen, elektronische Patientenakte, Dokumentation und Entlastung
     von Personal - jeweils MIT gemessenem Effekt auf Versorgung, Ergebnis,
     Sicherheit oder Aufwand.
  2. Einfuehrung und Wirkung im System: Implementierungsforschung, Akzeptanz
     bei Personal und Patienten, Prozess- und Kostenwirkungen, Reifegrad,
     Auswirkungen auf Zugang und Ungleichheit.
  3. Bewertung, Regulierung, Sicherheit: Nutzenbewertung digitaler Anwendungen,
     Evidenzanforderungen, Verzerrung und Fairness von Algorithmen, Haftung,
     Datenschutz und Datennutzung, Interoperabilitaet.
  4. Belastbare Validierungsstudien mit klinischem Bezug - aber nur, wenn an
     echten Patientendaten und moeglichst prospektiv oder extern validiert.

NICHT in die Auswahl gehoeren: reine Modellentwicklung ohne Versorgungsbezug,
Arbeiten, die maschinelles Lernen nur als Auswertungsverfahren einer
epidemiologischen Fragestellung verwenden, Benchmark-Vergleiche ohne klinische
Anwendung, Bildverarbeitung an Phantomen oder Zelllinien sowie Uebersichten
ohne eigene Zahlen.

ZWEI HARTE REGELN ZUR ZUSAMMENSETZUNG (sie gehen der thematischen Rangfolge vor):

  1. MINDESTENS DREI der sechs Studien muessen aus Europa stammen oder ein
     europaeisches Gesundheitssystem betreffen. Liegen weniger als drei solche
     Arbeiten vor, nimm die verbleibenden Plaetze aus dem Rest - aber schoepfe
     die europaeischen zuerst aus, auch wenn sie thematisch nur zweitbeste sind.
  2. HOECHSTENS ZWEI der sechs duerfen Studien zur reinen Bilddiagnostik sein
     (Radiologie, Pathologie, Dermatoskopie, Endoskopie). Dieses Feld publiziert
     um ein Vielfaches mehr als alle uebrigen und verdraengt sie sonst.

ZWEITES AUSWAHLKRITERIUM - Übertragbarkeit auf Deutschland:
Bei sonst gleicher Qualität hat die übertragbare Studie IMMER Vorrang vor der
aktuelleren. Übertragbarkeit richtet sich hier nach ZWEI Achsen:

  Strukturell: Deutschland, Österreich, Schweiz, Niederlande, Belgien, Frankreich
    hoch; Skandinavien, Großbritannien, Kanada, Australien mittel; USA gering.
    Skandinavien und Estland sind digital deutlich weiter - ihre Befunde zeigen,
    was möglich ist, aber nicht, was hier morgen umsetzbar wäre.
  Regulatorisch: Die EU setzt mit KI-Verordnung, MDR und Gesundheitsdatenraum
    einen eigenen Rahmen. Eine US-Studie zu einem FDA-zugelassenen Produkt sagt
    über die Zulassungsfähigkeit hierzulande wenig; über den klinischen Nutzen
    kann sie trotzdem viel sagen.

  Hoch:    Deutschland und deutschsprachiger Raum, vergleichbare Sozial-
           versicherungssysteme.
  Mittel:  Übriges Europa, Kanada, Australien - anderer Digitalisierungsgrad,
           ähnlicher Versorgungsauftrag.
  Gering:  USA und Länder mit grundlegend anderer Finanzierung oder
           Ressourcenlage. Nur nehmen, wenn die Fragestellung davon
           unabhängig ist (Methodik, Sicherheitsprobleme, Verzerrung).

Fuer jede Studie:
- journal: Journalname genau so, wie er in der Kopfzeile des Abstracts steht -
  Abkuerzung nicht aufloesen, nichts ergaenzen. (Wird ohnehin durch die Angabe
  aus PubMed ersetzt; rate hier nichts.)
- year: Erscheinungsjahr, z. B. "2026"
- pmid: die PubMed-ID
- title: praegnanter deutscher Titel. **Er MUSS mit der digitalen bzw.
  KI-bezogenen Fragestellung beginnen; der klinische Anwendungsfall steht
  hinten oder gar nicht drin.** Fast jede Arbeit in diesem Feld hat einen
  klinischen Traegerfall - Beatmung, Hautkrebs, Atemnot -, und die Abstracts
  sind danach betitelt. Wer das uebernimmt, macht aus dem Portal eine
  beliebige medizinische Studiensammlung: Wer nur die Ueberschrift liest,
  sieht dann eine Intensivmedizin-Studie statt einer Arbeit ueber
  Datenschutz beim Modelltraining.
  Gut:      "KI-Training ueber fuenf Kliniken hinweg, ohne Patientendaten zu
             teilen: was der Datenschutz an Genauigkeit kostet"
            "Elektronische Patientenberichte in der Onkologie: was die
             Erfassung per App am Behandlungsverlauf aendert"
  Schlecht: "Foederiertes Lernen zur Vorhersage der Beatmungsentwoehnung"
            (fuehrt mit dem Anlassfall, die eigentliche Frage verschwindet)
- sum: 1 Satz auf Deutsch, was die Studie untersucht hat. Wenn der klinische
  Fall nur der Anlass ist, an dem gerechnet wurde, sage das ausdruecklich -
  sonst haelt die Leserschaft ihn fuer den Gegenstand der Arbeit.
- result: Deutsch, die konkreten Zahlen/Befunde + ein kurzer Einordnungssatz.
  Deutsches Zahlenformat mit Komma (z. B. 0,63). **Der Einordnungssatz darf
  nicht behaupten, was die Autoren selbst ablehnen.** Wo ein Abstract eine
  Deutung ausdruecklich zurueckweist ("should be read as a performance
  comparison rather than a privacy-performance trade-off"), diese Einschraenkung
  uebernehmen statt sie zu ueberschreiben. Ein Rechercheportal referiert, es
  wertet nicht auf.
- transfer: EIN Halbsatz (höchstens 12 Wörter), warum das Ergebnis für Deutschland
  taugt - oder wo die Grenze liegt. Nenne Land bzw. System und Datengrundlage.
  Keine ganzen Sätze, keine Wiederholung des Titels.
  Gut:      "Deutsche Klinikdaten, vergleichbare Dokumentationspflichten"
            "Estland - deutlich höherer Digitalisierungsgrad als hierzulande"
            "Niederlande, vergleichbares Versicherungssystem"
            "USA - nur der Sicherheitsbefund ist übertragbar"
            "Nur bedingt: proprietäres Modell, hier nicht verfügbar"
  Schlecht: "Diese Studie ist gut übertragbar." (sagt nichts)

WICHTIG - Fachterminologie: Etablierte englische Fachbegriffe NICHT eindeutschen.
Sie sind auch im deutschen Fachdeutsch stehende Begriffe; eine woertliche Uebersetzung
wirkt unprofessionell und erschwert das Wiederfinden. Beispiele fuer Begriffe, die
englisch bleiben: Machine Learning, Deep Learning, Large Language Model, Clinical
Decision Support, Electronic Health Record, Federated Learning, Explainable AI,
Usability, Workflow, Screening, Follow-up, Outcome, Baseline, Setting, Hazard Ratio,
Odds Ratio, Public Health. Gaengige Abkuerzungen ebenfalls unveraendert lassen:
KI, LLM, EHR, CDSS, NLP, AUC, ROC, API, FHIR, ICU, DiGA.
Deutsche Fachbegriffe, die es gibt, aber verwenden: Elektronische Patientenakte,
Telemedizin, Videosprechstunde, Entscheidungsunterstuetzung, Interoperabilitaet,
Nutzenbewertung, Versorgungsqualitaet, Patientensicherheit, Dokumentationsaufwand.
Faustregel: Wuerde eine deutsche Fachzeitschrift wie Monitor Versorgungsforschung den
Begriff englisch stehen lassen, dann tue es auch. Im Zweifel englisch belassen und bei
Bedarf eine kurze deutsche Erlaeuterung in Klammern ergaenzen.

Gib ausschliesslich das geforderte JSON zurueck.

=== ABSTRACTS ===
{abstracts}
"""
