from evenement_dao import EvenementDao
from evenement import Evenement
import bcrypt

"""
(message,user) =UserDao.get_one('Diallo123')
print(user[3])

evenement = Evenement('Luge', '2024-03-16','Mont-Royal','15','LUGE5245')
message= EvenementDao.create_evenement(evenement)
print(message)
"""

message = EvenementDao.supprimer_evenement('3567627')
print(message)




