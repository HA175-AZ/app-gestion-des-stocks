class Produit:
    def __init__(self, id_produit, nom, description, quantite, prix, seuil_alerte):
        self.id_produit = id_produit
        self.nom = nom
        self.description = description
        self.quantite = quantite
        self.prix = prix
        self.seuil_alerte = seuil_alerte