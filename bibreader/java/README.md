## Structure du projet

Ce projet JAVA est structuré en plusieurs dossiers :

- `src`: dossier du code source du projet
- `lib`: dossier des dépendences (`jar`)
- `jar`: dossier contenant le projet exporté en `jar`
- `bin`: dossier de compilation
- `.vscode`: dossier de configuration du projet dans vscode

Par ailleurs, 3 fichiers sont présents à la racine du projet :

- `Readme.md`: la documentation du projet
- `connect.sh`: script de configuration du raspberry à éxécuter au démarrage
- `exemple.py`: démonstration d'interfaçage du projet en python grâce à la librairie `jpype`

## Dépendences

Plusieurs dépendences sont nécessaire au bon fonctionnement du projet. Elles sont contenues dans le dossier `lib` sous forme de fichier `jar`:

- `json`: utilisé pour l'encodage des paramètres par le serveur de développement.
- `CAENRFIDLibrary`: la librairie fournie par CAEN RFID pour la lécture/écriture des tags RFID.
- `RXTXcomm`: utilisé par `CAENRFIDLibrary` pour la communication série avec le lecteur (branché en USB).

## Modes d'utilisation de `me.cocktail.jar`

Le `jar` construit à partir du projet rassemble dans un fichier unique l'ensemble du projet et peut ainsi être exporté et utilisé seul. Il s'utilise de 2 manières différentes :

- en tant que dépendences : importé dans d'autres projets JAVA ou python via JPype, il permet de lire/ecrire les tags RFID des **bibs**.
- en tant que serveur de test : directement executé via `java -jar me.cocktail.jar`, un serveur http sert une API basique permettant de lire une étiquette de **bib** (requête `GET`) et de l'écrire (requête `POST`)

## Détail des classes JAVA

- `BibReader.java`
- utils:
  - `Bib.java`: classe représentant un **bib** (BibID + BibData)
  - `BibID.java`: classe représentant l'ID d'un **bib**
  - `BibData.java`: classe représentant les données d'un **bib**
- dev:
  - `App.java`: point d'entrée de l'application (lancé par la commande `java -jar me.cocktail.jar`)
  - `HttpDevServer.java`: répondeur HTTP du serveur de test

### Lecture des tags

La classe `BibReader`, lorsqu'elle est instanciée, démarre la communication avec le lecteur. Les méthodes `readTag` et `writeTag` permettent ensuite de lire les tags grâce à la connexion au lecteur. Ces deux méthodes travaillent en entrée ou sortie avec la classe `Bib` qui est détaillée ci-dessous.

### Ecodage des informations

Les classes `BibID` et `BibData` sont des classes utilitaires chargées de décoder et réencoder les informations lues sous forme de tableau bytes (`byte[]`) vers un format plus facielement exploitable (chaîne de caractère, nombre).

L'identifiant, géré par la classe `BibID` est représenté par une chaîne de caractère correspondant à son encodage en base64.

Les informations du **bib** sont encodées comme suit (sur les 16 octets du tag RFID) :

- quantité (en ml) : 2 octets (0 - 65 535)
- annee : 2 octets
- mois : 1 octet
- jour : 1 octet
- type du **bib** : 10 octets

La class `Bib` a pour simple role de représenter un assemblage d'un identifiant et de données.

### Serveur de test

Le serveur de test repose sur la représentation d'un **bib** sous forme d'objet JSON.

- id : `string`
- data : `object`
  - quantity : `number`
  - e_year: `number`
  - e_month: `number`
  - e_day: `number`
  - type: `string`

2 routes sont définies :

- GET /api : lit le **bib** sous l'antenne
  - entrée : aucune
  - sortie :
    - lecture réussie : code 200, **bib** JSON
    - lecture impossible : code 500, détail de l'erreur
- POST /api : écrit le **bib** sous l'antenne après verification de son identifiant
  - entrée (corps) : **bib** JSON
  - sortie :
    - écriture réussie : code 200
    - écriture impossible : code 500, détail de l'erreur
