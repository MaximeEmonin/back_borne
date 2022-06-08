# Backend de la borne Cocktail.me

## Table des Matières

 - [Description Générale](#description-générale)
 - [Description Technique](#description-technique)
 - [Documentation de l'API](#documentation-de-lapi)

## Description générale
Ceci est le serveur qui tournera sur le *Raspberry Pi* interne à la borne **Cocktail.me**.
Le serveur fait la liaison entre le contrôleur des BIBs, le contrôleur des pompes, la base de données, et l'interface utilisateur.

## Description Technique
le serveur est codé en python, avec le Framework *FastAPI*.
<<<<<<< HEAD
=======
On trouve une documentation très complète [en ligne](https://fastapi.tiangolo.com/).
>>>>>>> dev
La technologie de base de données est *PostgreSQL*.

## Documentation de l'API

> NOTE: L'API retourne toutes les valeurs au format JSON

<<<<<<< HEAD
### GET /bibs
**renvoie**: liste de Bibs <br/>
> **Exemple de réponse**: 
> 
> ```
> [
>   {
>     quantity: 700,
>     type: 4,
>     expiration_date: 1649455200
>   },
>   {
>     quantity: 100,
>     type: 2,
>     expiration_date: 1649455200
>   }
> ] 
> ```

### GET /recipes
**renvoie**: liste de recettes faisables considérant les BIBs actuellement insérés dans la machine <br/>
> **Exemple de réponse**: 
> 
> ```
> [
>   {
>     id: 1,
>     name: "mojito",
>     photo: 1,
>     quantities: {
>       2: 200,
>       4: 100
>     }
>   },
>   {
>     id: 2,
>     name: "sex on the beach",
>     photo: 2,
>     quantities: {
>       2: 100,
>       4: 300
>     }
>   },
> ] 
> ```
=======
Voir La [documentation **ReDoc**](documentation.html).
>>>>>>> dev
