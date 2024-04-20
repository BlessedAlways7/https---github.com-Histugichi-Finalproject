from paiement_dao import PaiementDao
from paiement import Paiement


"""
(message,user) =UserDao.get_one('Diallo123')
print(user[3])

evenement = Evenement('Luge', '2024-03-16','Mont-Royal','15','LUGE5245')
message= EvenementDao.create_evenement(evenement)
print(message)
"""

paiement= Paiement('20','mastercard','254625476','2026-04-15','253')
message= PaiementDao.ajouter_paiement(paiement)
print(message)




