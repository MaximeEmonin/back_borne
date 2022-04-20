 Backend de la borne Cocktail.me

## Table des Matières

 - [Description Générale](#description-générale)
 - [Description Technique](#description-technique)
 - [Documentation de l'API](#documentation-de-lapi)

## Description générale
Ceci est le serveur qui tournera sur le *Raspberry Pi* interne à la borne **Cocktail.me**.
Le serveur fait la liaison entre le contrôleur des BIBs, le contrôleur des pompes, la base de données, et l'interface utilisateur.

## Description Technique
le serveur est codé en python, avec le Framework *FastAPI*.
La technologie de base de données est *PostgreSQL*.

## Documentation de l'API

> NOTE: L'API retourne toutes les valeurs au format JSON

### GET /bibs
**arguments**: aucun <br/>
**retourne**: liste de Bibs <br/>
> **Exemple**: 
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
