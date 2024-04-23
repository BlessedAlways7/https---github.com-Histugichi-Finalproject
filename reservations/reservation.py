class Reservation:
    def __init__(self,nom,date, place,id_evenement,id_user, statut) -> None:
        self.__nom = nom
        self.__date = date
        self.__place = place
        self.__id_evenement= id_evenement
        self.__id_user= id_user
        self.__statut= statut
        
    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, value):
        self.__nom = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        self.__place = value

    @property
    def id_evenement(self):
        return self.__id_evenement

    @id_evenement.setter
    def id_evenement(self, value):
        self.__id_evenement = value

    @property
    def id_user(self):
        return self.__id_user

    @id_user.setter
    def id_user(self, value):
        self.__id_user = value

    @property
    def statut(self):
        return self.__statut

    @statut.setter
    def statut(self, value):
        self.__statut = value

  

     

   