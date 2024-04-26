Objectifs du Projet :
  
● Concevoir une application web permettant aux usagers de réserver des places pour des événements.

    Fonctionnalités principales de l'application :

● Système de réservation en ligne pour différents types d'événements.
● Interface conviviale pour les utilisateurs, avec des fonctionnalités de recherche, de sélection de places et de paiement sécurisé.
● Gestion des réservations côté administrateur, avec la possibilité d'ajouter, de modifier ou d'annuler des événements, ainsi que de visualiser les données sur les réservations.

Consignes du Projet :

    Gestion des Utilisateurs :

● Mise en place d'un système d'authentification pour les utilisateurs.
● Création et gestion de profils utilisateurs avec des informations personnelles.

    Gestion des Événements :

● Ajout, modification et suppression d'événements.
● Attribution de catégories ou de tags à chaque événement.
● Affichage d'une liste d'événements avec des détails pertinents.

    Système de Réservation :

● Mise en place d'un système de réservation de billets pour les événements.
● Possibilité d'annuler une réservation si nécessaire.
● Affichage du statut des réservations (confirmé, en attente, annulé).

    Interface Utilisateur Intuitive :

● Conception d'une interface utilisateur conviviale pour la navigation.
● Utilisation de technologies frontend modernes pour une expérience utilisateur optimale.

    Gestion de Base de Données :

● Création d'une base de données pour stocker les informations sur les utilisateurs, les événements, et les réservations.
● Utilisation de requêtes SQL pour récupérer, modifier ou supprimer des données.

    Sécurité :
    
● Implémentation de pratiques de sécurité pour protéger les données utilisateur.
● Validation des formulaires et prévention des attaques courantes.

Instructions étape par étape pour installer et configurer notre projet!

    L'installation :
    
On a install flask avec pip install flask , ainsi que l'environnement. Ensuite, on a monté le squelette du projet pour avoir une base de se qui est essentiel pour commencer.

    Fonctionnalités:

Base de données: billet
Tables: évènement, paiement, réservation, user
Package evenements: evenement.py, evenement_dao
Package paiements: paiement.py, paiement_dao
Package reservations: reservation.py, paiement_dao, statut.py
Package users: user.py, user_dao

  liste des Événements:

payement:on a décidé  d'ajouté le payement en lien avec les activités
statut:l'état de la réservation un coup acheté
s'enregistrer: l'utilisateur est capable de se créer un profil
login: l'utilisateur est capable de se connecter avec ses identifiants
Admin: il gère les utilisateurs, ils sont capable de gérer les événements de les supprimer, de voir le status.

  Gestion des Utilisateurs:
  
Système de Réservation
Réservations : Système de réservation des activitées avec la gestion des statuts .

    Authentification et la sécurité: 

Quand un utilisateur s'enregistre , son mot de passe devient hasher se qui fait qui a une sécurité et qu'on a décidé de ne pas l'afficher aussi en clair pour compliquer le hakage.

- os.environ object
- Méthode load_dotenv
- Fonction BCrypt
- .gitignore

  Technologies utilisées:
  
python3, flask, sql, jinja2, mysql ,bootstrap

Difficultées:

On a eu beaucoup de problème à joindre la DB avec notre code pour que le tout s'affiche correctement.Ensuite,pour afficher les places on réussisait a faire apparaître des chiffres et des id rentrer manuellement et non connecté avec la database.Pour suivre,le hashage des mot de passes des utilisateurs, on a perdu beaucoup de temps a essayé et dû au manque de formation à se niveau et au exigence demandé qui son très haute sur plusieurs niveau et non que sur le mot de passe il a fallu se débrouillé comme on a pu, on a apprécié le coup de main donné par le professeur.

Contributeurs:
Émilie Kusters  et Max Létourneau
