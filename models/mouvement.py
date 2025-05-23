class Mouvement:
    def __init__(self, id_mouvement, id_produit, type_mouvement, quantite, date):
        self.id_mouvement = id_mouvement
        self.id_produit = id_produit
        self.type_mouvement = type_mouvement  # 'entrée' ou 'sortie'
        self.quantite = quantite
        self.date = date
