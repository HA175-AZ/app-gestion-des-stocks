import sqlite3
import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('gestion_stock.db')
        self.creer_tables()

    def creer_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS produit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            quantite INTEGER,
            prix REAL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS mouvement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produit INTEGER,
            type_mouvement TEXT,
            quantite INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_produit) REFERENCES produit(id)
        )''')
        # Vérifier si la colonne existe avant de l'ajouter
        cursor.execute("PRAGMA table_info(produit)")
        colonnes = [colonne[1] for colonne in cursor.fetchall()]
    
        if "seuil_alerte" not in colonnes:
            cursor.execute("ALTER TABLE produit ADD COLUMN seuil_alerte INT DEFAULT 5")
           
        self.conn.commit()

    def fetch_one(self, query, params=()):
        """ Exécute une requête SQL et retourne une seule ligne """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()  # Retourne une ligne sous forme de tuple (ou None si aucun résultat)


    def ajouter_produit(self, nom, description, quantite, prix):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO produit (nom, description, quantite, prix)
                          VALUES (?, ?, ?, ?)''', (nom, description, quantite, prix))
        self.conn.commit()

    def modifier_produit(self, id_produit, nom, description, quantite, prix):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE produit
                          SET nom = ?, description = ?, quantite = ?, prix = ?
                          WHERE id = ?''', (nom, description, quantite, prix, id_produit))
        self.conn.commit()

    def supprimer_produit(self, id_produit):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM produit WHERE id = ?''', (id_produit,))
        self.conn.commit()

    def lister_produits(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM produit''')
        return cursor.fetchall()

    
    
    def enregistrer_mouvement(self, id_produit, type_mouvement, quantite):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO mouvement (id_produit, type_mouvement, quantite)
                          VALUES (?, ?, ?)''', (id_produit, type_mouvement, quantite))
        self.conn.commit()

    def mettre_a_jour_stock(self, id_produit, quantite, type_mouvement):
        cursor = self.conn.cursor()
        if type_mouvement == "entrée":
            cursor.execute('''UPDATE produit SET quantite = quantite + ? WHERE id = ?''', (quantite, id_produit))
        elif type_mouvement == "sortie":
            cursor.execute('''UPDATE produit SET quantite = quantite - ? WHERE id = ? AND quantite >= ?''', 
                           (quantite, id_produit, quantite))
        self.conn.commit()





    def generer_rapport_stock(self, periode="quotidien"):
        cursor = self.conn.cursor()
    
        # Déterminer la date de début du rapport
        if periode == "quotidien":
            date_debut = datetime.date.today()
        elif periode == "hebdomadaire":
            date_debut = datetime.date.today() - datetime.timedelta(days=7)
        elif periode == "mensuel":
            date_debut = datetime.date.today().replace(day=1)
        else:
            return []
    
        # Récupérer les variations et le stock actuel
        cursor.execute('''
            SELECT produit.nom, 
                   SUM(CASE WHEN mouvement.type_mouvement = 'entrée' THEN mouvement.quantite ELSE -mouvement.quantite END) AS variation_stock,
                   produit.quantite
            FROM mouvement
            JOIN produit ON mouvement.id_produit = produit.id
            WHERE mouvement.date >= ?
            GROUP BY produit.nom, produit.quantite
        ''', (date_debut,))
    
        rapport = cursor.fetchall()
        return rapport  # Retourne (produit, variation_stock, stock_actuel)
