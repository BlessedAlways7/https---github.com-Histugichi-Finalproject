from evenement_dao import EvenementDao
from evenement import Evenement
import bcrypt

"""
(message,user) =UserDao.get_one('Diallo123')
print(user[3])

evenement = Evenement('Luge', '2024-03-16','Mont-Royal','15','LUGE5245')
message= EvenementDao.create_evenement(evenement)
print(message)
message = EvenementDao.supprimer_evenement('3567627')
print(message)

"""
evenement=EvenementDao.recuperer_evenement_par_id(id_evenement)
nouveau_evenement=Evenement(
    id_evenement=id_evenement,
    nom='Bingo',
    date="2024-08-19",
    emplacement="Casino de Mont-Royal",
    prix="35",
)

message = EvenementDao.modifier_evenement(id_evenement,nouveau_evenement)
print(message)







