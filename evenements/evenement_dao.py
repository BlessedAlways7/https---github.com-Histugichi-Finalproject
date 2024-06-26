import database

from evenements.evenement import Evenement
from flask_bcrypt import Bcrypt
#from evenement import Evenement


# Création de la classe EvenementDao.
class EvenementDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()

# Méthode créer un évènement.
    @classmethod
    def create_evenement(cls, evenement:Evenement):
        sql = "INSERT INTO evenement (nom, date, emplacement, total_seat, prix,id_evenement) VALUES (%s,%s,%s,%s,%s,%s)"
        params = (evenement.nom, evenement.date, evenement.emplacement, evenement.total_seat,evenement.prix, evenement.id_evenement)
        try:
            EvenementDao.cursor.execute(sql, params)
            EvenementDao.connexion.commit()
            message = 'success'
        except Exception as error:
            message = 'failure'
        return message

# Méthode pour afficher tout les évènements.
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM evenement"
        try:
            EvenementDao.cursor.execute(sql)
            evenements = EvenementDao.cursor.fetchall()
            message = 'success'
        except Exception as error:
            evenements = []
            message ="erreur"
        return (message, evenements)


# Méthode pour modifier l'évènement.
    @classmethod
    def modifier_evenement(cls, id_evenement, nouveau_evenement:Evenement):
        sql = "UPDATE evenement SET nom = %s, date = %s, emplacement = %s, total_seat = %s, prix = %s WHERE id_evenement = %s"
        params = (nouveau_evenement.nom, nouveau_evenement.date, nouveau_evenement.emplacement,nouveau_evenement.total_seat, nouveau_evenement.prix,id_evenement)
        try:
            EvenementDao.cursor.execute(sql,params)
            EvenementDao.connexion.commit()
            message='success'
        except Exception as error :
            message = 'erreur'
        return message

# Méthode pour supprimer un évènement.
    @classmethod
    def supprimer_evenement(cls, id_evenement):
        sql = "DELETE FROM evenement WHERE id_evenement = %s"
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,))
            EvenementDao.connexion.commit()
            message= "L'événement a été supprimé avec succès."
            success=True
        except Exception as error :
            message = "Erreur lors de la suppression de l'évenement."
            success=False
        return success,message

# Méthode pour récupérer un évènement par ID de l'évènement.
    @classmethod
    def recuperer_evenement_par_id(cls, id_evenement):
        sql = "SELECT * FROM evenement WHERE id_evenement = %s" 
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,))
            evenement = EvenementDao.cursor.fetchone()
            if evenement:
                return (evenement)
            else:
                return None
        except Exception as error:
            print(f"Erreur lors de la récupération de l'événement par ID", error)
        return None

# Méthode pour récupérer l'évènement par son nom.
    @classmethod
    def get_evenement_id_by_name(cls, nom):
        sql = "SELECT id_evenement FROM evenement WHERE nom = %s"
        try:
            EvenementDao.cursor.execute(sql, (nom,))
            evenement = EvenementDao.cursor.fetchone()
            if evenement:
                return evenement[0]  
            else:
                return None
        except Exception as error:
            print("Error retrieving event ID by name")
            return None
        
    
# Méthode pour récupérer les information de l'évènement avec sa place réservée.
    @classmethod
    def get_event_info_with_reserved_places(cls):
        sql = """
                SELECT 
                    evenement.nom, 
                    evenement.id_evenement,
                    evenement.total_seat- COALESCE(COUNT(reservation.place), 0) AS available_places,
                    reservation.place
                FROM 
                    evenement
                LEFT JOIN 
                    reservation ON evenement.id_evenement= reservation.id_evenement
                GROUP BY 
                        evenement.nom, evenement.id_evenement, evenement.total_seat;
              """
        try:
            EvenementDao.cursor.execute(sql)
            event_info = EvenementDao.cursor.fetchall()
            return event_info
        except Exception as error:
             print("Error occurred while fetching event and reservation information:")
        return None
        
    