from enum import Enum

# Création de la classe ReservationStatut avec les attributs.
class ReservationStatut(Enum):
    CONFIRME = "Confirme"
    EN_ATTENTE = "En attente"
    ANNULE = "Annule"