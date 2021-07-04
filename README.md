## Willkommen bei 1337observer

Hier werden einfache Tools und Listen programmiert, um das Internet zu scannen.

* Unter /results sind einige Subdomain Scans.
* Unter /scripts liegen `online-checker.py` und `leak-checker.py`.
* Unter /howtos gibt es Anleitungen zu einzelnen Scripten.

## Ablauf:

* Domain scans in `/results/domainname` danach subdomain scan in `/results/domainname_subs`.
* `active-checker.py` einfaches Banner grabbing!
* `open-websites.py` zum einfachen Durchklicken der Ergebnisse.
* `leak-checker.py`zum Suchen von interessanten Dateien in den Subdomains.

## active-checker.py
Überprüft eine Liste von Subdomains, ob die Seite erreichbar ist und speichert zusätzlich ein paar Metadaten.

```
python3 scripts/active-checker.py -i results/domainname_subs/amass.txt -o results/domainname_subs/active.txt
```

## leak-checker.py

```
python3 scripts/leak-checker.py
```

## IPv4 Scan:

Ergebnis wird in `/results/ipv4/results_datum.txt` gespeichert.

```
python3 scripts/ipv4-scan.py
```
