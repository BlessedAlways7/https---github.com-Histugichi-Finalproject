import database
from paiements.paiement import Paiement
#from paiement import Paiement

class PaiementDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()


    @classmethod
    def get_all(cls):
        sql = "SELECT *from paiement"
        try:
            PaiementDao.cursor.execute(sql)
            paiements = PaiementDao.cursor.fetchall()
            message = 'success'
        except Exception as error:
            users = []
            message = 'error'
        return (message, paiements)


    @classmethod
    def ajouter_paiement(cls, paiement:Paiement):
        sql = "INSERT INTO paiement (montant,mode_paiement,numero_carte,date_expiration,cvv) VALUES (%s,%s,%s,%s,%s)"
        params = (paiement.montant,paiement.mode_paiement,paiement.numero_carte,paiement.date_expiration,paiement.cvv)
        try:
            PaiementDao.cursor.execute(sql, params)
            PaiementDao.connexion.commit()
            message = 'success'        
        except Exception as error:
            message = 'failure'
        return message
  
    