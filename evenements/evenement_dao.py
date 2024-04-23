import database

from evenements.evenement import Evenement
from flask_bcrypt import Bcrypt
#from evenement import Evenement


class EvenementDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()

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

      
    @classmethod
    def supprimer_evenement(cls, id_evenement):
        sql = "DELETE FROM evenement WHERE id_evenement = %s"
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,))
            EvenementDao.connexion.commit()
            message= "L'événement a été supprimé avec succès."
            success=True
        except Exception as error :
            message = "Erreur lors de la suppression de l'évenement"
            success=False
        return success,message

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
    

    @classmethod
    def get_event_info_with_reserved_places(cls,id_evenement,nom):
        sql = """
                SELECT 
                    e.nom,
                    e.id_evenement, 
                    e.total_seat,
                    (e.total_seat - COALESCE(SUM(r.place), 0)) AS places_disponibles
                FROM 
                    evenement e
                LEFT JOIN 
                    reservation r ON e.id_evenement = r.id_evenement AND e.nom= r.nom
                WHERE 
                    e.id_evenement = %s AND e.nom = %s
                GROUP BY 
                    e.id_evenement, e.total_seat;
              """
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,nom))
            event_info = EvenementDao.cursor.fetchall()
            return event_info
        except Exception as error:
            print="error"
            return None
        
    