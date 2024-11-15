# Modélisation de la Base de Données pour le Projet

## 1. Identification des Entités et des Relations

En analysant le jeu de données, les principales entités et leurs relations ont été identifiées comme suit :

### Entités Principales
- **Annonce** : Représente chaque bien immobilier à vendre ou à louer.
- **Ville** : Table pour les villes uniques où se trouvent les biens.
- **Équipement** : Table pour les équipements spécifiques (ex. : "Ascenseur", "Balcon") avec une relation plusieurs-à-plusieurs avec les annonces.

### Relations
- **Annonce** et **Ville** : Relation plusieurs-à-un, une annonce est liée à une seule ville.
- **Annonce** et **Équipement** : Relation plusieurs-à-plusieurs, chaque annonce peut avoir plusieurs équipements, et chaque équipement peut appartenir à plusieurs annonces.

## 2. Définition des Attributs pour Chaque Entité

### Annonce
- **id** : Clé primaire, identifiant unique pour chaque annonce.
- **title** : Titre de l'annonce.
- **price** : Prix de l'annonce, stocké en texte pour permettre des valeurs comme "PRIX NON SPÉCIFIÉ".
- **datetime** : Date et heure de publication (utiliser DateTime en SQLAlchemy).
- **nb_rooms** : Nombre de pièces (entier).
- **nb_baths** : Nombre de salles de bain (entier).
- **surface_area** : Surface en mètres carrés (float).
- **link** : URL vers l'annonce.
- **city_id** : Clé étrangère pointant vers la table **Ville**.

### Ville
- **id** : Clé primaire, identifiant unique pour chaque ville.
- **name** : Nom de la ville.

### Équipement
- **id** : Clé primaire, identifiant unique pour chaque équipement.
- **name** : Nom de l'équipement (ex. : "Ascenseur", "Balcon").

### Table Associative
- **AnnonceEquipement** : Table intermédiaire pour gérer la relation plusieurs-à-plusieurs entre les entités **Annonce** et **Équipement**.

## 3. Conception du Schéma de la Base de Données

### Diagramme Entité-Relation (ERD)
Représentation des relations et des attributs des entités. 

- **Annonce** → **Ville** : Relation plusieurs-à-un.
- **Annonce** → **Équipement** : Relation plusieurs-à-plusieurs via la table **AnnonceEquipement**.

### Normalisation
Pour assurer la cohérence des données, le schéma suit les principes de normalisation :

1. **1ère forme normale (1NF)** : Chaque champ est atomique (indivisible).
2. **2ème forme normale (2NF)** : Les informations redondantes sont déplacées dans des tables séparées (comme **Ville** et **Équipement**).
3. **3ème forme normale (3NF)** : Tous les attributs dépendent uniquement de la clé primaire.
