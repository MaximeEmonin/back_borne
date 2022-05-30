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
On trouve une documentation très complète [en ligne](https://fastapi.tiangolo.com/).
La technologie de base de données est *PostgreSQL*.

## Documentation de l'API

> NOTE: L'API retourne toutes les valeurs au format JSON

Voir La [documentation **ReDoc**](documentation.html).