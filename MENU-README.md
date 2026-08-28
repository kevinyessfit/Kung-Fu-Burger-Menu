# Menu digital + QR code

Trois fichiers, un seul endroit à modifier.

| Fichier | À quoi ça sert |
|---|---|
| `menu.html` | Le menu que voit le client sur son téléphone |
| `qr.html` | L'affichette à imprimer (QR code + mode d'emploi) |
| `menu-qr.svg` / `menu-qr.png` | Le QR code seul, pour l'impression et les réseaux |
| `tools/make-qr.py` | Régénère le QR code si l'adresse du menu change |

## 1. Mettre le menu en ligne

Le site est statique : n'importe quel hébergement fait l'affaire.
Avec **GitHub Pages** (gratuit) :

1. Sur GitHub → onglet **Settings** → **Pages**
2. *Source* : **Deploy from a branch**, branche `main`, dossier `/ (root)`
3. Enregistrer, attendre une minute

Le menu est alors accessible à :
`https://kevinyessfit.github.io/Business-Cookie/menu.html`

C'est exactement l'adresse encodée dans le QR code livré ici.

## 2. Modifier le menu

Tout se passe **dans `menu.html`, dans le bloc `<script>` en bas du fichier**.
Rien d'autre n'est à toucher.

### Les informations de la boutique — `CONFIG`

```js
const CONFIG = {
  nom:       "COOKIES BUSINESS",
  slogan:    "Cookies maison cuits le jour même…",
  devise:    "FCFA",
  infos:     ["Ouvert 9h – 20h", "Livraison possible"],
  whatsapp:  "",          // ex. "2250102030405" — sans + ni espaces
  telephone: "",          // ex. "01 02 03 04 05"
  brouillon: true         // ← passe à false quand le vrai menu est en place
};
```

- `whatsapp` rempli → un bouton **Commander sur WhatsApp** apparaît, avec un
  message déjà écrit. Laissé vide → le bouton ne s'affiche pas.
- `brouillon: false` → le bandeau rouge « menu de démonstration » disparaît.

### Les articles — `MENU`

```js
{
  titre: "Cookies à l'unité",
  note:  "Cuits le matin même.",       // facultatif
  items: [
    { nom: "Cookie chocolat noir",
      desc: "Pépites de chocolat noir, cœur fondant.",
      prix: 500,
      tags: ["Best-seller"] },          // facultatif, le 1er tag est doré
    { nom: "Cookie coco", prix: 600, dispo: false }   // affiché « Épuisé »
  ]
}
```

- `prix: 4900` s'affiche automatiquement **4 900 FCFA**.
  Pour un prix libre, écris du texte : `prix: "dès 2 500"`.
- `dispo: false` grise l'article et le barre — pratique pour une rupture du
  jour, sans avoir à supprimer la ligne.
- Ajouter une catégorie = ajouter un bloc `{ titre, items }` dans `MENU`.
  Le menu de navigation en haut se met à jour tout seul.

## 3. Le QR code

**Le QR code ne change jamais quand tu modifies le menu.** Il pointe vers
l'adresse de la page, pas vers son contenu. Les affichettes déjà imprimées
restent donc valables à vie, même si tu changes tous les prix.

Il n'y a besoin de le régénérer que si l'**adresse** du menu change :

```bash
pip install segno
python3 tools/make-qr.py https://ton-domaine.com/menu.html
```

Pense alors à mettre à jour l'adresse écrite en bas de l'affichette, dans
`qr.html` (balise `<p class="url">`).

### Imprimer

Ouvre `qr.html` dans un navigateur → bouton **Imprimer l'affichette**.
Seule l'affichette part à l'impression, les boutons et les explications sont
automatiquement masqués.

Conseils d'impression :
- QR de **3 cm de côté minimum** ; plus grand si l'affiche est lue de loin
- garder la marge claire autour du code
- ne rien coller ni écrire par-dessus

Le fichier `menu-qr.svg` est vectoriel : il peut être agrandi à n'importe
quelle taille (chevalet, kakémono, vitrine) sans perdre en qualité.
