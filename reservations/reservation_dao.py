import database
from reservations.statut import ReservationStatut
from reservations.reservation import Reservation
from flask_bcrypt import Bcrypt


class ReservationDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()

    def __init__(self) -> None:
        pass

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
    
    @classmethod
    def reserver_place(cls,reservation:Reservation):
        sql = "INSERT INTO reservation (nom, date, place,id_evenement,id_user,id_reservation,statut) VALUES (%s,%s, %s, %s,%s,%s,%s)"
        params = (reservation.nom, reservation.date,reservation.place, reservation.id_evenement,reservation.id_user,reservation.id_reservation, reservation.statut)   
        try:
            ReservationDao.cursor.execute(sql, params)
            ReservationDao.connexion.commit()    
            message = 'success'
        except Exception as error:
            message = 'failure'
        return message
        

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
        
        
    @classmethod
    def places_reservees(cls):
        sql = "SELECT SUM(place) FROM reservation"
        try:
            ReservationDao.cursor.execute(sql)
            nombre_reservations = ReservationDao.cursor.fetchone()[0]
            print (f"Nombre de reservations: {nombre_reservations}")
            return nombre_reservations   
        except Exception as error:
            print (f"Erreur lors de la récupération des réservations! {error}")
            return 0

       
    @classmethod
    def nombre_places_disponibles(cls):
        capacite_totale= 200
        try:
            reservations= ReservationDao.places_reservees()
            disponibles = capacite_totale - reservations
            return disponibles if disponibles >= 0 else 0          
        except Exception as error:
            print(f"Erreur lors du calcul des places disponibles!", error)
            return 0

    @classmethod
    def filtrer_reservations_par_personne(cls,nom):
        sql = """SELECT *FROM reservation WHERE nom = %s"""
        try:
            ReservationDao.cursor.execute(sql,(nom,))
            reservations = ReservationDao.cursor.fetchall()
            if reservations:
                return reservations, f"La personne {nom} a réservé la place."
            else:
                return None, f" Malheureusement, aucune reservation à été fait pour {nom}!"
        except Exception as error:
           return None, f"Erreur lors de la récupération des réservations : {error}"

    @classmethod    
    def belongs_to_user(cls, id_reservation, id_user):
        sql = "SELECT COUNT(*) FROM reservation WHERE id_reservation = %s AND id_user = %s"
        params = (id_reservation, id_user)
        try:
            cls.cursor.execute(sql, params)
            count = cls.cursor.fetchone()[0]
            return count > 0  # If count is greater than 0, the reservation belongs to the user
        except Exception as error:
            print("Error checking if reservation belongs to user")
            return False 
        

    @classmethod
    def annuler_reservation(cls,id):
        sql = """DELETE FROM reservation WHERE id = %s"""
        try:
            ReservationDao.cursor.execute(sql, (id,))
            ReservationDao.connexion.commit()
            if ReservationDao.cursor.rowcount > 0:
                return f"La réservation au numero {id} a bien été annulée."
            else:
                return f"Impossible d'annuler cette réservation car elle n'existe pas."
        except Exception as error:
            return f"Une erreur est survenue lors de l'annulation de la réservation : {error}"
           
                