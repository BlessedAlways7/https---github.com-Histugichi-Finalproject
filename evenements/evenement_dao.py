import database
from evenements.evenement import Evenement
from flask_bcrypt import Bcrypt
#from evenement import Evenement


class EvenementDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()

    @classmethod
    def create_evenement(cls, evenement:Evenement):
        sql = "INSERT INTO evenement (nom, date, emplacement, prix,id_evenement) VALUES (%s,%s,%s,%s,%s)"
        params = (evenement.nom, evenement.date, evenement.emplacement, evenement.prix, evenement.id_evenement)
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
        sql = "UPDATE evenement SET nom = %s, date = %s, emplacement = %s, prix = %s, WHERE id = %s",
        params = (nouveau_evenement.nom, nouveau_evenement.date, nouveau_evenement.emplacement, nouveau_evenement.prix,id_evenement)
        try:
            EvenementDao.cursor.execute(sql,params)
            EvenementDao.connexion.commit()
            message="Mise à jour réussie"
        except Exception as error :
            message = "Erreur lors de la modification de l'évenement"
        return message
      
    @classmethod
    def supprimer_evenement(cls, id_evenement):
        sql = "DELETE FROM evenement WHERE id_evenement = %s"
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,))
            EvenementDao.connexion.commit()
            message= "L'événement a été supprimé avec succès."
        except Exception as error :
            message = "Erreur lors de la suppression de l'évenement"
        return message

    @classmethod
    def recuperer_evenement_par_id(cls, id_evenement):
        sql = "SELECT * FROM evenement WHERE id_evenement = %s" 
        try:
            EvenementDao.cursor.execute(sql,(id_evenement,))
            evenement = EvenementDao.cursor.fetchone()
            if evenement:
                return Evenement(evenement)
            else:
                return None
        except Exception as error:
            print("Erreur lors de la récupération de l'événement par ID")
        return None