# Création de la classe Paiemenet avec les attributs.
class Paiement:
    def __init__(self,montant,mode_paiement,numero_carte,date_expiration,cvv) -> None:
        
        self.__montant = montant
        self.__mode_paiement = mode_paiement
        self.__numero_carte = numero_carte
        self.__date_expiration = date_expiration
        self.__cvv = cvv

    @property
    def montant(self):
        return self.__montant

    @montant.setter
    def montant(self, value):
        self.__montant = value

    @property
    def mode_paiement(self):
        return self.__mode_paiement

    @mode_paiement.setter
    def mode_paiement(self, value):
        self.__mode_paiement = value

    @property
    def numero_carte(self):
        return self.__numero_carte

    @numero_carte.setter
    def numero_carte(self, value):
        self.__numero_carte = value

    @property
    def date_expiration(self):
        return self.__date_expiration

    @date_expiration.setter
    def date_expiration(self, value):
        self.__date_expiration = value

    @property
    def cvv(self):
        return self.__cvv

    @cvv.setter
    def cvv(self, value):
        self.__cvv = value

        