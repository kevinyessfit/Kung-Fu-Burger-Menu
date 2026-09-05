# KUNG FU BURGER — menu en ligne

La carte du restaurant sur téléphone, avec prise de commande WhatsApp,
accessible par QR code.

| Fichier | À quoi ça sert |
|---|---|
| `index.html` | La carte que voit le client, avec panier et envoi de commande WhatsApp |
| `qr.html` | L'affichette à imprimer (QR code + mode d'emploi) |
| `menu-qr.svg` / `menu-qr.png` | Le QR code seul, pour l'impression et les réseaux |
| `tools/make-qr.py` | Régénère le QR code si l'adresse du menu change |
| `images/` | Les 40 photos de plats + le logo, découpés dans la carte papier |
| `og-image.jpg` | L'aperçu affiché quand le lien est partagé (WhatsApp, TikTok) |
| `favicon.png` | L'icône de l'onglet et du raccourci sur l'écran d'accueil |

## 1. Ou le menu est heberge

Le menu est publie sur **Netlify**, a l'adresse :
`https://kungfuburger.org/`

C'est cette adresse qui est encodee dans le QR code. Le menu est la page
d'accueil du site : rien a taper apres le nom.

Le nom de domaine propre n'est pas cosmetique. Les adresses gratuites
precedentes (`kung-fu-burger-menu.netlify.app` puis
`kevinyessfit.github.io`) etaient toutes deux coupees par le reseau
mobile, connexion fermee des l'ouverture (ERR_CONNECTION_CLOSED), alors
que le web fonctionnait par ailleurs : ces sous-domaines d'hebergement
gratuit figurent sur des listes de filtrage anti-hameconnage.

**Chaque push sur `main` republie le site automatiquement**, en une minute
environ. `netlify.toml` decrit la construction ; il n'y a rien a regler a
la main.

Le site n'appelle aucun serveur exterieur : polices, images et logo sont
servis par le site lui-meme, pour ne dependre d'aucun domaine tiers
susceptible d'etre filtre.

### Si l'adresse change un jour

Trois choses sont a reprendre — **avant d'imprimer les affichettes, pas
apres** :

1. **regenerer le QR code** : mettre a jour `URL_MENU` en haut de
   `tools/make-qr.py`, puis `python3 tools/make-qr.py` ;
2. l'adresse affichee en bas de l'affichette, dans `qr.html` ;
3. les balises `og:url`, `og:image` et `twitter:image` en haut de
   `index.html`, qui doivent rester des adresses absolues.

### Renouvellement du domaine

`kungfuburger.org` est a renouveler chaque annee. **S'il expire, le QR
code cesse de fonctionner et toutes les affichettes posees sur les tables
deviennent inutiles.** Verifier que le renouvellement automatique est
actif et que la carte bancaire enregistree reste valide.

## 2. Comment le client commande

1. Il scanne le QR code posé sur la table ou collé en vitrine.
2. La carte s'ouvre, rangée par catégorie : Burgers, Menus, Snacks,
   À ajouter, Thé au lait, Milkshake, Jus, Café.
3. Il touche **Ajouter** (ou choisit **500 ML / 700 ML** pour les boissons).
   Une barre apparaît en bas avec le total en direct.
4. Il ouvre **Voir ma commande** : il ajuste les quantités, choisit
   *Sur place / À emporter / Livraison*, met son nom, son adresse si c'est
   une livraison, et une note éventuelle (« sans piment »…).
5. Il touche **Envoyer sur WhatsApp** : WhatsApp s'ouvre avec la commande
   déjà rédigée, il n'a plus qu'à envoyer.

Le message que tu reçois ressemble à ça :

```
Bonjour KUNG FU BURGER ! Je voudrais commander :

• 2 x Burger Bacon — 7 000 F
• 1 x Thé aux perles (700 ML) — 2 000 F

TOTAL : 9 000 F
Service : Livraison
Nom : Kevin
Adresse : Cotonou, Fidjrosse
Note : sans piment
```

Le panier est gardé dans le téléphone du client : s'il ferme la page par
erreur, il retrouve sa commande en revenant.

**Il n'y a pas de paiement en ligne** : le client commande, tu confirmes
et tu encaisses comme d'habitude. C'est volontaire — aucun compte à créer,
aucune commission à payer.

## 3. Modifier la carte

Tout se passe **dans `index.html`, dans le bloc `<script>` en bas du
fichier**. Rien d'autre n'est à toucher.

### Le restaurant — `CONFIG`

```js
const CONFIG = {
  nom:       "KUNG FU BURGER",
  whatsapp:  "2290194719079",       // international, sans + ni espaces
  telephone: "+229 01 94 71 90 79",
  modes:     ["Sur place", "À emporter", "Livraison"]
};
```

### Les plats — `CARTE`

Une catégorie :

```js
{
  id:"burgers", titre:"Burgers", zh:"汉堡",
  note:"Servis avec salade et sauce maison.",
  items:[
    { nom:"Burger Bacon", zh:"芝士培根牛肉堡", prix:3500 }
  ]
}
```

Une catégorie de boissons, avec deux formats :

```js
{
  id:"jus", titre:"Jus", zh:"水果茶",
  tailles:["500 ML","700 ML"],
  items:[
    { nom:"Jus de citron", zh:"金桔柠檬", prix:[1000,1500] }
  ]
}
```

- `prix: 3500` s'affiche **3 500 F** automatiquement.
- Avec `tailles`, chaque article prend **autant de prix que de tailles**
  (`prix:[1000,1500]`), et le client voit un bouton par format.
- `desc:"1 Burger & 1 Frites & 1 Soda"` ajoute une description (utilisée
  pour les Menus 1 à 8).
- `img:"burger-bacon"` affiche la photo `images/burger-bacon.webp` à gauche
  du nom. Sans `img`, la fiche reste alignée, seul le texte s'élargit.
  Pour remplacer une photo : garde le même nom de fichier, mets ton image
  carrée dans `images/`, et rien d'autre ne bouge.
- `dispo:false` affiche l'article en « Épuisé aujourd'hui » et retire le
  bouton — pratique pour une rupture du jour, sans supprimer la ligne.
- Ajouter une catégorie = ajouter un bloc `{ id, titre, items }`.
  Le menu de navigation en haut se met à jour tout seul.

Les plats d'une même catégorie sont affichés dans une grille : ils
s'alignent en colonnes régulières et gardent la même hauteur par rangée,
quelle que soit la longueur des noms.

## 4. Le QR code

**Le QR code ne change jamais quand tu modifies la carte.** Il pointe vers
l'adresse du site, pas vers son contenu : change tes prix autant que tu
veux, les affichettes déjà imprimées restent valables.

Il n'y a besoin de le régénérer que si l'**adresse** du menu change :

```bash
pip install segno
python3 tools/make-qr.py https://ton-domaine.com/
```

Mets alors à jour l'adresse écrite en bas de l'affichette, dans `qr.html`
(balise `<p class="url">`).

### Imprimer

Ouvre `qr.html` → bouton **Imprimer l'affichette**. Seule l'affichette part
au papier, les boutons et les explications sont masqués automatiquement.

- QR de **3 cm de côté minimum**, plus grand si l'affiche est lue de loin
- garder la marge claire autour du code
- ne rien coller ni écrire par-dessus

`menu-qr.svg` est vectoriel : agrandissable à n'importe quelle taille
(chevalet, kakémono, vitrine) sans perte de qualité.

## 5. Les photos

Les 40 photos ont été découpées dans ta carte papier scannée, nettoyées
(fond ramené au blanc) et enregistrées en WebP 240 × 240 — 223 Ko pour
l'ensemble, pensé pour la data mobile.

**12 articles n'ont pas de photo** : les 6 *Snacks* et les 6 *À ajouter*
sont de simples listes de prix sur la carte papier, sans image à découper.
Leurs fiches s'affichent sans vignette. Envoie-moi des photos et je les
ajoute — ou dépose-les toi-même dans `images/` puis ajoute `img:"..."` sur
l'article.

Les vignettes viennent d'un scan : la définition reste correcte à la taille
affichée, mais de vraies photos des plats seraient plus nettes. Certaines
gardent la pastille de prix imprimée sur la carte ; les montants qu'elles
portent sont ceux affichés par le menu.

## 6. Points à vérifier par le restaurant

Relevés en recopiant la carte papier :

- **Cappucino — 2 000 F** : le prix imprimé était masqué par une étiquette
  manuscrite « 2000 ». C'est ce prix qui a été retenu.
- **Un burger à 3 500 F a été laissé de côté** : sur la carte papier il est
  recouvert de deux papiers collés, seul « Ja… Bœuf Salé » reste lisible.
  S'il se vend encore, ajoute-le dans la catégorie `burgers`.
- **Orthographe corrigée** pour l'affichage client : Alie → Aile,
  cuissed → cuisse, Spaghtti → Spaghetti, Popcrn → Pop-corn,
  Crevette pané → Crevette panée. Les prix, eux, n'ont pas été touchés.
