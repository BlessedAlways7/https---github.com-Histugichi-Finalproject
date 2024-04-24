import database
#from reservation import Reservation
#from statut import ReservationStatut

from reservations.statut import ReservationStatut
from reservations.reservation import Reservation
from evenements.evenement_dao import EvenementDao
from flask_bcrypt import Bcrypt

# Création de la classe ReservationDao.
class ReservationDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()

    def __init__(self) -> None:
        pass

    # Méthode pour afficher toute les réservations.
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM reservation"
        try:
            ReservationDao.cursor.execute(sql)
            reservations = ReservationDao.cursor.fetchall()
            message = 'success'
        except Exception as error:
            reservations = []
            message ="erreur"
        return (message, reservations)
    
    # Méthode reserver_place pour réserver une place.
    @classmethod
    def reserver_place(cls,reservation:Reservation):
        sql = "INSERT INTO reservation (nom, date, place,id_evenement,id_user,statut) VALUES (%s,%s, %s,%s,%s,%s)"
        params = (reservation.nom, reservation.date,reservation.place, reservation.id_evenement,reservation.id_user, reservation.statut)   
        try:
            ReservationDao.cursor.execute(sql, params)
            ReservationDao.connexion.commit()   
            success=True 
            message = 'success'
            # Récupération du dernier ID inséré
            last_id = ReservationDao.cursor.lastrowid
        except Exception as error:
            print(error)
            success=False
            message = 'failure'
            print("Error lors de l'insertion de la réservation")
        return (success,message,last_id)
        
    # Méthode pour confirmer une réservation.
    @classmethod
    def confirmer_reservation(cls, id_reservation):
        # Mettre à jour le statut de la réservation dans la base de données
        sql = "UPDATE reservation SET statut = %s WHERE id = %s"
        params = (ReservationStatut.CONFIRME.value, id_reservation)
        try:
            ReservationDao.cursor.execute(sql, params)
            ReservationDao.connexion.commit()
            message = 'success'
        except Exception as error:
            message = 'failure'
        return message
    
    # Méthode pour retourner les places reserver selon id de l'evenement.
    @classmethod
    def places_reservees(cls,id_evenement):
        sql = "SELECT SUM(place) FROM reservation WHERE id_evenement = %s" 
        try:
            ReservationDao.cursor.execute(sql(id_evenement,))
            nombre_reservations = ReservationDao.cursor.fetchone()[0]
            print (f"Nombre de reservations pour l'événement {id_evenement}: {nombre_reservations}")
            return nombre_reservations if nombre_reservations is not None else 0  
        except Exception as error:
            print (f"Erreur lors de la récupération des réservations pour l'événement {id_evenement}")
            return 0
         
    # Méthode  pour calculer les places disponibles.
    @classmethod
    def places_disponibles(cls,id_evenement,nom):
        total_seats = EvenementDao.get_event_info_with_reserved_places(id_evenement,nom)
        if total_seats is not None:
            return None       
        places_reservees=ReservationDao.places_reservees(id_evenement)
        if places_reservees is not None:
            return None
        places_disponibles= total_seats - places_reservees
        return places_disponibles
        
    # Méthode pour afficher les réservation par ID de l'utilisateur.
    @classmethod
    def filtrer_reservations_id_user(cls,id_user):
        sql = """SELECT *FROM reservation WHERE id_user = %s"""
        try:
            ReservationDao.cursor.execute(sql,(id_user,))
            reservations = ReservationDao.cursor.fetchall()
            if reservations:
                return reservations, f"Voici les réservations de l'utilisateur: {id_user}."
            else:
                return None, f" Malheureusement, aucune reservation à été fait pour {id_user}!"
        except Exception as error:
           return None, f"Erreur lors de la récupération des réservations. "

    # Méthode pour afficher le statut de la réservation.
    @classmethod
    def afficher_statut_reservations(cls):
        sql= "SELECT*FROM reservation" 
        try:
            ReservationDao.cursor.execute(sql)
            reservations = ReservationDao.cursor.fetchall()
            return reservations
        except Exception as error:
            print("Erreur lors de l'affichage des statuts des réservations.")
            return None
           
     # Méthode pour annuler une réservation.      
    @classmethod
    def annuler_reservation(cls,id_evenement,id_user,id_reservation):
        sql = """DELETE FROM reservation WHERE id_evenement=%s AND id_user = %s AND id_reservation= %s"""
        try:
            ReservationDao.cursor.execute(sql, (id_evenement,id_user,id_reservation))
            ReservationDao.connexion.commit()
            if ReservationDao.cursor.rowcount > 0:
                message='success'
            else:
                message = 'Aucune réservation retrouver avec ce ID.'
        except Exception as error:
            message='error'
        return message
    
    # Méthode pour mise a jour du statut de la reservation.
    @classmethod
    def update_statut_reservation(cls,id_reservation, nouveau_statut):
        sql=  "UPDATE reservation SET statut = %s WHERE id_reservation = %s"
        try:
            ReservationDao.cursor.execute(sql,(nouveau_statut,id_reservation))
            ReservationDao.connexion.commit()
            return 'success'
        except Exception as error:
            return ('error')
            
            

        
        
           
                