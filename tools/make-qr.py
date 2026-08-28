#!/usr/bin/env python3
"""Genere les fichiers QR code qui pointent vers le menu digital.

Usage :
    pip install segno
    python3 tools/make-qr.py                      # utilise l'URL par defaut
    python3 tools/make-qr.py https://mon-site.fr/menu.html

Produit a la racine du depot :
    menu-qr.svg  -> vectoriel, a utiliser pour l'impression (affiche, chevalet, flyer)
    menu-qr.png  -> bitmap 1000x1000, a utiliser sur les reseaux sociaux
"""

import pathlib
import sys

import segno

# URL par defaut du menu (GitHub Pages de ce depot).
# Change cette ligne si le menu est heberge sur ton propre domaine.
URL_MENU = "https://kevinyessfit.github.io/Business-Cookie/menu.html"

# Couleurs de la marque (identiques a menu.html).
CHOCO = "#3A2318"
CREAM = "#FFFDF9"

RACINE = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else URL_MENU

    # Correction d'erreur H : le QR reste lisible meme abime, sali ou
    # partiellement recouvert par un logo — indispensable en usage restaurant.
    qr = segno.make(url, error="h")

    svg = RACINE / "menu-qr.svg"
    png = RACINE / "menu-qr.png"

    qr.save(svg, scale=10, border=4, dark=CHOCO, light=CREAM)
    qr.save(png, scale=20, border=4, dark=CHOCO, light=CREAM)

    print(f"URL encodee : {url}")
    print(f"Version QR  : {qr.version} (correction {qr.error.upper()})")
    for f in (svg, png):
        print(f"Ecrit       : {f.relative_to(RACINE)} ({f.stat().st_size} octets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
