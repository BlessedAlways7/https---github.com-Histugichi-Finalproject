from enum import Enum

# Création de la classe ReservationStatut avec les attributs.
class ReservationStatut(Enum):
    CONFIRME = "Confirmé"
    EN_ATTENTE = "En attente"
    ANNULE = "Annulé"